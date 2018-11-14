"""Tests for API endpoints that performs fetching of CVE information by date and further by ecosystem."""

from behave import given, then, when
from urllib.parse import urljoin
import requests


@given('cve_bydate_ecosystem service is running')
def running_cve_bydate_ecosystem_api(context):
    """Checks if API is running."""
    return context.is_cve_bydate_ecosystem_service_running(context)

def perform_bydate_ecosystem_search(context, date, ecosystem):
    """Call API endpoint to search for ecosystem."""
    if ecosystem is None:
        path = "api/v1/bydate/{date}".format(date=date)
    else:
        path = "api/v1/bydate/{date}/{ecosystem}".format(date=date, ecosystem=ecosystem)
    url = urljoin(context.coreapi_url, path)
    context.response = requests.get(url)

@when('I search for {date} date')
@when("I search for {date} date and {ecosystem} ecosystem")
def search_for_ecosystem(context, date, ecosystem=None):
    """Search for given ecosystem via the bydate_ecosystem search REST API call."""
    perform_bydate_ecosystem_search(context, date, ecosystem)


@then('I should receive an empty JSON response')
def empty_JSON_response(context):
    """Check whether the received JSON response is empty"""
    response = context.response
    assert response
    assert 'count' in response
    assert response['count'] == 0
    assert 'add' in response
    assert len(response['add']) == 0
    assert 'remove' in response
    assert len(response['remove'])==0

