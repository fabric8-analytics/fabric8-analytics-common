#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests gemini api endpoints."""
import requests

from behave import given, when, then
from urllib.parse import urljoin

from src.parsing import parse_token_clause
from src.authorization_tokens import authorization
from src.attribute_checks import check_and_get_attribute
from src.utils import read_data_gemini
import os
import json


@given('Gemini service is running')
def running_gemini_api(context):
    """Check if gemini pod is running."""
    return context.is_gemini_api_running


@given('Gemini service git url is {url}')
def set_git_url(context, url):
    """Set Git URL for test."""
    context.url = url


@given('Gemini service git sha is {sha}')
def set_git_sha(context, sha):
    """Set Git SHA for test."""
    context.sha = sha


@given('Gemini service epv list is {epv_list}')
def set_epv_list(context, epv_list):
    """Set epv_list for test."""
    context.epv_list = epv_list


@given('Gemini service dependency files are set')
def set_dependency_files(context):
    """Set dependency_files for test."""
    path_to_direct_file = os.path.abspath('data/gemini_scan_data/direct-dependencies.txt')
    path_to_transitive_file = os.path.abspath('data/gemini_scan_data/transitive-dependencies.txt')
    context.dependency_files = list()
    with open(path_to_direct_file, 'rb') as f:
        context.dependency_files.append((
            "dependencyFile[]",
            (
                'direct-dependencies.txt',
                f.read(),
                'text/plain'
            )
        ))
    with open(path_to_transitive_file, 'rb') as f:
        context.dependency_files.append((
            "dependencyFile[]",
            (
                'transitive-dependencies.txt',
                f.read(),
                'text/plain'
            )
        ))


@when('I access the {endpoint} endpoint of Gemini service')
@when('I access the {endpoint} endpoint of Gemini service {token} authorization token')
def access_gemini_url(context, endpoint, token="without"):
    """Access the Gemini service API using the HTTP GET method."""
    url = urljoin(context.gemini_api_url, endpoint)
    use_token = parse_token_clause(token)
    headers = {}
    if use_token:
        headers = authorization(context)
    context.response = requests.get(url, headers=headers)


@when('I access the {endpoint} endpoint of Gemini service for {parameter} report {history}')
@when('I access the {endpoint} endpoint of Gemini service for {parameter} report')
def access_stacks_report_list(context, endpoint, parameter='', history=''):
    """Access the Gemini stacks-report/list API endpoint using the HTTP GET method."""
    url = urljoin(context.gemini_api_url, '{ep}/{param}'.format(ep=endpoint, param=parameter))
    context.response = requests.get(url)
    context.history = True if history == 'history' else False


@when('I call the {endpoint} endpoint of Gemini service using the HTTP PUT method')
def access_gemini_url_put_method(context, endpoint):
    """Access the Gemini service API using the HTTP PUT method."""
    url = urljoin(context.gemini_api_url, endpoint)
    context.response = requests.put(url)


@when('I call the {endpoint} endpoint of Gemini service using the HTTP PATCH method')
def access_gemini_url_patch_method(context, endpoint):
    """Access the Gemini service API using the HTTP PATCH method."""
    url = urljoin(context.gemini_api_url, endpoint)
    context.response = requests.patch(url)


@when('I call the {endpoint} endpoint of Gemini service using the HTTP DELETE method')
def access_gemini_url_delete_method(context, endpoint):
    """Access the Gemini service API using the HTTP DELETE method."""
    url = urljoin(context.gemini_api_url, endpoint)
    context.response = requests.delete(url)


@when('I call the {endpoint} endpoint of Gemini service using the HTTP HEAD method')
def access_gemini_url_head_method(context, endpoint):
    """Access the Gemini service API using the HTTP HEAD method."""
    url = urljoin(context.gemini_api_url, endpoint)
    context.response = requests.head(url)


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
    headers['git-url'] = "https://github.com/heroku/node-js-sample.git"

    if method == 'post':
        content = {
            'git-url': context.url,
            'git-sha': context.sha
        }

        if endpoint == "/api/v1/user-repo/notify":
            content.update({
                "epv_list": context.epv_list
            })
        url = '{}/{}'.format(context.gemini_api_url, endpoint)
        if endpoint == '/api/v1/user-repo/scan':
            content = read_data_gemini()
            headers['git-url'] = "https://github.com/heroku/node-js-sample.git"
            headers.pop('Accept', None)
            context.response = requests.post(url, data=json.dumps(content),
                                             headers=headers)
        else:
            context.response = requests.post(url, json=content, headers=headers)
    else:
        api_url = "{api_url}/{endpoint}?git-url={git_url}&git-sha={git_sha}".format(
            api_url=context.gemini_api_url,
            endpoint=endpoint,
            git_url=context.url,
            git_sha=context.sha)
        context.response = requests.get(api_url, headers=headers)


def check_cve_count(cve_count, cves):
    """Check if number of returned CVEs is expected."""
    assert cve_count is not None
    assert int(cve_count) == int(cves), \
        "{exp} CVEs expected, but {found} was found".format(exp=cves, found=cve_count)


@then('I should find {cves} CVEs for package {p} version {v} from ecosystem {e} in dependencies')
def check_cves_for_epv(context, cves, p, v, e):
    """Check number of CVEs reported for given e/p/v in dependencies."""
    response = context.response.json()
    depencencies = check_and_get_attribute(response, "dependencies")

    for dependency in depencencies:
        cve_count = check_and_get_attribute(dependency, "cve_count")
        ecosystem = check_and_get_attribute(dependency, "ecosystem")
        package = check_and_get_attribute(dependency, "name")
        version = check_and_get_attribute(dependency, "version")
        if ecosystem == e and package == p and version == v:
            check_cve_count(cve_count, cves)
            return
    raise Exception("{e}/{p}/{v} was not found".format(e=e, p=p, v=v))


@then('I should get a valid report')
def check_valid_report(context):
    """Check if the stacks report is a valid one."""
    response = context.response.json()
    if context.history:
        assert(isinstance(response['objects'], list))
    else:
        assert(isinstance(response, dict))
