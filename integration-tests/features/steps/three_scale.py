#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests 3scale registration endpoint."""
import requests
import json

from behave import given, then, when
from urllib.parse import urljoin

from src.authorization_tokens import *


@given('3scale staging pod is running')
def running_3scale_api_register(context):
    """Check if 3scale pod is running."""
    return context.is_3scale_staging_running


def three_scale_register_url(context):
    """Construct URL for 3scale REST API call."""
    return urljoin(context.threescale_url, 'get-route')


def get_data(context):
        """Construct data for 3scale REST API POST call."""
        token = authorization(context).get("Authorization", None)
        token = token.split("Bearer ")[-1]
        data = {
            "auth_token": token,
            "service_id": context.service_id[:-1]
        }
        return data


def get_headers():
    """Construct headers for 3scale REST API POST call."""
    return {'Content-type': 'application/json'}


def register_3scale(context, use_token):
    """Call API endpoint get_route."""
    if use_token:
        data = get_data(context)
        headers = get_headers()
        context.response = requests.post(three_scale_register_url(context),
                                         data=json.dumps(data),
                                         headers=headers)
    else:
        headers = get_headers()
        context.response = requests.post(three_scale_register_url(context),
                                         headers=headers)


@when("I access get_route API end point for 3scale without authorization")
def register_3scale_without_token(context):
    """Try to register to 3scale without authentication."""
    register_3scale(context, False)


@then('I should get 404 status code as response')
def check_status_code_3scale_registration(context):
    """Check 3scale registration route require authorization tokens."""
    assert context.response.status_code == 404


@when("I make a post call with proper authentication token")
def register_3scale_with_token(context):
    """Try to register to 3scale with authentication."""
    register_3scale(context, True)


@then('I should get json object')
def validate_result_post_registration(context):
    """Check that json response the appropriate data."""
    json_data = context.response.json()
    assert context.response.status_code == 200
    assert len(json_data) is not 0

    user_key = json_data.get("user_key", None)
    assert user_key is not None

    endpoints = json_data.get("endpoints", None)
    assert endpoints is not None

    prod_url = endpoints.get("prod", None)
    assert prod_url is not None
    assert prod_url.startswith("http://") is True

    stage_url = endpoints.get("stage", None)
    assert stage_url is not None
    assert stage_url.startswith("http://") is True
