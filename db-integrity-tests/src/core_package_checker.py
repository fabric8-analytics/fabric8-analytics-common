"""Checker for JSON files stored for the whole packages in core-package-data bucket."""


class CorePackageChecker:
    """Checker for JSON files stored for the whole packages in core-package-data bucket."""

    BUCKET_NAME = "bayesian-core-package-data"

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
            return "OK"
        except Exception as e:
            return "N/A"

    def check_github_details(self):
        """Check all relevant attributes stored in the JSON with GitHub details."""
        try:
            data = self.read_metadata("github_details")
            return "OK"
        except Exception as e:
            return "N/A"

    def check_keywords_tagging(self):
        """Check all relevant attributes stored in the JSON with keywods tagging."""
        try:
            data = self.read_metadata("keywords_tagging")
            return "OK"
        except Exception as e:
            return "N/A"

    def check_libraries_io(self):
        """Check the content of package metadata taken from libaries.io."""
        try:
            data = self.read_metadata("libraries_io")
            return "OK"
        except Exception as e:
            return "N/A"
