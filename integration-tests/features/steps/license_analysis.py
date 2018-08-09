"""Tests for license analysis service."""

import requests

from behave import then, when
from urllib.parse import urljoin

from src.parsing import *
from src.utils import *
from src.authorization_tokens import *
from src.attribute_checks import *

from common import *


LICENSE_ANALYSIS_PAYLOAD_DIRECTORY = "data/license_analysis"

# endpoint name for the license analysis
LICENSE_RECOMMENDER_ENDPOINT = "license-recommender"

STACK_LICENSE_PAYLOAD_DIRECTORY = "data/license_analysis_stack_license"

# endpoint name for the stack license analysis
STACK_LICENSE_ENDPOINT = "stack_license"


@when("I access the license analysis service")
def access_license_service(context):
    """Access the licence analysis service."""
    context.response = requests.get(context.license_service_url)


@when("I access the license analysis service with authorization token")
def access_license_service(context):
    """Access the licence analysis service using the authorization token."""
    context.response = requests.get(context.license_service_url,
                                    headers=authorization(context))


def url_to_endpoint(service_url, endpoint):
    """Construct URL to the selected endpoint."""
    assert service_url, "Service URL must be specified and should not be empty"
    assert endpoint, "Endpoint must be spefified and should not be empty"
    url = urljoin(service_url, "/api/v1/")
    return urljoin(url, endpoint)


def send_payload_to_license_analysis(context, directory, filename, endpoint, use_token):
    """Send the selected file to the license analysis service to be processed."""
    filename = '{directory}/{filename}'.format(directory=directory, filename=filename)
    path_to_file = os.path.abspath(filename)

    url = url_to_endpoint(context.license_service_url, endpoint)

    with open(path_to_file) as json_data:
        if use_token:
            response = requests.post(url, data=json_data,
                                     headers=authorization(context))
        else:
            response = requests.post(url, data=json_data)

    context.response = response


@when("I send the file {filename} to the license analysis service")
@when("I send the file {filename} to the license analysis service {token} authorization token")
def send_the_file_for_license_analysis(context, filename, token="without"):
    """Test step to send the selected file to the license analysis service."""
    use_token = parse_token_clause(token)
    send_payload_to_license_analysis(context, LICENSE_ANALYSIS_PAYLOAD_DIRECTORY, filename,
                                     LICENSE_RECOMMENDER_ENDPOINT, use_token)


@when("I send the file {filename} to the stack license analysis endpoint of license " +
      "analysis service")
@when("I send the file {filename} to the stack license analysis endpoint of license " +
      "analysis service {token} authorization token")
def send_the_file_for_stack_license_analysis(context, filename, token="without"):
    """Test step to send the payload to the stack analysis endpoint of license analysis service."""
    use_token = parse_token_clause(token)
    send_payload_to_license_analysis(context, STACK_LICENSE_PAYLOAD_DIRECTORY, filename,
                                     STACK_LICENSE_ENDPOINT, use_token)


@then("I should find that the license analysis status is {expected}")
def check_license_analysis_status(context, expected):
    """Check the status of license analysis."""
    json_data = context.response.json()
    status = check_and_get_attribute(json_data, "status")
    status = status.lower()
    assert status == expected, \
        "License service returns status {status}, but other status {expected} is expected instead" \
        .format(status=status, expected=expected)


@then("I should see that the analysis message says \"{message}\"")
def check_license_analysis_message(context, message):
    """Check the message for the last license analysis."""
    json_data = context.response.json()
    actual = check_and_get_attribute(json_data, "message")
    assert actual == message, \
        "License service returns message {actual}, but other message {message} is expected" \
        .format(actual=actual, message=message)


@then("I should find that the license analysis failed because of stack conflict")
def check_license_analysis_status_stack_conflict_expected(context):
    """Check the status of license analysis - stack conflict is expected."""
    check_license_analysis_status(context, "stackconflict")


@then("I should find that the license analysis failed because of component conflict")
def check_license_analysis_status_component_conflict_expected(context):
    """Check the status of license analysis - component conflict is expected."""
    check_license_analysis_status(context, "componentconflict")


