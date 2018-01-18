#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests 3scale registration endpoint."""
import requests
import json

from behave import given, then, when
from urllib.parse import urljoin

from src.attribute_checks import *
from src.authorization_tokens import *


@given('3scale staging pod is running')
def running_3scale_api_register(context):
    """Check if 3scale pod is running."""
    return context.is_3scale_staging_running


def three_scale_register_url(context):
    """Construct URL for 3scale REST API call."""
    return urljoin(context.threescale_url, 'get-route')


def get_data(context, use_token):
        """Construct data for 3scale REST API POST call."""
        if use_token:
            token = authorization(context).get("Authorization", None)
            token = token.split("Bearer ")[-1]
            data = {
                "auth_token": token,
                "service_id": context.service_id[:-1]
            }
        else:
            data = {
                "service_id": context.service_id[:-1]
            }
        return data


def get_headers():
    """Construct headers for 3scale REST API POST call."""
    return {'Content-type': 'application/json'}


def register_3scale(context, use_token):
    """Call API endpoint get_route."""
    if use_token:
        data = get_data(context, use_token)
        headers = get_headers()
        context.response = requests.post(three_scale_register_url(context),
                                         data=json.dumps(data),
                                         headers=headers)
    else:
        data = get_data(context, use_token)
        headers = get_headers()
        context.response = requests.post(three_scale_register_url(context),
                                         data=json.dumps(data),
                                         headers=headers)


@when("I access get_route API end point for 3scale without authorization")
def register_3scale_without_token(context):
    """Try to register to 3scale without authentication."""
    register_3scale(context, False)


@when("I make a post call to 3scale with proper authentication token")
def register_3scale_with_token(context):
    """Try to register to 3scale with authentication."""
    register_3scale(context, True)


@then('I should get proper 3scale response')
def validate_result_post_registration(context):
    """Check that json response contains appropriate data."""
    json_data = context.response.json()
    assert context.response.status_code == 200
    assert json_data

    check_attribute_presence(json_data, "user_key")
    endpoints = check_and_get_attribute(json_data, "endpoints")

    prod_url = check_and_get_attribute(endpoints, "prod")
    assert prod_url.startswith("https://")

    # stage_url = check_and_get_attribute(endpoints, "stage")
    # assert stage_url.startswith("http://")
