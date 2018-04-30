#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests gemini api endpoints."""
import requests
import json

from behave import given, then, when

from src.parsing import *
from src.json_utils import *
from src.authorization_tokens import *


@given('Gemini service is running')
def running_gemini_api(context):
    """Check if gemini pod is running."""
    return context.is_gemini_api_running


@given('Gemini service git url is {url}')
def set_git_url(context, url):
    """Set git url for test."""
    context.url = url


@given('Gemini service git sha is {sha}')
def set_git_url(context, sha):
    """Set git sha for test."""
    context.sha = sha


@when('I {method} to Gemini API {endpoint}')
@when('I {method} to Gemini API {endpoint} {token} authorization token')
def call_backbone_api(context, method="get", endpoint="/api/v1/register", token="without"):
    """Get or post data to gemini API."""
    use_token = parse_token_clause(token)
    headers = {}
    if use_token:
        headers = authorization(context)
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json'

    if method == 'post':
        content = {
            'git-url': context.url,
            'git-sha': context.sha
        }
        context.response = requests.post('{}/{}'.format(context.gemini_api_url, endpoint),
                                         json=json.loads(content), headers=headers)
    else:
        api_url = "{api_url}/{endpoint}?git-url={git_url}&git-sha={git_sha}".format(
            api_url=context.gemini_api_url,
            endpoint=endpoint,
            git_url=context.url,
            git_sha=context.sha)
        context.response = requests.get(api_url, headers=headers)
