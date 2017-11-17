
"""Tests for API endpoints that for Crowdsourcing."""
import requests

from behave import given, then, when
from urllib.parse import urljoin

from src.parsing import *
from src.utils import *
from src.authorization_tokens import *


@given('Master tag list api is running')
def running_master_tag_list_api(context):
    """Wait for the master tag list REST API to be available."""
    if not context.is_master_tag_list_service_running(context):
        context.wait_for_master_tag_list_service(context, 60)


def master_tag_list_url(context, ecosystem):
    """Construct URL for master tag list REST API call."""
    return urljoin(context.coreapi_url,
                   'api/v1/master-tags/{e}'.format(e=ecosystem))


def get_master_tag_list(context, ecosystem, use_token):
    """Call API endpoint master tag list"""
    if use_token:
        context.response = requests.get(master_tag_list_url(context, ecosystem),
                                        headers=authorization(context))
    else:
        context.response = requests.get(master_tag_list_url(context, ecosystem))


@when("I access master tag list API point for ecosystem {ecosystem} without authorization token")
def fetch_master_tag_list_without_token(context, ecosystem):
    """Fetch master tag list for given ecosystem REST API call."""
    get_master_tag_list(context, ecosystem, False)


@when("I access master tag list API point for ecosystem {ecosystem} with authorization token")
def fetch_master_tag_list_with_token(context, ecosystem):
    """Fetch master tag list for given ecosystem REST API call."""
    get_master_tag_list(context, ecosystem, True)


@then('I should get 401 status code as response for master tag list')
def check_status_code_for_master_tag_list(context):
    """Check master tag list require authorization tokens"""
    assert context.response.status_code == 401


@then('I should get json object contains tag_list which is a array of strings')
def check_master_tag_list_response_json(context):
    """Check that json response contains master tags"""
    json_data = context.response.json()
    assert 'ecosystem' in json_data
    assert 'tag_list' is not any(json_data.get('tag_list', []))


@given("get next untagged component api is running")
def running_get_untagged_component_api(context):
    """Wait for the get next untagged component REST API to be available."""
    if not context.is_get_untagged_component_service_running(context):
        context.wait_for_get_untagged_component_service(context, 60)


def get_next_untagged_component_url(context, ecosystem):
    """Construct URL for get next untagged component REST API call."""
    return urljoin(context.coreapi_url,
                   'api/v1/get-next-component/{e}'.format(e=ecosystem))


def get_next_untagged_component(context, ecosystem, use_token):
    """Call API endpoint get next untagged component"""
    if use_token:
        context.response = requests.post(get_next_untagged_component_url(context, ecosystem),
                                         headers=authorization(context))
    else:
        context.response = requests.post(get_next_untagged_component_url(context, ecosystem))


@when("I access get next untagged component for ecosystem {ecosystem} without authorization token")
def get_next_untagged_component_without_token(context, ecosystem):
    """get next untagged component for given ecosystem REST API call."""
    get_next_untagged_component(context, ecosystem, False)


@when("I access get next untagged component for ecosystem {ecosystem} with authorization token")
def get_next_untagged_component_with_token(context, ecosystem):
    """get next untagged component for given ecosystem REST API call."""
    get_next_untagged_component(context, ecosystem, True)


@then("I should get 401 status code as response for next untagged component")
def check_status_code_for_get_next_untagged_component(context):
    """Check get next untagged component require authorization tokens"""
    assert context.response.status_code == 401


@then("I should get a 200 status code and component as {response} type")
def check_get_next_untagged_component_response(context, response):
    """Check that response contains the component"""
    data = context.response.json()
    assert context.response.status_code == 200
    assert data.__class__.__name__ == response
    if type(data) is str:  # for maven ecosystem
        assert len(data) != 0
        assert data.find(':') != -1
    elif type(data) is dict:  # for unsupported ecosystem
        assert 'error' in data
        assert data.get('error') == "No package found for tagging."


@when("I access set tags api endpoint without authorization token")
def post_invalid_input_to_set_tags_without_token(context):
    input_json = {"ecosystem": "maven"}  # component and tags are missing.
    context.response = requests.post(context.coreapi_url + 'api/v1/set-tags',
                                     data=input_json)


@then("I should get 401 status code as response for set tags api endpoint")
    assert context.response.status_code == 401


@when("I post invalid json input to the set tags endpoint")
def post_invalid_input_to_set_tags(context):
    input_json = {"ecosystem": "maven"}  # component and tags are missing.
    context.response = requests.post(context.coreapi_url + 'api/v1/set-tags',
                                     data=input_json,
                                     headers=authorization(context))


@then("I should get a 400 status code as response")
def check_response_for_invalid_input_to_set_tags(context):
    assert context.response.status_code == 400
