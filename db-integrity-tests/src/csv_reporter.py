"""CSV reporter for package metadata and statuses."""

import csv


class CSVReporter:
    """CSV reporter for package metadata and statuses."""

    def __init__(self, filename):
        """Initialize the class, register the filename to be generated."""
        self.filename = filename

    def __enter__(self):
        """Initialize the CSV writer."""
        self.fout = open(self.filename, "w")
        self.writer = csv.writer(self.fout)
        return self

    def __exit__(self, type, value, traceback):
        """Close the CSV writer."""
        if self.fout:
            self.fout.close()

    def csv_header_for_core_packages(self):
        """Write the header row."""
        self.writer.writerow(["Ecosystem", "Package", "In core-packages?", "In packages?",
                              "package.json", "github_details",
                              "keywords_tagging", "libraries_io", "Leftovers"])

    def core_package_info(self, ecosystem, package_name, in_core_packages, in_packages,
                          core_package_json, core_package_github_details,
                          core_package_keywords_tagging, core_package_libraries_io, core_leftovers):
        """Write the record with package data."""
        self.writer.writerow([ecosystem, package_name, int(in_core_packages), int(in_packages),
                              core_package_json, core_package_github_details,
                              core_package_keywords_tagging, core_package_libraries_io,
                              core_leftovers])

    def csv_header_for_package_version(self):
        """Write the header row."""
        self.writer.writerow(["Ecosystem", "Package", "Version", "Base JSON", "Subdir"])

    def package_version_info(self, ecosystem, package_name, version, base_json, subdir):
        """Write the record with E+P+V data."""
        self.writer.writerow([ecosystem, package_name, version, int(base_json), int(subdir)])
