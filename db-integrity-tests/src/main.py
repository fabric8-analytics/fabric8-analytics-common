"""The main module of the database integrity tests."""

import sys
import re

from s3interface import S3Interface
from s3configuration import S3Configuration
from gremlin_configuration import GremlinConfiguration
from gremlin_interface import GremlinInterface
from cliargs import *

import logging

ECOSYSTEMS = [
    "pypi"
]


def initial_checks(s3interface, gremlinInterface):
    """Perform initial checks of services + selftest."""
    check_buckets_existence(s3interface)


def check_buckets_existence(s3interface):
    """Check if all expected buckets really exists."""
    expected_buckets = [
        "core-data",
        "core-manifests",
        "core-package-data"]

    prefix = s3interface.deployment_prefix
    buckets = s3interface.read_bucket_names()

    for expected_bucket in expected_buckets:
        full_bucket_name = prefix + "-bayesian-" + expected_bucket
        logging.info("checking presence of bucket {bucket}".format(bucket=full_bucket_name))
        assert full_bucket_name in buckets, \
            "Can not find bucket with name '{n}'".format(n=full_bucket_name)


def set_log_level(log_level):
    """Set the desired log level."""
    logging.basicConfig(level=log_level)
    logging.info("Log level is set to {level}".format(level=log_level))


def main():
    """Entry point to the database integrity tests."""
    cli_arguments = cli_parser.parse_args()
    set_log_level(cli_arguments.log_level)

    s3configuration = S3Configuration()
    s3interface = S3Interface(s3configuration)
    s3interface.connect()

    gremlinConfiguration = GremlinConfiguration()
    gremlinInterface = GremlinInterface(gremlinConfiguration)

    initial_checks(s3interface, gremlinInterface)


if __name__ == "__main__":
    # execute only if run as a script
    main()
