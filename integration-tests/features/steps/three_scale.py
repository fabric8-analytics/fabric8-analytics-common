#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests 3scale registration endpoint."""
import requests
import json

from behave import given, then, when
from urllib.parse import urljoin

from src.authorization_tokens import *

# How to mock the response 
# How tp set the url

@given('3scale staging pod is running')
def running_3scale_api_register(context):
    return context.is_3scale_staging_running
    

def three_scale_register_url(context):
    """Construct URL for 3scale REST API call."""
    return urljoin(context.threescale_url)


def register_3scale(context, use_token):
    """Call API endpoint get_route."""
    if use_token:
        data = {"auth_token": authorization(context)}
        headers = {'Content-type': 'application/json'}
        context.response = requests.post(three_scale_register_url(context),
                        data=json.dumps(data), headers=headers)
    else:
        context.response = requests.get(three_scale_register_url(context))


@when("I access get_route API end point for 3scale without authorization")
def register_3scale_without_token(context):
    """Tries to register to 3scale without authentication"""
    register_3scale(context, False)

@then('I should get 401 status code as response for master tag list')
def check_status_code_3scale_registration(context):
    """Check 3scale registration route require authorization tokens."""
    assert context.response.status_code == 401


@when("When I make a post call with proper authentication token")
def register_3scale_with_token(context):
    """Tries to register to 3scale with authentication"""
    register_3scale(context, True)


@then('I should get json object that contains prod_url, user_key and staging_url')
def validate_result_post_registration(context):
    """Check that json response the appropriate data."""
    json_data = context.response.json()
    # assert json_data["endpoints"]["prod_url"] ==
    # assert json_data["endpoints"]["stage_url"] ==
    # assert json_data["user_key"] == 
