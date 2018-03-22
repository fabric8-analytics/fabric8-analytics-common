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

    def csv_header(self):
        """Write the header row."""
        self.writer.writerow(["Ecosystem", "Package", "In core-packages?", "In packages?",
                              "Core: package.json", "Core: github_details",
                              "Core: keywords_tagging", "Core: libraries_io", "Core: Leftovers"])

    def package_info(self, ecosystem, package_name, in_core_packages, in_packages,
                     core_package_json, core_package_github_details, core_package_keywords_tagging,
                     core_package_libraries_io, core_leftovers):
        """Write the record with package data."""
        self.writer.writerow([ecosystem, package_name, int(in_core_packages), int(in_packages),
                              core_package_json, core_package_github_details,
                              core_package_keywords_tagging, core_package_libraries_io,
                              core_leftovers])
