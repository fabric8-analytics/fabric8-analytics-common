"""Utility functions to work with CSV files.

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


def read_csv_as_table(csv_input_file_name, skip_first_line=False):
    """Read the given CSV file, parse it, and return as list of lists."""
    output = []
    with open(csv_input_file_name, 'r') as fin:
        csv_content = csv.reader(fin, delimiter=',')
        if skip_first_line:
            next(csv_content, None)
        for row in csv_content:
            output.append(row)
    return output


def read_csv_as_dicts(csv_input_file_name):
    """Read the given CSV file, parse it, and return as list of dicts."""
    input_table = read_csv_as_table(csv_input_file_name, skip_first_line=False)

    # first line should contain headers
    header = input_table[0]
    # rest lines would contain actual data
    data = input_table[1:]

    output = []
    # process all lines with data
    for input_line in data:
        record = {}
        for i in range(len(header)):
            record[header[i]] = input_line[i]
        output.append(record)
    return output
