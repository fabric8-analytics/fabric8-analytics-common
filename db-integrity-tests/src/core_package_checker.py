"""Checker for JSON files stored for the whole packages in core-package-data bucket."""

from checker import Checker
from botocore.exceptions import ClientError


class CorePackageChecker(Checker):
    """Checker for JSON files stored for the whole packages in core-package-data bucket."""

    BUCKET_NAME = "bayesian-core-package-data"
    GITHUB_DETAILS_SCHEMA_VERSION = "2-0-1"

    def __init__(self, s3interface, ecosystem, package_name):
        """Initialize the core package checker."""
        self.s3interface = s3interface
        self.ecosystem = ecosystem
        self.package_name = package_name

    def read_metadata(self, metadata_key):
        """Read JSON metadata for the given key."""
        key = self.s3interface.package_analysis_key(self.ecosystem, self.package_name, metadata_key)
        return self.s3interface.read_object(CorePackageChecker.BUCKET_NAME, key)

    def check_core_json(self):
        """Check the content of package toplevel file."""
        key = self.s3interface.package_key(self.ecosystem, self.package_name)
        try:
            data = self.s3interface.read_object(CorePackageChecker.BUCKET_NAME, key)
            assert data, "N/A"
            return "OK"
        except Exception as e:
            return str(e)

    @staticmethod
    def release_string(ecosystem, package, version=None):
        """Construct a string with ecosystem:package or ecosystem:package:version tuple."""
        return "{e}:{p}:{v}".format(e=ecosystem, p=package, v=version)

    def check_release_attribute(self, data, version=None):
        """Check the content of _release attribute.

        Check that the attribute _release contains proper release string for given ecosystem
        and package.
        """
        self.check_attribute_presence(data, "_release")
        assert data["_release"] == self.release_string(self.ecosystem, self.package_name, version)

    def check_github_details(self):
        """Check all relevant attributes stored in the JSON with GitHub details."""
        try:
            data = self.read_metadata("github_details")
            assert data, "N/A"
            self.check_audit_metadata(data)
            return "OK"
        except ClientError as e:
            return "N/A"
        except Exception as e:
            return str(e)

    def check_keywords_tagging(self):
        """Check all relevant attributes stored in the JSON with keywods tagging."""
        try:
            data = self.read_metadata("keywords_tagging")
            assert data, "N/A"
            self.check_audit_metadata(data)
            return "OK"
        except ClientError as e:
            return "N/A"
        except Exception as e:
            return str(e)

    def check_libraries_io(self):
        """Check the content of package metadata taken from libaries.io."""
        try:
            data = self.read_metadata("libraries_io")
            assert data, "N/A"
            self.check_audit_metadata(data)
            return "OK"
        except ClientError as e:
            return "N/A"
        except Exception as e:
            return str(e)
