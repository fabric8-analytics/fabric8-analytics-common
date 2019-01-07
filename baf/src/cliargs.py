"""Module with specification of all supported command line arguments."""

import argparse

cli_parser = argparse.ArgumentParser()

cli_parser.add_argument('-v', '--version',
                        help='show version information',
                        action='store_true')

cli_parser.add_argument('-i', '--input',
                        help='specify input file with test descriptions',
                        action='store')

cli_parser.add_argument('-u', '--url',
                        help='specify URL to test',
                        action='store')

cli_parser.add_argument('-D', '--dry',
                        help='dry run (do not call REST API)',
                        action='store_true')

cli_parser.add_argument('-t', '--text',
                        help='generate report in plain text format',
                        action='store')

cli_parser.add_argument('-H', '--html',
                        help='generate report in HTML format',
                        action='store')

cli_parser.add_argument('-C', '--csv',
                        help='generate report in CSV format',
                        action='store')

cli_parser.add_argument('-T', '--tsv',
                        help='generate report in TSV format',
                        action='store')

cli_parser.add_argument('-X', '--xml',
                        help='generate report in XML format',
                        action='store')
