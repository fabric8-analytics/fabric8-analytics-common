"""Module with specification of all supported command line arguments."""

import argparse

cli_parser = argparse.ArgumentParser()

cli_parser.add_argument('-u', '--url',
                        help='specify URL to test',
                        action='store')

cli_parser.add_argument('-H', '--html',
                        help='generate report in HTML format',
                        action='store_true')
