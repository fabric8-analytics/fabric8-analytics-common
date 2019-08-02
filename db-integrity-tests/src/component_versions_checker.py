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

    @property
    def version(self):
        """Return the current value of the version property."""
        return self._version

    @version.setter
    def version(self, version):
        """Set the value of the version property."""
        self._version = version

    def check_release_attribute(self, data):
        """Check the content of _release attribute.

        Check that the attribute _release contains proper release string for given ecosystem
        and package.
        """
        self.check_attribute_presence(data, "_release")
        assert data["_release"] == self.release_string(self.ecosystem, self.package_name,
                                                       self._version)

    def read_core_metadata(self):
        """Read JSON metadata for the given key."""
        key = self.s3interface.component_key(self.ecosystem, self.package_name, self._version)
        return self.s3interface.read_object(ComponentVersionsChecker.BUCKET_NAME, key)

    def read_metadata(self, metadata_key):
        """Read JSON metadata for the given key."""
        key = self.s3interface.component_analysis_key(self.ecosystem, self.package_name,
                                                      self._version, metadata_key)
        return self.s3interface.read_object(ComponentVersionsChecker.BUCKET_NAME, key)

    def read_metadata_list(self):
        """Read list of all metadata for given E+P."""
        try:
            jsons = self.s3interface.read_object_list(ComponentVersionsChecker.BUCKET_NAME,
                                                      self.ecosystem, self.package_name,
                                                      update_names=False, remove_prefix=True)
            return jsons
        except ClientError:
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

    def check_data_exist(self, data):
        """Check that the given data exists."""
        assert data, "N/A"

    def compare_ecosystems(self, actual_ecosystem):
        """Compare two ecosystems: the setup ecosystem with the actual one."""
        assert self.ecosystem is not None, "Missing ecosystem to compare"
        assert actual_ecosystem is not None, "Missing ecosystem to compare"
        assert self.ecosystem == actual_ecosystem, "Ecosystem {e1} differs from expected " \
            "ecosystem {e2}".format(e1=actual_ecosystem, e2=self.ecosystem)

    def compare_packages(self, actual_package):
        """Compare two packages: the setup package with the actual one."""
        assert self.package_name is not None, "Missing package to compare"
        assert actual_package is not None, "Missing package to compare"
        assert self.package_name == actual_package, "Package {p1} differs from expected " \
            "package {p2}".format(p1=actual_package, p2=self.package_name)

    def compare_versions(self, actual_version):
        """Compare two versions: the setup version with the actual one."""
        assert self._version is not None, "Missing version to compare"
        assert actual_version is not None, "Missing version to compare"
        assert self._version == actual_version, "Version {v1} differs from expected " \
            "version {v2}".format(v1=actual_version, v2=self._version)

    def check_core_data(self):
        """Check the component core data read from the AWS S3 database.

        Expected format (with an example data):
            {
              "analyses": [
                "security_issues",
                "metadata",
                "keywords_tagging",
                "digests",
                "source_licenses",
                "dependency_snapshot"
              ],
              "audit": null,
              "dependents_count": -1,
              "ecosystem": "pypi",
              "finished_at": "2017-10-06T13:41:43.450021",
              "id": 1,
              "latest_version": "0.2.4",
              "package": "clojure_py",
              "package_info": {
                "dependents_count": -1,
                "relative_usage": "not used"
              },
              "release": "pypi:clojure_py:0.2.4",
              "started_at": "2017-10-06T13:39:30.134801",
              "subtasks": null,
              "version": "0.2.4"
            }
        """
        try:
            data = self.read_core_metadata()
            self.check_data_exist(data)
            started_at = self.check_and_get_attribute(data, "started_at")
            self.check_timestamp(started_at)

            finished_at = self.check_and_get_attribute(data, "finished_at")
            self.check_timestamp(finished_at)

            actual_ecosystem = self.check_and_get_attribute(data, "ecosystem")
            self.compare_ecosystems(self, actual_ecosystem)

            actual_package = self.check_and_get_attribute(data, "package")
            self.compare_packages(self, actual_package)

            actual_version = self.check_and_get_attribute(data, "version")
            self.compare_versions(self, actual_version)

            # the following attributes are expected to be presented for all component
            # toplevel metadata
            attributes_to_check = ["id", "analyses", "audit", "dependents_count", "latest_version",
                                   "package_info", "subtasks"]
            self.check_attributes_presence(data, attributes_to_check)

            return "OK"
        except ClientError:
            return "N/A"
        except Exception as e:
            return str(e)

    def check_code_metrics(self):
        """Check the content of package version metadata taken from core_metrics.json."""
        try:
            data = self.read_metadata("code_metrics")
            assert data, "N/A"
            self.check_audit_metadata(data)
            self.check_release_attribute(data)
            self.check_status_attribute(data)
            self.check_attributes_presence(data, ["details", "schema", "summary"])
            summary = data["summary"]
            self.check_attributes_presence(summary, ["blank_lines", "code_lines", "comment_lines",
                                                     "total_files", "total_lines"])
            details = data["details"]
            assert details
            #
            #
            # 'details': {   'languages': [   {   'blank_lines': 433,
            #                                    'code_lines': 2927,
            #                                    'comment_lines': 62,
            #                                    'files_count': 1,
            #                                    'language': 'Clojure'},
            #                                {   'blank_lines': 1771,
            #                                    'code_lines': 6679,
            #                                    'comment_lines': 1174,
            #                                    'files_count': 77,
            #                                    'language': 'Python',
            #
            return "OK"
        except ClientError:
            return "N/A"
        except Exception as e:
            return str(e)

    def check_dependency_snapshot(self):
        """Check the content of package version metadata taken from dependency_snapshot.json."""
        try:
            data = self.read_metadata("dependency_snapshot")
            assert data, "N/A"
            self.check_audit_metadata(data)
            self.check_release_attribute(data)
            self.check_status_attribute(data)
            self.check_schema_attribute(data, "dependency_snapshot", "1-0-0")
            self.check_attribute_presence(data, "summary")
            summary = data["summary"]
            self.check_attributes_presence(summary, ["dependency_counts", "errors"])
            dependency_counts = self.check_and_get_attribute(summary, "dependency_counts")
            runtime_count = self.check_and_get_attribute(dependency_counts, "runtime")
            assert int(runtime_count) >= 0
            return "OK"
        except ClientError:
            return "N/A"
        except Exception as e:
            return str(e)

    def check_digests(self):
        """Check the content of package version metadata taken from digests.json."""
        try:
            data = self.read_metadata("digests")
            assert data, "N/A"
            self.check_audit_metadata(data)
            self.check_release_attribute(data)
            self.check_status_attribute(data)
            self.check_schema_attribute(data, "digests", "1-0-0")
            self.check_attributes_presence(data, ["details", "summary"])
            details = self.check_and_get_attribute(data, "details")
            assert len(details) >= 0
            # TODO: list of maps
            return "OK"
        except ClientError:
            return "N/A"
        except Exception as e:
            return str(e)

    def check_keywords_tagging(self):
        """Check the content of package version metadata taken from keywords_tagging.json."""
        try:
            data = self.read_metadata("keywords_tagging")
            assert data, "N/A"
            self.check_audit_metadata(data)
            self.check_release_attribute(data)
            self.check_status_attribute(data)
            self.check_attributes_presence(data, ["details", "summary"])
            #  no schema to check (yet?)
            #  tracked here: https://github.com/openshiftio/openshift.io/issues/1074
            return "OK"
        except ClientError:
            return "N/A"
        except Exception as e:
            return str(e)

    def check_metadata(self):
        """Check the content of package version metadata taken from metadata.json."""
        try:
            data = self.read_metadata("metadata")
            self.check_data_exist(data)
            self.check_audit_metadata(data)
            self.check_release_attribute(data)
            self.check_status_attribute(data)
            self.check_attributes_presence(data, ["details", "summary", "schema"])
            self.check_schema_attribute(data, "metadata", "3-2-0")
            details = data["details"]
            assert details
            # TODO: list of maps
            return "OK"
        except ClientError:
            return "N/A"
        except Exception as e:
            return str(e)

    def check_security_issues(self):
        """Check the content of package version metadata taken from security_issues.json."""
        try:
            data = self.read_metadata("security_issues")
            self.check_data_exist(data)
            self.check_audit_metadata(data)
            self.check_release_attribute(data)
            self.check_status_attribute(data)
            self.check_schema_attribute(data, "security_issues", "3-0-1")
            self.check_attributes_presence(data, ["details", "summary", "schema"])
            details = data["details"]
            assert type(details) is list
            # TODO: list of maps
            summary = data["summary"]
            for cve in summary:
                self.check_cve_value(cve)
            return "OK"
        except ClientError:
            return "N/A"
        except Exception as e:
            return str(e)

    def check_source_licenses(self):
        """Check the content of package version metadata taken from source_licenses.json."""
        try:
            data = self.read_metadata("source_licenses")
            assert data, "N/A"
            self.check_audit_metadata(data)
            self.check_release_attribute(data)
            self.check_status_attribute(data)
            self.check_schema_attribute(data, "source_licenses", "3-0-0")
            self.check_attributes_presence(data, ["details", "summary", "schema"])
            return "OK"
        except ClientError:
            return "N/A"
        except Exception as e:
            return str(e)

    def check_leftovers(self, jsons):
        """Check for any leftovers in the S3 database."""
        try:
            jsons = [json[1 + json.find("/"):] for json in jsons]
            jsons = set(jsons)

            expected = {'security_issues.json', 'digests.json', 'metadata.json',
                        'dependency_snapshot.json', 'code_metrics.json', 'source_licenses.json',
                        'keywords_tagging.json'}

            leftovers = jsons - expected
            assert not leftovers, ",".join(leftovers)
            return "none"
        except ClientError:
            return "S3-related error"
        except Exception as e:
            return str(e)
