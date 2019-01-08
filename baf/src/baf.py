"""The main module of the Bayesian API Fuzzer."""

import sys
from fastlog import log
from csv_reader import read_csv_as_dicts
from setup import setup
from cliargs import cli_parser

from fuzzer import run_test
from results import Results
from report_generator import generate_reports


VERSION_MAJOR = 1
VERSION_MINOR = 0


def run_all_loaded_tests(cfg, fuzzer_settings, tests, results):
    """Run all tests read from CSV file."""
    i = 1
    for test in tests:
        log.info("Starting test #{n} with name '{desc}'".format(n=i, desc=test["Name"]))
        with log.indent():
            run_test(cfg, fuzzer_settings, test, results)
        i += 1


def start_tests(cfg, fuzzer_settings, tests, results):
    """Start all tests using the already loaded configuration and fuzzer settings."""
    log.info("Run tests")
    with log.indent():
        if not tests or len(tests) == 0:
            log.error("No tests loaded!")
            sys.exit(-1)
        if len(tests) == 1:
            log.success("Loaded 1 test")
        else:
            log.success("Loaded {n} tests".format(n=len(tests)))
        run_all_loaded_tests(cfg, fuzzer_settings, tests, results)


def read_fuzzer_settings(filename):
    """Read fuzzer settings from the CSV file."""
    log.info("Read fuzzer settings")
    with log.indent():
        fuzzer_settings = read_csv_as_dicts(filename)
        if len(fuzzer_settings) == 1:
            log.success("Loaded 1 setting")
        else:
            log.success("Loaded {n} settings".format(n=len(fuzzer_settings)))
    return fuzzer_settings


def show_version():
    """Show BAF version."""
    print("BAF version {major}.{minor}".format(major=VERSION_MAJOR, minor=VERSION_MINOR))


def main():
    """Entry point to the Bayesian API Fuzzer."""
    log.setLevel(log.INFO)
    cli_arguments = cli_parser.parse_args()
    if cli_arguments.version:
        show_version()
        sys.exit(0)
    else:
        cfg = setup(cli_arguments)
        fuzzer_settings = read_fuzzer_settings("fuzzer_settings.csv")
        results = Results()
        tests = read_csv_as_dicts(cfg["input_file"])
        start_tests(cfg, fuzzer_settings, tests, results)
        generate_reports(tests, results, cfg)


if __name__ == "__main__":
    # execute only if run as a script
    main()
