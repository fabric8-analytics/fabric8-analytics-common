"""AWS S3 Interface used by tests."""

import boto3
import botocore
from botocore.exceptions import ClientError
import json

from s3configuration import S3Configuration


class S3Interface():
    """Interface to the AWS S3 database."""

    def __init__(self, s3configuration):
        """Create a new interface to the AWS S3.

        Remember the access key, secret access key, region, and deployment
        prefix that will be used later to connect to the AWS S3.
        """
        self.s3_configuration = s3configuration

        # to be set up by the connect() method
        self.s3_resource = None
        self.s3_session = None

    def connect(self):
        """Connect to the AWS S3 database."""
        # we are already connected -> let's use this connection
        if self.s3_resource is not None:
            return

        # create the session used to communicate with the S3 database
        # and check if the operation was successful
        self.s3_session = boto3.session.Session(
            aws_access_key_id=self.s3_configuration.access_key_id,
            aws_secret_access_key=self.s3_configuration.secret_access_key,
            region_name=self.s3_configuration.region_name)

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

    def read_bucket_names(self):
        """Read names of all available buckets from the AWS S3 database."""
        buckets = self.read_all_buckets()
        return [bucket.name for bucket in buckets]

    def full_bucket_name(self, bucket_name):
        """Insert deployment prefix to the given bucket name."""
        return "{p}-{b}".format(p=self.deployment_prefix, b=bucket_name)

    @staticmethod
    def package_key(ecosystem, package):
        """Construct a key to the selected package in the given ecosystem."""
        return "{ecosystem}/{package}.json".format(ecosystem=ecosystem,
                                                   package=package)

    @staticmethod
    def package_key_to_metadata(ecosystem, package):
        """Construct a key to the selected package in the given ecosystem."""
        return "{ecosystem}/{package}".format(ecosystem=ecosystem, package=package)

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

    @property
    def deployment_prefix(self):
        """Get the deployment prefix set up during initialization of this class."""
        return self.s3_configuration.deployment_prefix

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

    def read_ecosystems_from_bucket(self, bucket_name):
        """Return list of all ecosystems from selected bucket."""
        bucket = self.s3_resource.Bucket(self.full_bucket_name(bucket_name))
        result = bucket.meta.client.list_objects(Bucket=bucket.name, Delimiter='/')
        names = [o.get('Prefix') for o in result.get('CommonPrefixes')]
        # remove the / at the end of object name
        return [name[:-1] for name in names]

    def read_ecosystems_from_core_package_data(self):
        """Return list of all ecosystems from core-package-data bucket."""
        return self.read_ecosystems_from_bucket("bayesian-core-package-data")

    def read_ecosystems_from_core_data(self):
        """Return list of all ecosystems from core-data bucket."""
        return self.read_ecosystems_from_bucket("bayesian-core-data")

    def read_packages_from_bucket_for_ecosystem(self, ecosystem, bucket_name):
        """Return list of all packages found for the selected ecosystem."""
        if not ecosystem.endswith("/"):
            ecosystem += "/"
        bucket = self.s3_resource.Bucket(self.full_bucket_name(bucket_name))

        # parameters to be passed to list_objects_v2 method
        kwargs = {'Bucket': bucket.name, 'Delimiter': '/', 'Prefix': ecosystem}

        package_names = []

        # the S3 interface supports and requires 'pagination', so we need
        # to get list of package names in a loop
        while True:
            result = bucket.meta.client.list_objects_v2(**kwargs)
            names = [o.get('Prefix') for o in result.get('CommonPrefixes')]
            # names are returned in format "ecosystem/package/"
            # -> we need to get only the package part
            package_names.extend([name[name.find("/") + 1: name.find("/", -1)] for name in names])
            # perform 'pagination', but only when results were truncated
            if not result.get("IsTruncated"):
                break
            # token used by S3 to remember when the next page should begin
            kwargs['ContinuationToken'] = result['NextContinuationToken']

        return package_names

    def read_core_packages_for_ecosystem(self, ecosystem):
        """Return list of all core packages for the selected ecosystem."""
        return self.read_packages_from_bucket_for_ecosystem(ecosystem, "bayesian-core-package-data")

    def read_packages_for_ecosystem(self, ecosystem):
        """Return list of all packages for the selected ecosystem."""
        return self.read_packages_from_bucket_for_ecosystem(ecosystem, "bayesian-core-data")

    def read_object_list(self, bucket_name, ecosystem, package):
        """Read list of objects (JSON files) stored for the given E+P."""
        bucket_name = self.full_bucket_name(bucket_name)
        prefix = S3Interface.package_key_to_metadata(ecosystem, package)
        bucket = self.s3_resource.Bucket(bucket_name)
        result = bucket.meta.client.list_objects_v2(Bucket=bucket.name, Prefix=prefix)
        contents = result["Contents"]
        json_files = [o["Key"] for o in contents]
        return [json_file[json_file.rfind("/") + 1:] for json_file in json_files]

    @staticmethod
    def selector_to_key(selector):
        """Construct a key from given selector (that is written in tests w/o underscores)."""
        return selector.lower().replace(" ", "_")
