"""Test coverage parsing and computing."""

import re
import requests
from progress_bar import *


CODE_COVERAGE_THRESHOLD = 50


def unit_test_coverage_ok(unit_test_coverage):
    """Return True only if unit test coverage is above given threshold."""
    if unit_test_coverage is not None:
        return int(unit_test_coverage["coverage"]) > CODE_COVERAGE_THRESHOLD
    else:
        return False


def parse_unit_test_statistic(line):
    """Parse the line containing unit test coverage statistic."""
    pattern = re.compile('TOTAL\s+(\d+)\s+(\d+)\s+(\d+)%')
    match = pattern.match(line)
    if len(match.groups()) == 3:
        coverage = match.group(3)
        return {"statements": match.group(1),
                "missed": match.group(2),
                "coverage": coverage,
                "progress_bar_class": progress_bar_class(coverage),
                "progress_bar_width": progress_bar_width(coverage)}
    else:
        return None


def write_unit_test_coverage(unit_test_output, repository):
    """Write the test coverage to new file."""
    filename = repository + ".coverage.txt"
    with open(filename, "w") as fout:
        for line in unit_test_output:
            fout.write("%s\n" % line)


def read_unit_test_coverage(ci_jobs, jenkins_url, repository):
    """Read and process unit test coverage."""
    url = ci_jobs.get_console_output_url(repository)
    if url is not None:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text.split("\n")
            unit_test_output = []
            for line in content:
                line = line.strip()
                # check where the test coverage begins
                if line.startswith("Name  ") and line.endswith("Stmts   Miss  Cover   Missing"):
                    unit_test_output.append(line)
                # check where the test coverage ends
                elif line.startswith("TOTAL      ") and line.endswith("%"):
                    unit_test_output.append(line)
                    write_unit_test_coverage(unit_test_output, repository)
                    return parse_unit_test_statistic(line)
                elif unit_test_output:
                    unit_test_output.append(line)
    return None


def read_unit_test_coverage_for_week(repository, week):
    """Read and process unit test coverage."""
    filename = "{repository}.coverage.{week}.txt".format(repository=repository, week=week)
    try:
        with open(filename, "r") as fin:
            content = fin.readlines()
            for line in content:
                line = line.strip()
                if line.startswith("TOTAL      ") and line.endswith("%"):
                    return parse_unit_test_statistic(line)
    except Exception as e:
        return None
