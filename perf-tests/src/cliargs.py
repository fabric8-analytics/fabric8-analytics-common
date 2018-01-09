"""Module with specification of all supported command line arguments."""

import argparse

cli_parser = argparse.ArgumentParser()

cli_parser.add_argument('-s', '--server-api-benchmark',
                        help='run the basic server API benchmarks',
                        action='store_true')

cli_parser.add_argument('-j', '--jobs-api-benchmark',
                        help='run the basic jobs API benchmarks',
                        action='store_true')

cli_parser.add_argument('-S', '--stack-analysis-benchmark',
                        help='run stack analysis benchmarks',
                        action='store_true')

cli_parser.add_argument('-C', '--component-analysis-benchmark',
                        help='run component analysis benchmarks',
                        action='store_true')

cli_parser.add_argument('-P', '--package-query-to-graph-benchmark',
                        help='run benchmark that query packages in the graph database',
                        action='store_true')

cli_parser.add_argument('-V', '--package-version-query-to-graph-benchmark',
                        help='run benchmark that query package version in the graph database',
                        action='store_true')

cli_parser.add_argument('-p', '--parallel',
                        help='enable making parallel calls',
                        action='store_true')

cli_parser.add_argument('-d', '--dump',
                        help='dump JSON responses to files for further investigation',
                        action='store_true')

cli_parser.add_argument('--thread-min',
                        help='minimum number of threads for parallel calls (defalt=1)',
                        type=int, default=1)

cli_parser.add_argument('--thread-max',
                        help='maximum number of threads for parallel calls (defalt=10)',
                        type=int, default=10)

cli_parser.add_argument('--server-api-check',
                        help='check if the server API accepts requests',
                        action='store_true')

cli_parser.add_argument('--jobs-api-check',
                        help='check if the jobs API accepts requests',
                        action='store_true')

cli_parser.add_argument('--aws-s3-check',
                        help='check the connection to the AWS S3 database',
                        action='store_true')

cli_parser.add_argument('-g', '--generate-graph',
                        help='generate graph(s) as output',
                        action='store_true')

cli_parser.add_argument('-c', '--generate-csv',
                        help='generate CSV file(s) as output',
                        action='store_true')

cli_parser.add_argument('-H', '--generate-html',
                        help='generate HTML file(s) as output',
                        action='store_true')

cli_parser.add_argument('--sla',
                        help='run only benchmarks that are needed for SLA acceptance',
                        action='store_true')

cli_parser.add_argument('--manifest',
                        help='manifest file (from the data directory) used for the stack analysis',
                        type=str)
