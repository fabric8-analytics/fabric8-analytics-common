"""The main module of the Analytics API Load Tests tool.

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

import sys
import os
from time import time
from fastlog import log
from csv_reader import read_csv_as_dicts
from setup import setup
from cliargs import cli_parser

from component_analysis import ComponentAnalysis
from stack_analysis import StackAnalysis
from test_runner import start_tests


# current version of this tool
VERSION_MAJOR = 1
VERSION_MINOR = 0


def check_api_endpoint(api):
    """Check that some API endpoint is callable."""
    log.info("Checking: core API endpoint")
    with log.indent():
        if not api.is_api_running():
            log.error("Fatal: tested system is not available")
            sys.exit(1)
        else:
            log.success("ok")


def check_auth_token(api):
    """Check the authorization token for the core API."""
    log.info("Checking: authorization token for the core API")
    with log.indent():
        if api.check_auth_token_validity():
            log.success("ok")
        else:
            log.error("Fatal: wrong token(?)")
            sys.exit(1)


def check_system(api):
    """Check if all system endpoints are available and that tokens are valid."""
    # try to access system endpoints
    log.info("System check")
    with log.indent():
        check_api_endpoint(api)
        check_auth_token(api)


def show_version():
    """Show A2T version."""
    print("A2T version {major}.{minor}".format(major=VERSION_MAJOR, minor=VERSION_MINOR))


def main():
    """Entry point to the Analytics API Load Tests."""
    log.setLevel(log.INFO)
    cli_arguments = cli_parser.parse_args()
    if cli_arguments.version:
        show_version()
        sys.exit(0)
    else:
        cfg = setup(cli_arguments)

        coreapi_url = os.environ.get('F8A_SERVER_API_URL', None)
        component_analysis = ComponentAnalysis(coreapi_url,
                                               cfg["access_token"], cfg["user_key"], True)
        stack_analysis = StackAnalysis(coreapi_url,
                                       cfg["access_token"], cfg["user_key"], True)

        check_system(component_analysis)

        try:
            tests = read_csv_as_dicts(cfg["input_file"])
        except Exception as e:
            log.error("Test description can not be read")
            log.error(e)
            sys.exit(0)

        t1 = time()
        tags = cfg["tags"]
        start_tests(cfg, tests, tags, component_analysis, stack_analysis)
        t2 = time()
        log.info("Start time: {}".format(t1))
        log.info("End time:   {}".format(t2))
        log.info("Duration:   {}".format(t2 - t1))


if __name__ == "__main__":
    # execute only if run as a script
    main()