@then("I should find empty stack license")
def check_license_analysis_stack_license_empty(context):
    """Check the computed stack license."""
    json_data = context.response.json()
    license = check_and_get_attribute(json_data, "stack_license")
    assert license is None, \
        "License service returns {license} stack license, " \
        "but null value is expected instead" \
        .format(license=license)


@then("I should find that the stack license is {expected}")
def check_license_analysis_stack_license(context, expected):
    """Check the computed stack license."""
    json_data = context.response.json()
    license = check_and_get_attribute(json_data, "stack_license")
    assert license == expected, \
        "License service returns {license} stack license, " \
        "but other license {expected} is expected instead" \
        .format(license=license, expected=expected)


@then("I should not see any conflict packages")
def check_no_conflict_packages(context):
    """Check the computed conflict packages."""
    json_data = context.response.json()
    conflict_packages = check_and_get_attribute(json_data, "conflict_packages")
    assert len(conflict_packages) == 0, \
        "There should not be any conflict packages reported, " \
        "but the service returned {p} conflicting packages" \
        .format(p=", ".join(conflict_packages))


@then("I should see one group of conflict packages")
@then("I should see {expected} groups of conflict packages")
def check_has_conflict_packages(context, expected="one"):
    """Check the computed conflict packages."""
    json_data = context.response.json()
    expected = parse_number(expected)
    conflict_packages = check_and_get_attribute(json_data, "conflict_packages")
    actual = len(conflict_packages)
    assert actual == expected, \
        "There should be {expected} conflict packages reported, " \
        "but the service returned {actual} conflicting packages" \
        .format(expected=expected, actual=actual)


@then("I should see the license {license} for package {package} in the {order} group of conflict " +
      "packages")
def check_conflict_package_in_a_list(context, license, package, order):
    """Check the computed conflict license existence."""
    json_data = context.response.json()
    order = parse_number(order)
    conflict_packages = check_and_get_attribute(json_data, "conflict_packages")

    # preliminary check the number of conflict packages
    assert len(conflict_packages) >= order, "At least {n} groups of conflicting packages  expected"

    group = conflict_packages[order]

    # check if the package belongs to selected group
    assert package in group, "Package {package} is expected in the {order} group".format(
        package=package, order=order)

    actual_license = group[package]

    # time to check the license tied to selected package
    assert actual_license == license, \
        "The expected license {license} is different from actual license {actual}".format(
            license=license, actual=actual_license)


@then("I should not see any outlier packages")
def check_no_outlier_packages(context):
    """Check the computed outlier packages."""
    json_data = context.response.json()
    outlier_packages = check_and_get_attribute(json_data, "outlier_packages")
    assert len(outlier_packages) == 0, \
        "There should not be any outlier packages reported, " \
        "but the service returned {p} packages" \
        .format(p=", ".join(outlier_packages))


@then("I should see {expected} distinct license")
@then("I should see {expected} distinct licenses")
def check_distinct_license_count(context, expected):
    """Check the number of distinct licenses found by the license service."""
    json_data = context.response.json()
    expected = parse_number(expected)
    distinct_licenses = check_and_get_attribute(json_data, "distinct_licenses")
    found = len(distinct_licenses)
    assert found == expected, \
        "There should be {expected} distinct licenses in the license analysis, but {found} " \
        "has been found".format(expected=expected, found=found)


@then("I should not see any distinct licenses")
def check_no_distinct_licenses(context):
    """Check distinct licenses from the license service."""
    json_data = context.response.json()
    distinct_licenses = check_and_get_attribute(json_data, "distinct_licenses")
    assert len(distinct_licenses) == 0, \
        "There should not be any distinct licenses reported, " \
        "but the service returned {licenses} such licenses" \
        .format(licenses=", ".join(distinct_licenses))


@then("I should find {license} license in distinct licenses")
def check_distinct_license_existence(context, license):
    """Check if the given license has been returned from the license service."""
    json_data = context.response.json()
    distinct_licenses = check_and_get_attribute(json_data, "distinct_licenses")
    assert distinct_licenses, "Distinct licenses array shall not be empty"
    assert license in distinct_licenses, \
        "Can not find the expected {license} license in distinct licenses".format(license=license)


