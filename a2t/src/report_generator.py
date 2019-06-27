"""Report generator from A2T.

Copyright (c) 2019 Red Hat Inc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import csv
import os
import sys
import platform


def export_header(csv_writer):
    """Export CSV header."""
    csv_writer.writerow(["#",
                         "Test name", "Method",
                         "Ecosystem", "Package", "Version",
                         "Manifest",
                         "Thread#", "Status code",
                         "Analysis results",
                         "Start time", "End time", "Duration"])


def export_environment_info(csv_writer):
    """Export basic information about test environment."""
    csv_writer.writerow(["System family", os.name])
    csv_writer.writerow(["System", platform.system()])
    csv_writer.writerow(["Version", platform.release()])
    csv_writer.writerow(["Python", "{}.{}".format(sys.version_info.major, sys.version_info.minor)])
    csv_writer.writerow(["Path to interpret", sys.executable])


def export_test_setup(csv_writer, test):
    """Export information about test setup."""
    csv_writer.writerow(["Name", "Component analysis", "Stack analysis",
                         "Python payload", "Maven payload", "NPM payload",
                         "Improper payload", "Mix payloads",
                         "Check responses", "Export responses", "Comment"])
    csv_writer.writerow([test["Name"], test["Component analysis"], test["Stack analysis"],
                         test["Python payload"], test["Maven payload"], test["NPM payload"],
                         test["Improper payload"], test["Mix payloads"],
                         test["Check responses"], test["Export responses"], test["Comment"]])


def export_test_results(csv_writer, results):
    """Export results for all tests/API calls."""
    for i in range(results.qsize()):
        result = results.get()
        csv_writer.writerow([i + 1,
                             result["name"], result["method"],
                             result["ecosystem"], result["package"], result["version"],
                             result["manifest"],
                             result["thread_id"],
                             result["status_code"],
                             result["analysis"],
                             result["started"], result["finished"], result["duration"]])


def export_totat_time(csv_writer, start, end, duration):
    """Export informations about total time."""
    csv_writer.writerow(["Start time", start])
    csv_writer.writerow(["End time", end])
    csv_writer.writerow(["Duration", duration])


def generate_csv_report(results, test, start, end, duration, filename):
    """Generate CSV report with all A2T tests."""
    with open(filename, 'w', encoding='utf8') as fout:
        csv_writer = csv.writer(fout)
        export_environment_info(csv_writer)
        csv_writer.writerow([])
        export_test_setup(csv_writer, test)
        csv_writer.writerow([])
        export_totat_time(csv_writer, start, end, duration)
        csv_writer.writerow([])
        export_header(csv_writer)
        export_test_results(csv_writer, results)
