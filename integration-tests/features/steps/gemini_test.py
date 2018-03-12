#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests 3scale registration endpoint."""
import requests
import json

from behave import given, then, when
from urllib.parse import urljoin

from src.attribute_checks import *

@given('gemini staging pod is running')
def running_gemini_staging(context):
    """Check if 3scale pod is running."""
    return context._is_gemini_server_running


def gemini_register_url(context):
    """Construct URL for 3scale REST API call."""
    return urljoin(context.gemini_server_url, 'register')


def get_headers():
    """Construct headers for 3scale REST API POST call."""
    return {'Content-type': 'application/json'}


def request_register(context, use_token):
    """Call API endpoint get_route."""
    data = {
            "email_ids": "abcd@gmail.com",
            "git_sha": "somesha",
            "git_url": "test"
    }
    headers = get_headers()
    context.response = requests.post(gemini_register_url(context),
                                     data=json.dumps(data),
                                     headers=headers)
