"""The main module of the Bayesian API Fuzzer."""

import sys
from fastlog import log
from csv_reader import read_csv_as_dicts
from setup import setup

from fuzzer import run_test


def run_all_tests(cfg, tests):
    """Run all tests read from CSV file."""
    i = 1
    for test in tests:
        log.info("Starting test #{n} with name '{desc}'".format(n=i, desc=test["Name"]))
        with log.indent():
            run_test(cfg, test)
        i += 1


def main():
    """Entry point to the Bayesian API Fuzzer."""
    log.setLevel(log.INFO)
    cfg = setup()

    log.info("Run tests")
    with log.indent():
        tests = read_csv_as_dicts("tests.csv")
        if not tests or len(tests) == 0:
            log.error("No tests loaded!")
            sys.exit(-1)
        if len(tests) == 1:
            log.info("Loaded 1 test")
        else:
            log.info("Loaded {n} tests".format(n=len(tests)))
        run_all_tests(cfg, tests)


if __name__ == "__main__":
    # execute only if run as a script
    main()
