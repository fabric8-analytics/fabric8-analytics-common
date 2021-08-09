"""Tests for API endpoints that performs v2 Vunerablity analysis route."""
import requests

import time
import json

from behave import then, when
from urllib.parse import urljoin

from src.parsing import parse_token_clause
from component_analysis_v2_batchcall import get_packages_from_json


def vulnerability_analysis_batch_call_url(context):
    """Construct url for call."""
    return urljoin(context.core_v2_api_url,
                   '/api/v2/vulnerability-analysis/')


def perform_Vuln_batch_call(context, use_user_key, packages_file):
    """Perform Batch Call for vulnerability-analysis."""
    context.duration = None
    start_time = time.time()

    url = vulnerability_analysis_batch_call_url(context)
    parms = {'user_key': context.three_scale_preview_user_key}

    data = get_packages_from_json(packages_file)

    if use_user_key:
        context.response = requests.post(url, params=parms, json=data)
        if context.response.status_code == 429:
            raise Exception("429 Limit excceded")
    else:
        context.response = requests.post(url, json=data)
    end_time = time.time()
    context.duration = end_time - start_time


def validate_vuln_feilds(vul):
    """Validate feilds present in vulnerability."""
    for vuln in vul:
        assert "id" in vuln
        assert "severity" in vuln
        assert "title" in vuln
        assert "url" in vuln
        assert "fixed_in" in vuln

def validate_vuln_basic_feilds(single_item):
    """Validate Basic Vulnerabity feilds."""
    if single_item['vulnerabilities'] != []:
        assert "package" in single_item, "No package Found!"
        assert "version" in single_item, "No Version Found!"
        validate_vuln_feilds(single_item['vulnerabilities'])
    else:
        assert "package" in single_item
        assert "version" in single_item
        assert single_item['vulnerabilities'] == []

def validate_all_feilds(json_data):
    """Validate all the feilds that are present in result."""
    for single_item in json_data:
        validate_vuln_basic_feilds(single_item)

def match_pkg_ver_key_val(item, pkg, ver, key, val):
    """Validate the package and version"""
    try:
        if item['package'] == pkg and item['version'] == ver:
            assert item['vulnerabilities'][key] == val
    except KeyError:
        pass

def match_fixed_in(item, value_to_match):
    """Match value preset in fixed in"""
    assert value_to_match in item['vulnerabilities']['fixed_in'], 'The Specified version doesnt exist'


@when("I start vulnerablity analysis for {file} {user_key} user_key")
def start_batch_call(context, file, user_key):
    """Start vulnerablity analysis Batch call."""
    use_user_key = parse_token_clause(user_key)
    perform_Vuln_batch_call(context, use_user_key, file)

@then('I should be able to find all feilds in the result')
def find_vulnerablities(context):
    """I should be able to find some Vulnerablities."""
    json_data = context.response.json()
    validate_all_feilds(json_data)

@when('I should find pkg {package} and version {version} with vulnerablity {key} {value} in Result')
def match_package_version_id(context, package, version, key, value):
    """Match the package and version provided."""
    json_data = context.response.json()

    # Acceptable Keys are ("id|severity|title|url")

    for single_item in json_data:
        match_pkg_ver_key_val(single_item, pkg=package, ver=version, key=key, val=value)


