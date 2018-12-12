"""Utility functions to work with CSV files."""

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
