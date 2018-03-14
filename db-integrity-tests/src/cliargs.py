"""Module with specification of all supported command line arguments."""

import argparse

cli_parser = argparse.ArgumentParser()

cli_parser.add_argument('--log-level',
                        help='log level as defined in ' +
                             'https://docs.python.org/3.5/library/logging.html#logging-level',
                        type=int, default=20)
