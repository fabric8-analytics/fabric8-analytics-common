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
            self.check_attribute_presence(data, "id")
            self.check_attribute_presence(data, "package_id")
            self.check_attribute_presence(data, "started_at")
            self.check_attribute_presence(data, "finished_at")
            assert data, "N/A"
            return "OK"
        except Exception as e:
            return str(e)

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
            self.check_release_attribute(data)
            self.check_status_attribute(data)

            self.check_attribute_presence(data, "summary")
            self.check_attribute_presence(data, "details")

            self.check_schema_attribute(data, "github_details",
                                        CorePackageChecker.GITHUB_DETAILS_SCHEMA_VERSION)
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
            self.check_release_attribute(data)
            self.check_status_attribute(data)

            details = self.get_details_node(data)
            self.check_attribute_presence(details, "package_name")
            self.check_attribute_presence(details, "repository_description")
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
            self.check_release_attribute(data)
            self.check_status_attribute(data)
            return "OK"
        except ClientError as e:
            return "N/A"
        except Exception as e:
            return str(e)

    def check_git_stats(self):
        """Check the content of package metadata taken from git_stats.json."""
        try:
            data = self.read_metadata("git_stats")
            assert data, "N/A"
            self.check_audit_metadata(data)
            self.check_release_attribute(data)
            self.check_status_attribute(data)
            details = self.get_details_node(data)
            self.check_attribute_presence(details, "master")
            return "OK"
        except ClientError as e:
            return "N/A"
        except Exception as e:
            return str(e)

    def check_leftovers(self):
        """Check for any leftovers in the S3 database."""
        try:
            jsons = self.s3interface.read_object_list(CorePackageChecker.BUCKET_NAME,
                                                      self.ecosystem, self.package_name)
            jsons = set(jsons)

            # remove the 'main' JSON file
            package_json = "{p}.json".format(p=self.package_name)
            jsons.remove(package_json)

            expected = {'github_details.json', 'keywords_tagging.json', 'git_stats.json',
                        'libraries_io.json'}

            leftovers = jsons - expected
            assert not leftovers, ",".join(leftovers)
            return "none"
        except ClientError as e:
            return "S3-related error"
        except Exception as e:
            return str(e)
