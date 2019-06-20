"""Module with specification of all supported command line arguments.

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

import argparse

cli_parser = argparse.ArgumentParser()

cli_parser.add_argument('-v', '--version',
                        help='show version information',
                        action='store_true')

cli_parser.add_argument('-i', '--input',
                        help='specify input file with test descriptions',
                        action='store')

cli_parser.add_argument('-t', '--tags',
                        help='select tests by tags',
                        action='store')

cli_parser.add_argument('-D', '--dry',
                        help='dry run (do not call REST API)',
                        action='store_true')

cli_parser.add_argument('-d', '--dump-results',
                        help='dump REST API results into JSON files',
                        action='store_true')
