"""Test coverage parsing and computing."""

import re
import requests
from progress_bar import *
from jacoco_to_codecov import *
from fastlog import log


# default code coverage threshold used when no threshold is specified
# in the configuration file
CODE_COVERAGE_THRESHOLD = 90


def unit_test_coverage_ok(unit_test_coverage, code_coverage_threshold=CODE_COVERAGE_THRESHOLD):
    """Return True only if unit test coverage is above given threshold."""
    if unit_test_coverage is not None:
        # check the code coverage against the specified threshold
        return int(unit_test_coverage["coverage"]) >= code_coverage_threshold
    else:
        return False


def log_coverage(statements, missed, coverage):
    """Log info about the coverage read from reports."""
    with log.indent():
        log.info("statements {s}".format(s=statements))
        log.info("missed     {m}".format(m=missed))
        log.info("coverage   {c}".format(c=coverage))


def parse_unit_test_statistic(line):
    """Parse the line containing unit test coverage statistic."""
    pattern = re.compile(r'TOTAL\s+(\d+)\s+(\d+)\s+(\d+)%')
    match = pattern.match(line)
    if len(match.groups()) == 3:
        coverage = match.group(3)
        statements = match.group(1)
        missed = match.group(2)
        log_coverage(statements, missed, coverage)
        return {"statements": statements,
                "missed": missed,
                "coverage": coverage,
                "progress_bar_class": progress_bar_class(coverage),
                "progress_bar_width": progress_bar_width(coverage)}
    else:
        return None


def compute_jacoco_test_statistic(project_coverage_report):
    """Compute test coverage etc. from the CSV data exported from JaCoCo and converted."""
    java_classes = project_coverage_report.read_java_classes()
    statements, missed, coverage = ProjectCoverageReport.compute_total(java_classes)
    log_coverage(statements, missed, coverage)

    return {"statements": statements,
            "missed": missed,
            "coverage": int(coverage),
            "progress_bar_class": progress_bar_class(coverage),
            "progress_bar_width": progress_bar_width(coverage)}


def write_unit_test_coverage(unit_test_output, repository):
    """Write the test coverage to new file in text format."""
    filename = repository + ".coverage.txt"
    with open(filename, "w") as fout:
        for line in unit_test_output:
            fout.write("%s\n" % line)


def write_unit_test_coverage_as_csv(unit_test_output, repository):
    """Write the test coverage to new file in CSV format."""
    filename = repository + ".coverage.csv"
    with open(filename, "w") as fout:
        for line in unit_test_output:
            fout.write("%s\n" % line)


def line_with_jacoco_test_header(line):
    """Check if the given string represents JaCoCo unit test header."""
    return line == "Code coverage report BEGIN"


def line_with_jacoco_test_footer(line, report_type):
    """Check if the given string represents JaCoCo unit test footer."""
    return report_type == "jacoco" and line == "Code coverage report END"


def line_with_unit_test_header(line):
    """Check if the given string represents unit test header."""
    return line.startswith("Name  ") and line.endswith("Stmts   Miss  Cover   Missing")


def line_with_unit_test_summary(line, report_type="pycov"):
    """Check if the given string represents unit test summary."""
    return report_type == "pycov" and line.startswith("TOTAL      ") and line.endswith("%")


def log_report_type(report_type):
    """Display info which unit test report type has been detected."""
    with log.indent():
        log.info("{report_type} report detected".format(report_type=report_type))


def read_unit_test_coverage(ci_jobs, jenkins_url, repository):
    """Read and process unit test coverage."""
    log.info("Reading unit test coverage")
    url = ci_jobs.get_console_output_url(repository)
    report_type = None
    if url is not None:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text.split("\n")
            unit_test_output = []
            for line in content:
                line = line.strip()
                # check where the test coverage begins
                if line_with_unit_test_header(line):
                    log_report_type("pycov")
                    report_type = "pycov"
                    unit_test_output.append(line)
                elif line_with_jacoco_test_header(line):
                    log_report_type("jacoco")
                    report_type = "jacoco"
                    # not needed to write the header
                    # unit_test_output.append(line)
                # check where the test coverage ends
                elif line_with_unit_test_summary(line, report_type):
                    unit_test_output.append(line)
                    write_unit_test_coverage(unit_test_output, repository)
                    return parse_unit_test_statistic(line)
                # check where the test coverage ends
                elif line_with_jacoco_test_footer(line, report_type):
                    # not needed to write the footer
                    # unit_test_output.append(line)
                    write_unit_test_coverage_as_csv(unit_test_output, repository)
                    p = ProjectCoverageReport(repository + ".coverage.csv")
                    p.convert_code_coverage_report(repository + ".coverage.txt")
                    return compute_jacoco_test_statistic(p)
                # now we know we have something to report
                elif report_type:
                    unit_test_output.append(line)
    log.warning("No coverage report found")
    return None


def read_unit_test_coverage_for_week(repository, week):
    """Read and process unit test coverage."""
    filename = "{repository}.coverage.{week}.txt".format(repository=repository, week=week)
    try:
        with open(filename, "r") as fin:
            content = fin.readlines()
            for line in content:
                line = line.strip()
                if line_with_unit_test_summary(line):
                    return parse_unit_test_statistic(line)
    except Exception as e:
        return None
