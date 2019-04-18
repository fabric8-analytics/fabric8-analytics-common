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


def export_header(csv_writer):
    """Export CSV header."""
    csv_writer.writerow(["#",
                         "Test name", "Ecosystem", "Package", "Version",
                         "Thread#", "Status code",
                         "Start time", "End time", "Duration"])


def export_test_results(csv_writer, results):
    """Export results for all tests/API calls."""
    for i in range(results.qsize()):
        result = results.get()
        csv_writer.writerow([i + 1,
                             result["name"],
                             result["ecosystem"], result["package"], result["version"],
                             result["thread_id"],
                             result["status_code"],
                             result["started"], result["finished"], result["duration"]])


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
        export_test_results(csv_writer, results)
