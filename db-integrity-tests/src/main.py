"""The main module of the database integrity tests."""

import requests
import sys

from s3interface import S3Interface
from s3configuration import S3Configuration
from gremlin_configuration import GremlinConfiguration
from cliargs import *


def main():
    """Entry point to the database integrity tests."""
    cli_arguments = cli_parser.parse_args()

    pass


if __name__ == "__main__":
    # execute only if run as a script
    main()
