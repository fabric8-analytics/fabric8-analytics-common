"""Tests for API endpoints that performs v2 component analysis."""
import requests

import time
import json

from behave import then, when
from urllib.parse import urljoin

from src.parsing import parse_token_clause


def component_analysis_batch_call_url(context):
    """Construct url for batch call."""
    return urljoin(context.core_v2_api_url,
                   '/api/v2/component-analyses')


def get_packages_from_json(file):
    """Get the json data from the file for batch call."""
    filename = 'data/batch_call/{file}'.format(file=file)
    data = None
    try:
        f = open(filename, 'r')
        data = json.load(f)
    except IOError:
        raise Exception('There is no file named: {file}'.format(file=filename))
    return data


def perform_CA_batch_call(context, use_user_key, packages_file):
    """Perform Batch Call for component analysis."""
    context.duration = None
    start_time = time.time()

    url = component_analysis_batch_call_url(context)
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
        assert "cvss" in vuln
        assert "is_private" in vuln
        assert "cwes" in vuln
        assert "cvss_v3" in vuln
        assert "severity" in vuln
        assert "title" in vuln
        assert "url" in vuln
        assert "cve_ids" in vuln
        assert "fixed_in" in vuln


def find_synk_vuln_id(item, vid, score):
    """Find and validate vuln id and score."""
    for i in item['vulnerability']:
        if i["id"] == vid and str(i["cvss"]) == score:
            return
    raise Exception("Cannot find id {}".format(vid))


def find_privates(item, vid):
    """Find private vulns in result."""
    for i in item['vulnerability']:
        if i["id"] == vid and i['is_private']:
            return
    raise Exception("No private vulnerability found for id {}".format(vid))


@when("I start CA batch call for {file} {user_key} user_key")
def start_batch_call(context, file, user_key):
    """Start CA Batch call."""
    use_user_key = parse_token_clause(user_key)
    perform_CA_batch_call(context, use_user_key, file)


@then('I should be able to validate all the feilds or vulnerablities in the result')
def find_vulnerablities(context):
    """I should be able to find some Vulnerablities."""
    json_data = context.response.json()
    for item in json_data:
        assert "package" in item, "No package Found!"
        assert "version" in item, "No Version Found!"
        if "vulnerability" in item:
            assert "message" in item, "No message found"
            assert "highest_severity" in item, "No severity found"
            assert "known_security_vulnerability_count" in item
            assert "security_advisory_count" in item
            assert "recommended_versions" in item, "No Recommended version found"
            assert "registration_link" in item, "No snyk registration link found"
            validate_vuln_feilds(item['vulnerability'])
        else:
            assert "recommendation" in item
            assert item['recommendation'] == {}


@then('I should find package {package} {version} has no recommendation')
def find_package_versions(context, package, version):
    """I should find a particular package has no recommendation."""
    json_data = context.response.json()
    for item in json_data:
        if item['package'] == package and item['version'] == version:
            assert item['recommendation'] == {}


@then('I should find package {package} {version} has {rec_version} recommended version')
def find_recommended_version(context, package, version, rec_version):
    """I should be able to validate recommended version."""
    json_data = context.response.json()
    for item in json_data:
        if item['package'] == package and item['version'] == version:
            assert item['recommended_versions'] == rec_version


@then('I should find snyk id {vid} and {score} for package {package} and version {version}')
def find_snyk_id(context, package, version, vid, score):
    """I should be able to find snyk vuln id."""
    json_data = context.response.json()
    for item in json_data:
        if item['package'] == package and item['version'] == version:
            find_synk_vuln_id(item, vid, score)


@then('I should find snyk id {vid} for package {package} and version {version} as private')
def find_for_private_vuln(context, package, version, vid):
    """Find for private vulnerability in result."""
    json_data = context.response.json()
    for item in json_data:
        if item['package'] == package and item['version'] == version:
            find_privates(item, vid)


@then('I should not find package {package} with version {version} in result')
def check_if_package_exists(context, package, version):
    """I should not find a particular package in result."""
    json_data = context.response.json()
    for item in json_data:
        if item['package'] == package and item['version'] == version:
            raise Exception("Package {} with version {} found in result".format(package, version))
