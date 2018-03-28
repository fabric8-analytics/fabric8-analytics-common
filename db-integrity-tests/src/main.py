"""The main module of the database integrity tests."""

import sys
import re

from s3interface import S3Interface
from s3configuration import S3Configuration
from gremlin_configuration import GremlinConfiguration
from gremlin_interface import GremlinInterface
from cliargs import *
from utils import *
from csv_reporter import CSVReporter
from schema_validator import *
from core_package_checker import CorePackageChecker
from component_versions_checker import ComponentVersionsChecker

import logging

ECOSYSTEMS = [
    "pypi", "go", "maven", "npm", "nuget"
]


def initial_checks(s3interface, gremlinInterface):
    """Perform initial checks of services + selftest."""
    if s3interface is not None:
        check_buckets_existence(s3interface)
    else:
        logging.info("S3 tests disabled, skipping")
    if gremlinInterface is not None:
        pass
    else:
        logging.info("Gremlin tests disabled, skipping")


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
        core_package_git_stats = "N/A"
        core_package_leftovers = "N/A"

        if in_core_packages:
            core_package_json = core_package_checker.check_core_json()
            core_package_github_details = core_package_checker.check_github_details()
            core_package_keywords_tagging = core_package_checker.check_keywords_tagging()
            core_package_libraries_io = core_package_checker.check_libraries_io()
            core_package_git_stats = core_package_checker.check_git_stats()
            core_package_leftovers = core_package_checker.check_leftovers()

        csvReporter.core_package_info(ecosystem, package_name, in_core_packages, in_packages,
                                      core_package_json, core_package_github_details,
                                      core_package_keywords_tagging, core_package_libraries_io,
                                      core_package_git_stats, core_package_leftovers)


def check_package_versions_in_ecosystem(s3interface, csvReporter, ecosystem):
    """Check all package versions in selected ecosystem."""
    packages = s3interface.read_packages_for_ecosystem(ecosystem)

    # dummy read
    # core_packages = read_list("s3_core_packages.txt")
    # packages = read_list("s3_packages.txt")

    for package_name in packages:
        component_versions_checker = ComponentVersionsChecker(s3interface, ecosystem, package_name)
        all_jsons = component_versions_checker.read_metadata_list()
        directories, version_jsons, versions, metadata_list = \
            component_versions_checker.read_versions()

        for version in sorted(versions):
            component_versions_checker.version = version
            base_json = version in version_jsons
            subdir = version in directories
            metadata_for_version = [m for m in metadata_list if m.startswith(version + "/")]
            core_data = component_versions_checker.check_core_data()
            code_metrics = component_versions_checker.check_code_metrics()
            dependency_snapshot = component_versions_checker.check_dependency_snapshot()
            digests = component_versions_checker.check_digests()
            keywords_tagging = component_versions_checker.check_keywords_tagging()
            metadata = component_versions_checker.check_metadata()
            security_issues = component_versions_checker.check_security_issues()
            source_licenses = component_versions_checker.check_source_licenses()
            leftovers = component_versions_checker.check_leftovers(metadata_for_version)
            csvReporter.package_version_info(ecosystem, package_name, version, base_json, subdir,
                                             core_data, code_metrics, dependency_snapshot, digests,
                                             keywords_tagging, metadata, security_issues,
                                             source_licenses, leftovers)


def check_packages_in_s3(s3interface):
    """Check all packages in all ecosystems."""
    ECOSYSTEMS = ["pypi"]
    with CSVReporter("s3_core_packages.csv") as csvReporter:
        csvReporter.csv_header_for_core_packages()
        for ecosystem in ECOSYSTEMS:
            check_packages_in_ecosystem(s3interface, csvReporter, ecosystem)

    with CSVReporter("s3_package_versions.csv") as csvReporter:
        csvReporter.csv_header_for_package_version()
        for ecosystem in ECOSYSTEMS:
            check_package_versions_in_ecosystem(s3interface, csvReporter, ecosystem)


def set_log_level(log_level):
    """Set the desired log level."""
    logging.basicConfig(level=log_level)
    logging.info("Log level is set to {level}".format(level=log_level))


def main():
    """Entry point to the database integrity tests."""
    cli_arguments = cli_parser.parse_args()
    set_log_level(cli_arguments.log_level)

    s3_tests_enabled = not cli_arguments.disable_s3_tests
    gremlin_tests_enabled = not cli_arguments.disable_gremlin_tests

    s3interface = None
    if s3_tests_enabled:
        s3configuration = S3Configuration()
        s3interface = S3Interface(s3configuration)
        s3interface.connect()

    gremlinInterface = None
    if gremlin_tests_enabled:
        gremlinConfiguration = GremlinConfiguration()
        gremlinInterface = GremlinInterface(gremlinConfiguration)

    initial_checks(s3interface, gremlinInterface)

    if cli_arguments.check:
        logging.info("Only initial check is performed, exiting")
        sys.exit()

    check_packages_in_s3(s3interface)


if __name__ == "__main__":
    # execute only if run as a script
    main()
