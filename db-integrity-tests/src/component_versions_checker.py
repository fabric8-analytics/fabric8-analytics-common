"""Checker for JSON files stored for component versions in core-data bucket."""

from checker import Checker
from botocore.exceptions import ClientError


class ComponentVersionsChecker(Checker):
    """Checker for JSON files stored for component versions in core-data bucket."""

    BUCKET_NAME = "bayesian-core-data"

    def __init__(self, s3interface, ecosystem, package_name):
        """Initialize the core package checker."""
        self.s3interface = s3interface
        self.ecosystem = ecosystem
        self.package_name = package_name

    def read_metadata(self, metadata_key):
        """Read JSON metadata for the given key."""
        key = self.s3interface.package_analysis_key(self.ecosystem, self.package_name, metadata_key)
        return self.s3interface.read_object(ComponentVersionsChecker.BUCKET_NAME, key)

    def read_metadata_list(self):
        """Read list of all metadata for given E+P."""
        try:
            jsons = self.s3interface.read_object_list(ComponentVersionsChecker.BUCKET_NAME,
                                                      self.ecosystem, self.package_name,
                                                      update_names=False, remove_prefix=True)
            return jsons
        except ClientError as e:
            return "S3-related error"
        except Exception as e:
            return str(e)

    @staticmethod
    def get_directories(metadata_list):
        """Get set of directories for the list of all metadata for given E+P."""
        seq = [metadata[:metadata.find("/")] for metadata in metadata_list
               if metadata.find("/") != -1]
        return set(seq)

    @staticmethod
    def get_version_jsons(metadata_list):
        """Get set of versions for the list of all metadata for given E+P."""
        seq = [metadata[:-len(".json")] for metadata in metadata_list
               if metadata.find("/") == -1 and metadata.endswith(".json")]
        return set(seq)

    def read_versions(self):
        """Read versions and also list of directories and all JSONs."""
        metadata_list = self.read_metadata_list()

        # set of directories, hopefully one directory per version
        directories = ComponentVersionsChecker.get_directories(metadata_list)

        # set of files $VERSION.json
        version_jsons = ComponentVersionsChecker.get_version_jsons(metadata_list)

        # ideally the following property should be true: directories=versions_json
        # so the union will be the same
        versions = directories | version_jsons
        return directories, version_jsons, versions, metadata_list