@then("I should not see any component conflicts")
def check_no_component_conflicts(context):
    """Check the computed component conflicts."""
    json_data = context.response.json()
    unknown_licenses = check_and_get_attribute(json_data, "unknown_licenses")
    component_conflicts = check_and_get_attribute(unknown_licenses, "component_conflict")
    assert len(component_conflicts) == 0, \
        "There should not be any component conflicts reported, " \
        "but the service returned {c} conflicts" \
        .format(c=", ".join(component_conflicts))


@then("I should not see any really unknown licenses")
def check_no_really_unknown_licenses(context):
    """Check the computed really unknown licenses."""
    json_data = context.response.json()
    unknown_licenses = check_and_get_attribute(json_data, "unknown_licenses")
    really_unknown = check_and_get_attribute(unknown_licenses, "really_unknown")
    assert len(really_unknown) == 0, \
        "There should not be any really unknown licenses reported, " \
        "but the service returned {c} unknown licenses" \
        .format(c=", ".join(really_unknown))


def no_package_found(package, version):
    """Throw an exception, because the given package+version can not be found."""
    msg = "Could not find expected package {package} version {version}".format(package=package,
                                                                               version=version)
    raise Exception(msg)


def check_packages_list(packages):
    """Check the content of list of packages."""
    assert len(packages) >= 1, "Expecting it least one package in the list"


@then("I should find license {license} for the package {package} version {version}")
def check_license_for_package_version(context, license, package, version):
    """Check if the given license has been reported for the package+version."""
    json_data = context.response.json()
    packages = check_and_get_attribute(json_data, "packages")
    check_packages_list(packages)

    for p in packages:
        if p["package"] == package and p["version"] == version:
            licenses = p["licenses"]
            assert license in licenses, ("Can not find expected license " +
                                         "{license} in {licenses}").format(license=license,
                                                                           licenses=licenses)
            # are we here? -> we have found the expected license -> everything's fine
            return

    # too bad, the package+version were not returned by the license service
    no_package_found(package, version)


@then("I should not find any license for package {package} version {version}")
def check_license_for_package_version_none(context, package, version):
    """Check if none license has been reported for the package+version."""
    json_data = context.response.json()
    packages = check_and_get_attribute(json_data, "packages")
    check_packages_list(packages)

    for p in packages:
        if p["package"] == package and p["version"] == version:
            licenses = p["licenses"]
            assert not licenses, \
                "None license shall be returned, but {licenses} has been found".format(
                    license=licenses)
            # are we here? -> we have found the expected license -> everything's fine
            return

    # too bad, the package+version were not returned by the license service
    no_package_found(package, version)


def test_attribute_value_in_license_analysis(packages, package, version, attribute_name,
                                             expected_value, error_message):
    """Check the value of selected attribute from the given package+version in license analysis."""
    # packages are returned in an array of dicts
    # and we need to find the package by its name and version
    for p in packages:
        if p["package"] == package and p["version"] == version:
            license_analysis = check_and_get_attribute(p, "license_analysis")
            actual_value = check_and_get_attribute(license_analysis, attribute_name)
            assert actual_value == expected_value, error_message
            # are we here? -> we have found the expected attribute value in license analysis
            # -> everything's fine
            return

    # too bad, the package+version were not returned by the license service
    no_package_found(package, version)


def test_attribute_value_in_license_analysis_list(packages, package, version, attribute_name,
                                                  expected_value, error_message):
    """Check the value of selected attribute from the given package+version in license analysis."""
    # packages are returned in an array of dicts
    # and we need to find the package by its name and version
    for p in packages:
        if p["package"] == package and p["version"] == version:
            license_analysis = check_and_get_attribute(p, "license_analysis")
            actual_values = check_and_get_attribute(license_analysis, attribute_name)
            assert expected_value in actual_values, error_message
            # are we here? -> we have found the expected attribute value in license analysis
            # -> everything's fine
            return

    # too bad, the package+version were not returned by the license service
    no_package_found(package, version)


@then("I should find that representative license has been found for package {package} " +
      "version {version}")
