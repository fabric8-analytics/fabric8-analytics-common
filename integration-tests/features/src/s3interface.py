"""AWS S3 Interface used by tests."""
import boto3
import botocore
from botocore.exceptions import ClientError
import json
import os


class S3Interface():
    """Interface to the AWS S3 database."""

    def __init__(self, aws_access_key_id, aws_secret_access_key, s3_region_name,
                 deployment_prefix):
        """Create a new interface to the AWS S3.

        Remember the access key, secret access key, region, and deployment
        prefix that will be used later to connect to the AWS S3.
        """
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.s3_region_name = s3_region_name
        self.deployment_prefix = deployment_prefix

        # to be set up by the connect() method
        self.s3_resource = None
        self.s3_session = None

    def check_connection_parameters(self):
        """Check all parameters needed to connect to S3."""
        assert self.aws_access_key_id is not None
        assert self.aws_secret_access_key is not None
        assert self.s3_region_name is not None

    def connect(self):
        """Connect to the AWS S3 database."""
        self.check_connection_parameters()

        # we are already connected -> let's use this connection
        if self.s3_resource is not None:
            return

        # create the session used to communicate with the S3 database
        # and check if the operation was successful
        self.s3_session = boto3.session.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.s3_region_name)

        assert self.s3_session is not None

        use_ssl = True
        endpoint_url = None

        # retrieve the bucket resource and check if the operation was successful
        self.s3_resource = self.s3_session.resource(
            's3',
            config=botocore.client.Config(signature_version='s3v4'),
            use_ssl=use_ssl, endpoint_url=endpoint_url)

        assert self.s3_resource is not None

    def read_all_buckets(self):
        """Read all available buckets from the AWS S3 database."""
        return self.s3_resource.buckets.all()

    def full_bucket_name(self, bucket_name):
        """Insert deployment prefix to the given bucket name."""
        return "{p}-{b}".format(p=self.deployment_prefix, b=bucket_name)

    @staticmethod
    def package_key(ecosystem, package):
        """Construct a key to the selected package in the given ecosystem."""
        return "{ecosystem}/{package}.json".format(ecosystem=ecosystem,
                                                   package=package)

    @staticmethod
    def package_analysis_key(ecosystem, package, metadata):
        """Construct a key to the selected package analysis in the given ecosystem."""
        return "{ecosystem}/{package}/{metadata}.json".format(ecosystem=ecosystem,
                                                              package=package,
                                                              metadata=metadata)

    @staticmethod
    def component_key(ecosystem, package, version):
        """Construct a key to the selected component in the given ecosystem."""
        return "{ecosystem}/{package}/{version}.json".format(ecosystem=ecosystem,
                                                             package=package,
                                                             version=version)

    @staticmethod
    def component_analysis_key(ecosystem, package, version, analysis):
        """Construct a key to the selected component analysis in the given ecosystem."""
        return "{ecosystem}/{package}/{version}/{analysis}.json".format(ecosystem=ecosystem,
                                                                        package=package,
                                                                        version=version,
                                                                        analysis=analysis)

    @staticmethod
    def component_core_package_data_key(ecosystem, package):
        """Construct a key to the selected package in the given ecosystem."""
        return "{ecosystem}/{package}.json".format(ecosystem=ecosystem,
                                                   package=package)

    @staticmethod
    def component_core_package_data_analysis_key(ecosystem, package, analysis):
        """Construct a key to the selected package analysis in the given ecosystem."""
        return "{ecosystem}/{package}/{analysis}.json".format(ecosystem=ecosystem,
                                                              package=package,
                                                              analysis=analysis)

    def does_bucket_exist(self, bucket_name):
        """Check if the given bucket exists in the S3 database.

        Return True only when bucket with given name exist and can be read
        by current AWS S3 database user.
        """
        try:
            s3 = self.s3_resource
            assert s3 is not None
            s3.meta.client.head_bucket(Bucket=self.full_bucket_name(bucket_name))
            return True
        except ClientError:
            return False

    def read_object(self, bucket_name, key):
        """Read byte stream from the S3 database, decode it into string, and parse as JSON."""
        s3 = self.s3_resource
        assert s3 is not None
        data = s3.Object(self.full_bucket_name(bucket_name), key).get()['Body'].read().decode()
        return json.loads(data)

    def read_object_metadata(self, bucket_name, key, attribute):
        """Read byte stream from the S3 database, decode it into string, and parse as JSON."""
        s3 = self.s3_resource
        assert s3 is not None
        data = s3.Object(self.full_bucket_name(bucket_name), key).get()[attribute]
        return data

    @staticmethod
    def selector_to_key(selector):
        """Construct a key from given selector (that is written in tests w/o underscores)."""
        return selector.lower().replace(" ", "_")

    def get_object_from_s3(self, bucket_name):
        """Download Manifest Files from S3."""
        self.connect()
        s3 = self.s3_resource
        files_to_download = ['package.json', 'pom.xml', 'pylist.json']
        path = 'data/dynamic_manifests/'
        if not os.path.exists(path):
            os.makedirs(path)

        for obj in files_to_download:
            key = "dynamic_manifests/" + obj
            try:
                s3.Bucket(bucket_name).download_file(key, path + obj)
            except botocore.exceptions.ClientError as e:
                print("The object does not exist.")
                return 'error in file fetching from s3', 400
        return 'success', 200
