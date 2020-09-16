"""Tests for API endpoints that performs User Management."""
import requests

import time

from behave import then, when
from urllib.parse import urljoin

from src.parsing import parse_token_clause


def user_management_url(context):
    """Construct url for user Management."""
    return urljoin(context.core_v2_api_url,
                   '/user')


def make_post_call(context, use_user_key):
    """Make the post call on the user management api."""
    context.duration = None
    start_time = time.time()

    url = user_management_url(context)
    parms = {'user_key': context.three_scale_preview_user_key}

    if use_user_key:
        context.response = requests.post(url, params=parms)
        if context.response.status_code == 429:
            raise Exception("429 Limit excceded")
    else:
        context.response = requests.post(url)
    end_time = time.time()
    context.duration = end_time - start_time


def make_put_call(context, use_user_key, snyk_token, uuid):
    """Make the put call on the user management api."""
    context.duration = None
    start_time = time.time()

    url = user_management_url(context)
    parms = {'user_key': context.three_scale_preview_user_key}
    data = {
        "snyk_api_token": snyk_token,
        "user_id": uuid
    }

    if use_user_key:
        context.response = requests.put(url, params=parms, json=data)
        if context.response.status_code == 429:
            raise Exception("429 Limit excceded")
    else:
        context.response = requests.put(url, json=data)
    end_time = time.time()
    context.duration = end_time - start_time


def make_get_call(context, use_user_key, uuid):
    """Make the get call on the user management api."""
    context.duration = None
    start_time = time.time()
    get_url = urljoin(context.core_v2_api_url, '/user/{}'.format(uuid))
    print(get_url)
    parms = {'user_key': context.three_scale_preview_user_key}

    if use_user_key:
        context.response = requests.get(get_url, params=parms)
        if context.response.status_code == 429:
            raise Exception("429 Limit excceded")
    else:
        context.response = requests.get(get_url)
    end_time = time.time()
    context.duration = end_time - start_time


@then('I should be able to validate post or put request')
def validate_response_put_post(context):
    """Validate the data in the response."""
    if context.response.status_code == 200:
        json_data = context.response.json()
        assert "user_id" in json_data
        context.uuid = json_data['user_id']


@then('I should be able to validate the get request')
def validate_get_response(context):
    """Validate put response."""
    json_data = context.response.json()
    code = context.response.status_code
    assert "status" in json_data
    if code == 404:
        assert "message" in json_data
    else:
        assert "user_id" in json_data


@then('I should get status as registered')
def get_satus_registered(context):
    """Validate if the status is registered."""
    json_data = context.response.json()
    assert json_data['status'] == "REGISTERED"


@then('I should get user not found message')
def user_not_found(context):
    """Validate user not found."""
    json_data = context.response.json()
    assert json_data['message'] == "User not found"


@when('I request user api for new UUID {user_key} user_key')
def make_uuid_request(context, user_key):
    """Start a post request on API."""
    use_user_key = parse_token_clause(user_key)
    make_post_call(context, use_user_key)


@when('I try the put call with snyk token and id {user} user_key')
def make_put_request(context, user):
    """Start a put call on API."""
    use_user_key = parse_token_clause(user)
    token = context.valid_synk_token
    uuid = context.uuid
    make_put_call(context, use_user_key, token, uuid)


@when('I try to get user {user_key} user_key')
def make_get_request(context, user_key):
    """Start a get call on API."""
    use_user_key = parse_token_clause(user_key)
    uuid = context.uuid
    make_get_call(context, use_user_key, uuid)


@when('I try the put call with invalid snyk token {user} user_key')
def make_invalid_put_request(context, user):
    """Start a put call on API."""
    use_user_key = parse_token_clause(user)
    token = "6e1dafe6-inva-lidd-tokk-endf25fa04ae"
    uuid = context.uuid
    make_put_call(context, use_user_key, token, uuid)


@when('I try to get invalid user {user_key} user_key')
def make_invalid_get_request(context, user_key):
    """Start a get call on API."""
    use_user_key = parse_token_clause(user_key)
    uuid = "really-invalid-user-guess"
    make_get_call(context, use_user_key, uuid)