def check_license_report_for_package_version(context, package, version):
    """Check if the given license has been reported for the package+version."""
    json_data = context.response.json()
    packages = check_and_get_attribute(json_data, "packages")
    check_packages_list(packages)
    # check if the '_message' attribute contain expected content
    test_attribute_value_in_license_analysis(packages, package, version, "_message",
                                             "Representative license found",
                                             "Wrong message has been found in the returned " +
                                             "license analysis")


@then("I should find that representative license has not been found for package {package} " +
      "version {version} with the reason {reason}")
def check_license_report_for_package_version(context, package, version, reason):
    """Check if the given license has been reported for the package+version."""
    json_data = context.response.json()
    packages = check_and_get_attribute(json_data, "packages")
    check_packages_list(packages)
    # check if the '_message' attribute contain expected content
    test_attribute_value_in_license_analysis(packages, package, version, "_message",
                                             reason,
                                             "Wrong message has been found in the returned " +
                                             "license analysis")


def resolve_expected_status(status):
    """Resolve expected status, that are to be checked for the selected package + version."""
    expected_statuses = {"successful": "Successful",
                         "conflict": "Conflict"}
    return expected_statuses.get(status, "Failure")


@then("I should find that license analysis was {status} for package {package} version {version}")
def check_license_analysis_status_for_package_version(context, status, package, version):
    """Check the status of license analysis for the package+version."""
    expected_status = resolve_expected_status(status)
    json_data = context.response.json()
    packages = check_and_get_attribute(json_data, "packages")
    check_packages_list(packages)
    # check if the 'status' attribute contain expected content
    test_attribute_value_in_license_analysis(packages, package, version, "status",
                                             expected_status,
                                             "Wrong license analysis status has been reported")


@then("I should find the {license} license in conflict licenses for the package " +
      "{package} version {version}")
def check_license_analysis_conflicts_for_package_version(context, license, package, version):
    """Check the conflicts of license analysis for the package+version."""
    json_data = context.response.json()
    packages = check_and_get_attribute(json_data, "packages")
    check_packages_list(packages)
    # packages are returned in an array of dicts
    # and we need to find the package by its name and version
    for p in packages:
        if p["package"] == package and p["version"] == version:
            license_analysis = check_and_get_attribute(p, "license_analysis")
            conflict_licenses_list = check_and_get_attribute(license_analysis, "conflict_licenses")
            for conflict_licenses in conflict_licenses_list:
                assert license in conflict_licenses, \
                    "The license {license} is expected in conflict_licenses {licenses}".format(
                        license=license, licenses=conflict_licenses)
                # are we here? -> we have found the expected attribute value in license analysis
                # -> everything's fine
                return

    # too bad, the package+version were not returned by the license service
    no_package_found(package, version)


@then("I should find that the representative license is {license} for package " +
      "{package} version {version}")
def check_representative_license_for_package_version(context, license, package, version):
    """Check the representative license for the package+version."""
    json_data = context.response.json()
    packages = check_and_get_attribute(json_data, "packages")
    check_packages_list(packages)

    error_message = "Wrong representative license has been found, " \
                    "expected license is '{expected}'".format(expected=license)
    # check if the '_representative_licenses' attribute contain expected content
    test_attribute_value_in_license_analysis(packages, package, version, "_representative_licenses",
                                             license, error_message)


@then("I should not see any unknown licenses for the package {package} version {version}")
def check_no_unknown_licenses_for_package_version(context, package, version):
    """Check the unknown licenses for the package+version."""
    json_data = context.response.json()
    packages = check_and_get_attribute(json_data, "packages")
    check_packages_list(packages)
    # check if the 'unknown_licenses' attribute contain expected content
    test_attribute_value_in_license_analysis(packages, package, version, "unknown_licenses",
                                             [],
                                             "No unknown licenses expected in the analysis")


@then("I should not see any conflict licenses for the package {package} version {version}")
def check_no_conflict_licenses_for_package_version(context, package, version):
    """Check the unknown licenses for the package+version."""
    json_data = context.response.json()
    packages = check_and_get_attribute(json_data, "packages")
    check_packages_list(packages)
    # check if the 'unknown_licenses' attribute contain expected content
    test_attribute_value_in_license_analysis(packages, package, version, "conflict_licenses",
                                             [],
                                             "No conflict licenses expected in the analysis")


