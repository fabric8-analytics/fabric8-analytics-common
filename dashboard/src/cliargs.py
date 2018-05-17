"""Module with specification of all supported command line arguments."""

import argparse

cli_parser = argparse.ArgumentParser()

cli_parser.add_argument('-dl', '--disable-liveness',
                        help='disable the service liveness checks',
                        action='store_true')

cli_parser.add_argument('-ds', '--disable-sla',
                        help='disable the SLA part',
                        action='store_true')

cli_parser.add_argument('-dq', '--disable-code-quality',
                        help='disable the code quality check',
                        action='store_true')

cli_parser.add_argument('-dj', '--disable-ci-jobs',
                        help='disable CI jobs table generation',
                        action='store_true')

cli_parser.add_argument('-c', '--clone-repositories',
                        help='make local clone of all repositories',
                        action='store_true')

cli_parser.add_argument('-d', '--cleanup-repositories',
                        help='cleanup the local clones of all repositories',
                        action='store_true')

cli_parser.add_argument('-t', '--code-coverage-threshold',
                        help='specify code coverage threshold',
                        type=int)
