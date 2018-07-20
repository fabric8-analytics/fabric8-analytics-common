"""Tests for license analysis service."""

import requests

from behave import given, then, when
from urllib.parse import urljoin

from src.parsing import *
from src.utils import *
from src.authorization_tokens import *
from src.attribute_checks import *


@when("I access the license analysis service")
def access_license_service(context):
    """Access the licence analysis service."""
    context.response = requests.get(context.license_service_url)


@when("I access the license analysis service with authorization token")
def access_license_service(context):
    """Access the licence analysis service using the authorization token."""
    context.response = requests.get(context.license_service_url,
                                    headers=authorization(context))


def send_payload_to_license_analysis(context, filename, use_token):
    """Send the selected file to the license analysis service to be processed."""
    filename = 'data/license_analysis/{filename}'.format(filename=filename)
    path_to_file = os.path.abspath(filename)

    endpoint = context.license_service_url + "/api/v1/license-recommender"

    with open(path_to_file) as json_data:
        if use_token:
            response = requests.post(endpoint, data=json_data,
                                     headers=authorization(context))
        else:
            response = requests.post(endpoint, data=json_data)

    context.response = response


@when("I send the file {filename} to the license analysis service")
@when("I send the file {filename} to the license analysis service {token} authorization token")
def send_the_file_for_license_analysis(context, filename, token="without"):
    """Test step to send the selected file to the license analysis service."""
    use_token = parse_token_clause(token)
    send_payload_to_license_analysis(context, filename, use_token)


@then("I should find that the license analysis status is {expected}")
def check_license_analysis_status(context, expected):
    """Check the status of license analysis."""
    json_data = context.response.json()
    status = check_and_get_attribute(json_data, "status")
    status = status.lower()
    assert status == expected, \
        "License service returns status {status}, but other status {expected} is expected instead" \
        .format(status=status, expected=expected)


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


@then("I should find {license} license in distinct licenses")
def check_distinct_license_existence(context, license):
    """Check if the given license has been returned from the license service."""
    json_data = context.response.json()
    distinct_licenses = check_and_get_attribute(json_data, "distinct_licenses")
    assert distinct_licenses, "Distinct licenses array shall not be empty"
    assert license in distinct_licenses, \
        "Can not find the expected {license} license in distinct licenses".format(license=license)
