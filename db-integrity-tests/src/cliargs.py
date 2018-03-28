"""Module with specification of all supported command line arguments."""

import argparse

cli_parser = argparse.ArgumentParser()

cli_parser.add_argument('--log-level',
                        help='log level as defined in ' +
                             'https://docs.python.org/3/library/logging.html#logging-levels',
                        type=int, default=20)

cli_parser.add_argument('-c', '--check',
                        help='perform initial check only',
                        action='store_true')

cli_parser.add_argument('-d3', '--disable-s3-tests',
                        help='disable S3 tests',
                        action='store_true')

cli_parser.add_argument('-dg', '--disable-gremlin-tests',
                        help='disable Gremlin tests',
                        action='store_true')
