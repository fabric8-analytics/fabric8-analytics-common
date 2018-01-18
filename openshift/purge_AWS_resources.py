#!/usr/bin/python3

"""Operations to purge/delete previously allocated AWS resources."""

import argparse
import boto3
from botocore.exceptions import ClientError
from itertools import chain
from os import getenv
from sys import exit, stderr

_AWS_ACCESS_KEY_ID = getenv('AWS_ACCESS_KEY_ID')
_AWS_SECRET_ACCESS_KEY = getenv('AWS_SECRET_ACCESS_KEY')
_AWS_DEFAULT_REGION = getenv('AWS_DEFAULT_REGION')
_DEPLOYMENT_PREFIX = getenv('DEPLOYMENT_PREFIX')


class AWSCleaner(object):
    """Operations to purge/delete previously allocated AWS resources."""

    def __init__(self, tag):
        """Initialize object."""
        self.tag = tag

    def purge_sqs_queues(self):
        """Purge/Delete SQS queues.

        If tag was specified during object creation, then delete all queues tagged with this tag.
        Else purge (remove messages from) all _DEPLOYMENT_PREFIX_ prefixed queues.
        """
        client = boto3.client('sqs',
                              aws_access_key_id=_AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=_AWS_SECRET_ACCESS_KEY,
                              region_name=_AWS_DEFAULT_REGION)
        resource = boto3.resource('sqs',
                                  aws_access_key_id=_AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=_AWS_SECRET_ACCESS_KEY,
                                  region_name=_AWS_DEFAULT_REGION)

        if self.tag:
            print("About to delete SQS queues tagged with %r. "
                  "It'll take a while to go through all queues, stay tuned." % ','.join(self.tag))
            for queue in resource.queues.all():
                tags = client.list_queue_tags(QueueUrl=queue.url).get('Tags', {})
                if tags.get(self.tag[0]) == self.tag[1]:
                    print("Deleting", queue.url)
                    client.delete_queue(QueueUrl=queue.url)
        else:
            print("About to purge %r prefixed SQS queues." % _DEPLOYMENT_PREFIX)
            for queue in chain(
                    # Supply more than just _DEPLOYMENT_PREFIX to QueueNamePrefix
                    # to avoid purging wrong queues.
                    resource.queues.filter(QueueNamePrefix=_DEPLOYMENT_PREFIX + '_api_'),
                    resource.queues.filter(QueueNamePrefix=_DEPLOYMENT_PREFIX + '_ingestion_'),
                    resource.queues.filter(QueueNamePrefix=_DEPLOYMENT_PREFIX + '_priority_'),
                    resource.queues.filter(QueueNamePrefix=_DEPLOYMENT_PREFIX + '_livenessFlow_')):
                print("Deleting messages from", queue.url)
                client.purge_queue(QueueUrl=queue.url)

    def purge_s3_buckets(self):
        """Purge/Delete S3 buckets.

        If tag was specified during object creating, then delete all buckets tagged with this tag.
        Else purge (remove objects from) all _DEPLOYMENT_PREFIX_ prefixed buckets.
        """
        s3 = boto3.resource('s3',
                            aws_access_key_id=_AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=_AWS_SECRET_ACCESS_KEY,
                            region_name=_AWS_DEFAULT_REGION)
        if self.tag:
            print("About to delete S3 buckets tagged with %r." % ','.join(self.tag))
        else:
            print("About to purge %r prefixed S3 buckets." % _DEPLOYMENT_PREFIX)

        for bucket in s3.buckets.all():
            match = False
            if self.tag:
                try:
                    # bucket is either tagged with tag argument
                    match = {'Key': self.tag[0], 'Value': self.tag[1]} in \
                            s3.BucketTagging(bucket.name).tag_set
                except ClientError:
                    pass
            # or name is _DEPLOYMENT_PREFIX prefixed
            elif bucket.name.startswith(_DEPLOYMENT_PREFIX + '-bayesian-core-'):
                match = True

            if match:
                print("Deleting", bucket) if self.tag else print("Deleting objects from", bucket)
                bucket.object_versions.delete()
                bucket.objects.delete()
                if self.tag:
                    # All objects (including all object versions and Delete Markers) in the bucket
                    # must be deleted before the bucket itself can be deleted.
                    bucket.delete()

    def delete_dynamodb_tables(self):
        """Purge/Delete DynamoDB tables.

        If tag was specified during object creating, then delete all tables tagged with this tag.
        Else delete all _DEPLOYMENT_PREFIX_ prefixed tables.
        """
        client = boto3.client('dynamodb',
                              aws_access_key_id=_AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=_AWS_SECRET_ACCESS_KEY,
                              region_name=_AWS_DEFAULT_REGION)
        resource = boto3.resource('dynamodb',
                                  aws_access_key_id=_AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=_AWS_SECRET_ACCESS_KEY,
                                  region_name=_AWS_DEFAULT_REGION)

        if self.tag:
            print("About to delete DynamoDB tables tagged with %r." % ','.join(self.tag))
        else:
            print("About to delete %r prefixed DynamoDB tables." % _DEPLOYMENT_PREFIX)

        for table in resource.tables.all():
            match = False
            if self.tag:
                # table is either tagged with tag argument
                match = {'Key': self.tag[0], 'Value': self.tag[1]} in\
                        client.list_tags_of_resource(ResourceArn=table.table_arn).get('Tags', [])
            # or table name is _DEPLOYMENT_PREFIX prefixed
            elif table.name.startswith(_DEPLOYMENT_PREFIX + '_'):
                match = True

            if match:
                # There's no 'purge' operation, so just delete the table in any case.
                print("Deleting", table)
                table.delete()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--force",
                        help="Allow to purge/delete resources tagged/prefixed with prod or stage")
    parser.add_argument("-t", "--tag",
                        help="Delete resources tagged with this 'key,value' tag")
    args = parser.parse_args()

    if not all(_AWS_ACCESS_KEY_ID and _AWS_SECRET_ACCESS_KEY and _AWS_DEFAULT_REGION and
               _DEPLOYMENT_PREFIX):
        print("Not all environment variables are properly defined.", file=stderr)
        exit(1)

    if args.tag:
        try:
            k, v = args.tag.split(',')
            args.tag = (k, v)
        except ValueError:
            print("Tag needs to be 'key,value'", file=stderr)
            exit(1)
        print("About to delete resources tagged with %r" % ','.join(args.tag))
    else:
        print("About to purge %r prefixed resources." % _DEPLOYMENT_PREFIX)

    if args.tag and args.tag[1].lower() in {'prod', 'stage'}:
        prod_stage = args.tag[1]
    elif _DEPLOYMENT_PREFIX.lower() in {'prod', 'stage'}:
        prod_stage = _DEPLOYMENT_PREFIX
    else:
        prod_stage = False
    if prod_stage and not args.force:
        print("If you really want to destroy %s use -f/--force." % prod_stage, file=stderr)
        exit(0)

    aws_cleaner = AWSCleaner(args.tag)
    aws_cleaner.purge_sqs_queues()
    aws_cleaner.purge_s3_buckets()
    aws_cleaner.delete_dynamodb_tables()
