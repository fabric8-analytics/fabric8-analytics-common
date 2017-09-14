import boto3
import botocore
import json


class S3Interface():

    def __init__(self, aws_access_key_id, aws_secret_access_key, s3_region_name,
                 deployment_prefix):
        assert aws_access_key_id is not None
        assert aws_secret_access_key is not None
        assert s3_region_name is not None

        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.s3_region_name = s3_region_name
        self.deployment_prefix = deployment_prefix

        self.s3_resource = None
        self.s3_session = None

    def connect(self):
        if self.s3_resource is not None:
            return

        self.s3_session = boto3.session.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.s3_region_name)

        assert self.s3_session is not None

        use_ssl = True
        endpoint_url = None

        self.s3_resource = self.s3_session.resource(
            's3',
            config=botocore.client.Config(signature_version='s3v4'),
            use_ssl=use_ssl, endpoint_url=endpoint_url)

        assert self.s3_resource is not None

    def read_all_buckets(self):
        return self.s3_resource.buckets.all()

    def full_bucket_name(self, bucket_name):
        return "{p}-{b}".format(p=self.deployment_prefix, b=bucket_name)

    def component_key(self, ecosystem, package, version):
        return "{ecosystem}/{package}/{version}.json".format(ecosystem=ecosystem,
                                                             package=package,
                                                             version=version)

    def component_analysis_key(self, ecosystem, package, version, analysis):
        return "{ecosystem}/{package}/{version}/{analysis}.json".format(ecosystem=ecosystem,
                                                                        package=package,
                                                                        version=version,
                                                                        analysis=analysis)

    def component_core_package_data_key(self, ecosystem, package, version, analysis):
        return "{ecosystem}/{package}/{analysis}.json".format(ecosystem=ecosystem,
                                                              package=package,
                                                              version=version,
                                                              analysis=analysis)

    def does_bucket_exist(self, bucket_name):
        '''Return True only when bucket with given name exist and can be read
        by current AWS S3 database user.'''
        try:
            s3 = self.s3_resource
            assert s3 is not None
            s3.meta.client.head_bucket(Bucket=self.full_bucket_name(bucket_name))
            return True
        except ClientError:
            return False

    def read_object(self, bucket_name, key):
        '''Read byte stream from S3, decode it into string, and parse as JSON.'''
        s3 = self.s3_resource
        assert s3 is not None
        data = s3.Object(self.full_bucket_name(bucket_name), key).get()['Body'].read().decode()
        return json.loads(data)

    def read_object_metadata(self, bucket_name, key, attribute):
        '''Read byte stream from S3, decode it into string, and parse as JSON.'''
        s3 = self.s3_resource
        assert s3 is not None
        data = s3.Object(self.full_bucket_name(bucket_name), key).get()[attribute]
        return data