@then("I should not see any outlier licenses for the package {package} version {version}")
def check_no_outliner_licenses_for_package_version(context, package, version):
    """Check the outlier licenses for the package+version."""
    json_data = context.response.json()
    packages = check_and_get_attribute(json_data, "packages")
    check_packages_list(packages)
    # check if the 'outlier_licenses' attribute contain expected content
    test_attribute_value_in_license_analysis(packages, package, version, "outlier_licenses",
                                             [],
                                             "No outlier licenses expected in the analysis")


@then("I should find outlier license {license} for the package {package} version {version}")
def check_outliner_license_for_package_version(context, license, package, version):
    """Check the outlier licenses for the package+version."""
    json_data = context.response.json()
    packages = check_and_get_attribute(json_data, "packages")
    check_packages_list(packages)
    # check if the 'outlier_licenses' attribute contain expected content
    error_message = "License {license} can not be found in outlier license list".format(
        license=license)
    test_attribute_value_in_license_analysis_list(packages, package, version, "outlier_licenses",
                                                  license, error_message)


@then("I should find data structure with information about license filter")
def check_license_filter_structure(context):
    """Check the existence of 'license_filter' attribute in the JSON response."""
    find_dictionary_under_the_path(context,
                                   "license_filter")


@then("I should find alternate packages dictionary in license filter data structure")
def check_license_filter_structure_alternate_packages(context):
    """Check the existence of 'license_filter/alternate_packages' attribute in the JSON response."""
    find_dictionary_under_the_path(context,
                                   "license_filter/alternate_packages")


@then("I should find companion packages dictionary in license filter data structure")
def check_license_filter_structure_companion_packages(context):
    """Check the existence of 'license_filter/companion_packages' attribute in the JSON response."""
    find_dictionary_under_the_path(context,
                                   "license_filter/companion_packages")


@then("I should not see any compatible packages in alternate packages dictionary in license "
      "filter data structure")
def check_license_filter_structure_alternate_packages_compatible_packages(context):
    """Check the existence of 'license_filter/alternate_packages/compatible_packages' attribute."""
    find_empty_list_under_the_path(context,
                                   "license_filter/alternate_packages/compatible_packages")


@then("I should not see any conflict packages in alternate packages dictionary in license "
      "filter data structure")
def check_license_filter_structure_alternate_packages_conflict_packages(context):
    """Check the existence of 'license_filter/alternate_packages/conflict_packages' attribute."""
    find_empty_list_under_the_path(context,
                                   "license_filter/alternate_packages/conflict_packages")


@then("I should not see any unknown license packages in alternate packages dictionary in license "
      "filter data structure")
def check_license_filter_structure_alternate_packages_unknown_license_packages(context):
    """Check the existence of 'license_filter/alternate_packages/unknown_license_packages'."""
    find_empty_list_under_the_path(context,
                                   "license_filter/alternate_packages/unknown_license_packages")


@then("I should not see any compatible packages in companion packages dictionary in license "
      "filter data structure")
def check_license_filter_structure_companion_packages_compatible_packages(context):
    """Check the existence of 'license_filter/companion_packages/compatible_packages' attribute."""
    find_empty_list_under_the_path(context,
                                   "license_filter/companion_packages/compatible_packages")


@then("I should not see any conflict packages in companion packages dictionary in license "
      "filter data structure")
def check_license_filter_structure_companion_packages_conflict_packages(context):
    """Check the existence of 'license_filter/companion_packages/conflict_packages' attribute."""
    find_empty_list_under_the_path(context,
                                   "license_filter/companion_packages/conflict_packages")


@then("I should not see any unknown license packages in companion packages dictionary in license "
      "filter data structure")
def check_license_filter_structure_companion_packages_unknown_license_packages(context):
    """Check the existence of 'license_filter/companion_packages/unknown_license_packages'."""
    find_empty_list_under_the_path(context,
                                   "license_filter/companion_packages/unknown_license_packages")
