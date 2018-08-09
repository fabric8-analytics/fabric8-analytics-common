"""Functions related to the interface to the AWS S3 database."""
from behave import then, when


@when('I connect to the AWS S3 database')
def connect_to_aws_s3(context):
    """Connect to the AWS S3.

    Try to connect to the AWS S3 database using the given access key,
    secret access key, and region name.
    """
    context.s3interface.connect()


@then('I should see {bucket} bucket')
def find_bucket_in_s3(context, bucket):
    """Check the bucket existence.

    Check if bucket with given name can be found and can be read by
    current AWS S3 database user.
    """
    assert context.s3interface.does_bucket_exist(bucket)
