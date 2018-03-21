"""The main module of the database integrity tests."""

import sys
import re

from s3interface import S3Interface
from s3configuration import S3Configuration
from gremlin_configuration import GremlinConfiguration
from gremlin_interface import GremlinInterface
from cliargs import *
from csv_reporter import CSVReporter
from schema_validator import *
from core_package_checker import CorePackageChecker

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


def check_packages_in_ecosystem(s3interface, csvReporter, ecosystem):
    """Check all packages in selected ecosystem."""
    core_packages = s3interface.read_core_packages_for_ecosystem(ecosystem)
    packages = s3interface.read_packages_for_ecosystem(ecosystem)
    store_list("s3_core_packages.txt", core_packages)
    store_list("s3_packages.txt", packages)

    # dummy read
    # core_packages = read_list("s3_core_packages.txt")
    # packages = read_list("s3_packages.txt")

    all_packages = list(set(core_packages) | set(packages))
    all_packages.sort()
    for package_name in all_packages:
        core_package_checker = CorePackageChecker(s3interface, ecosystem, package_name)

        in_core_packages = package_name in core_packages
        in_packages = package_name in packages
        core_package_json = "N/A"
        core_package_github_details = "N/A"
        core_package_keywords_tagging = "N/A"
        core_package_libraries_io = "N/A"

        if in_core_packages:
            core_package_json = core_package_checker.check_core_json()
            core_package_github_details = core_package_checker.check_github_details()
            core_package_keywords_tagging = core_package_checker.check_keywords_tagging()
            core_package_libraries_io = core_package_checker.check_libraries_io()

        csvReporter.package_info(ecosystem, package_name, in_core_packages, in_packages,
                                 core_package_json, core_package_github_details,
                                 core_package_keywords_tagging, core_package_libraries_io)


def check_packages_in_s3(s3interface):
    """Check all packages in all ecosystems."""
    ECOSYSTEMS = ["pypi"]
    with CSVReporter("s3_packages.csv") as csvReporter:
        csvReporter.csv_header()
        for ecosystem in ECOSYSTEMS:
            check_packages_in_ecosystem(s3interface, csvReporter, ecosystem)


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
    check_packages_in_s3(s3interface)


if __name__ == "__main__":
    # execute only if run as a script
    main()
