#!/usr/bin/python3

"""Operations to purge/delete previously allocated AWS resources."""

import boto3
from os import getenv
from sys import exit

_AWS_ACCESS_KEY_ID = getenv('AWS_ACCESS_KEY_ID')
_AWS_SECRET_ACCESS_KEY = getenv('AWS_SECRET_ACCESS_KEY')
_AWS_DEFAULT_REGION = getenv('AWS_DEFAULT_REGION')
_DEPLOYMENT_PREFIX = getenv('DEPLOYMENT_PREFIX')


class AWSCleaner(object):
    """Operations to purge/delete previously allocated AWS resources."""

    @staticmethod
    def purge_sqs_queues():
        """Remove messages in _DEPLOYMENT_PREFIX_[ingestion|api]_ prefixed queues."""
        client = boto3.client('sqs',
                              aws_access_key_id=_AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=_AWS_SECRET_ACCESS_KEY,
                              region_name=_AWS_DEFAULT_REGION)

        # Supply more than just _DEPLOYMENT_PREFIX to QueueNamePrefix to avoid purging wrong queues.
        queues_urls = \
            client.list_queues(QueueNamePrefix=_DEPLOYMENT_PREFIX + '_ingestion_').get('QueueUrls',
                                                                                       []) +\
            client.list_queues(QueueNamePrefix=_DEPLOYMENT_PREFIX + '_api_').get('QueueUrls', [])

        for qurl in queues_urls:
            print("Purging ", qurl)
            client.purge_queue(QueueUrl=qurl)
            # client.delete_queue(QueueUrl=qurl)

    @staticmethod
    def purge_s3_buckets():
        """Remove objects (and versions) in _DEPLOYMENT_PREFIX-bayesian-core- prefixed buckets."""
        s3 = boto3.resource('s3',
                            aws_access_key_id=_AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=_AWS_SECRET_ACCESS_KEY,
                            region_name=_AWS_DEFAULT_REGION)

        for bucket in s3.buckets.all():
            if bucket.name.startswith(_DEPLOYMENT_PREFIX + '-bayesian-core-'):
                print("Purging ", bucket)
                bucket.object_versions.delete()
                bucket.objects.delete()
                # All objects (including all object versions and Delete Markers) in the bucket
                # must be deleted before the bucket itself can be deleted.
                # bucket.delete()

    @staticmethod
    def delete_dynamodb_tables():
        """Delete _DEPLOYMENT_PREFIX_ prefixed tables."""
        dynamodb = boto3.resource('dynamodb',
                                  aws_access_key_id=_AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=_AWS_SECRET_ACCESS_KEY,
                                  region_name=_AWS_DEFAULT_REGION)

        for table in dynamodb.tables.all():
            if table.name.startswith(_DEPLOYMENT_PREFIX + '_'):
                # There's no 'purge' operation, so just delete the table.
                print("Deleting ", table)
                table.delete()


if __name__ == '__main__':
    if not all(_AWS_ACCESS_KEY_ID and _AWS_SECRET_ACCESS_KEY and _AWS_DEFAULT_REGION and
               _DEPLOYMENT_PREFIX):
        print("Not all environment variables are properly defined")
        exit(1)

    AWSCleaner.purge_sqs_queues()
    AWSCleaner.purge_s3_buckets()
    AWSCleaner.delete_dynamodb_tables()
