#!/usr/bin/env python3

"""An implementation of Tests as a Service (TAAS) application."""

import connexion
from behave.__main__ import main as behave_main

from tempfile import mktemp

from os import listdir, remove
from os.path import isfile, join

TEST_DIR = "features"
TEST_SUFFIX = ".feature"


def get_file_list(directory, suffix):
    """Get list of files from selected directory that has the specified suffix."""
    # read list of files
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    # filter it
    files = [f for f in files if f.endswith(suffix)]
    # remove suffix
    files = [f[:-len(suffix)] for f in files]
    # and finally return sorted version of the list
    return sorted(files)


def health_check():
    """Check the health status of the service."""
    return {}, 200


def get_readiness():
    """Get TaaS service readiness."""
    return health_check()


def get_liveness():
    """Get TaaS service liveness."""
    return health_check()


def get_all_tests():
    """Get all available tests."""
    try:
        test_list = get_file_list(TEST_DIR, TEST_SUFFIX)
        return {"tests": test_list}, 200
    except Exception as e:
        return {"Status": "error",
                "Reason": e.__str__()}, 500


def run_behave(testname):
    """Run the Behave machinery, read overall test result, capture log file."""
    test_specification = "{dir}/{test}{suffix}".format(dir=TEST_DIR, test=testname,
                                                       suffix=TEST_SUFFIX)
    logfile = mktemp()
    print("Logfile: {logfile}".format(logfile=logfile))

    output_specification = "--outfile={logfile}".format(logfile=logfile)
    result = behave_main([test_specification, output_specification])
    print("Test result: {result}:".format(result=result))

    try:
        log = None

        with open(logfile, "r") as fin:
            log = fin.read()

        remove(logfile)
        return result, log

    except Exception as e:
        print("Exception occured: ", e)
        return 2, None


def run_test(testname):
    """Run the specified tests."""
    if not testname:
        return {"Status": "error",
                "Reason": "No test name supplied"}, 400

    tests = get_file_list(TEST_DIR, TEST_SUFFIX)

    if testname not in tests:
        return {"Status": "error",
                "Reason": "The specified test was not found"}, 404

    result, log = run_behave(testname)

    if result == 0:
        return {"Status": "ok", "Log": log}, 200
    else:
        return {"Status": "error"}, 500


def main():
    """Start the Flask app."""
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.add_api('swagger.yaml', arguments={'title': 'Tests as a Service'})
    app.run(port=8080)


if __name__ == '__main__':
    main()
