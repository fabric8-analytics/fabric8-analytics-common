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
import time
from fastlog import log


def export_header(csv_writer):
    """Export CSV header."""
    csv_writer.writerow(["Test name", "Endpoint", "Method",
                         "Expected status", "Actual status",
                         "Start time", "End time", "Duration", "Payload"])


def export_test_results(csv_writer, results):
    """Export results for all tests/API calls."""
    for result in results.tests:
        test = result["Test"]
        status_code = str(result["Status code"]) or "N/A"
        payload = str(result["Payload"]) or "N/A"
        csv_writer.writerow([test["Name"], result["Url"], test["Method"],
                             test["Expected status"], status_code,
                             test["Start"], test["End"], test["Duration"],
                             payload])


def export_totat_time(csv_writer, start, end, duration):
    """Export informations about total time."""
    csv_writer.writerow(["Start time", start])
    csv_writer.writerow(["End time", end])
    csv_writer.writerow(["Duration", duration])


def generate_csv_report(results, start, end, duration, filename):
    """Generate CSV report with all A2T tests."""
    with open(filename, 'w', encoding='utf8') as fout:
        csv_writer = csv.writer(fout)
        export_totat_time(csv_writer, start, end, duration)
        csv_writer.writerow([])
        export_header(csv_writer)
        # export_test_results(csv_writer, results)
