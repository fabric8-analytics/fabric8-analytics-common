"""The main module of the database integrity tests."""

import sys
import re

from s3interface import S3Interface
from s3configuration import S3Configuration
from gremlin_configuration import GremlinConfiguration
from gremlin_interface import GremlinInterface
from cliargs import *
from csv_reporter import CSVReporter

import logging

ECOSYSTEMS = [
    "pypi", "go", "maven", "npm", "nuget"
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


def check_ecosystems_in_bucket(found_ecosystems, bucket_name):
    """Check if the selected bucket contains expected ecosystem objects."""
    expected_ecosystems = set(ECOSYSTEMS)

    # check if all expected ecosystems exists
    not_found_ecosystems = expected_ecosystems - set(found_ecosystems)
    if not_found_ecosystems:
        logging.error("the following ecosystem{s} can't we found in the '{b}' bucket: {e}".format(
            s='s' if len(not_found_ecosystems) > 1 else '', e=not_found_ecosystems, b=bucket_name))

    # check for possible leftovers
    leftovers = set(found_ecosystems) - expected_ecosystems
    if leftovers:
        logging.error(
            "the following unexpected object{s} were found in the '{b}' bucket: {o}".format(
                s='s' if len(leftovers) > 1 else '', o=leftovers, b=bucket_name))


def check_ecosystems_in_s3(s3interface):
    """Check if all tested buckets contain expected ecosystem objects."""
    found_ecosystems = s3interface.read_ecosystems_from_core_package_data()
    check_ecosystems_in_bucket(found_ecosystems, "core_package_data")

    found_ecosystems = s3interface.read_ecosystems_from_core_data()
    check_ecosystems_in_bucket(found_ecosystems, "core_data")


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
    check_ecosystems_in_s3(s3interface)


if __name__ == "__main__":
    # execute only if run as a script
    main()
