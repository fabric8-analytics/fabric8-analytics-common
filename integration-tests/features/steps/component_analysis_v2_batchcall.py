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


def check_for_registered_user_feilds(item):
    """I should check no registered user feilds are exposed."""
    if "exploitable_vulnerabilities_count" in item:
        raise Exception("Field exploitable_vulnerabilities_count Exposed in"
                        " Free user result")
    if "vendor_package_link" in item:
        raise Exception("Field vendor_package_link has been exposed for free user")


@when("I start CA batch call for {file} {user_key} user_key")
def start_batch_call(context, file, user_key):
    """Start CA Batch call."""
    use_user_key = parse_token_clause(user_key)
    perform_CA_batch_call(context, use_user_key, file)


@then('I should be able to validate all the feilds or vulnerablities in the result')
def find_vulnerablities(context):
    """I should be able to find some Vulnerablities."""
    json_data = context.response.json()
    for single_item in json_data:
        if "vulnerability" in single_item:
            assert "package" in single_item, "No package Found!"
            assert "version" in single_item, "No Version Found!"
            assert "package_unknown" in single_item
            assert "message" in single_item, "No message found"
            assert "highest_severity" in single_item, "No severity found"
            assert "known_security_vulnerability_count" in single_item
            assert "security_advisory_count" in single_item
            assert "recommended_versions" in single_item, "No Recommended version found"
            assert "registration_link" in single_item, "No snyk registration link found"
            validate_vuln_feilds(single_item['vulnerability'])
        elif single_item["package_unknown"]:
            assert "name" in single_item
            assert "version" in single_item
        else:
            assert "recommendation" in single_item
            assert "package_unknown" in single_item
            assert "package" in single_item
            assert "version" in single_item
            assert single_item['recommendation'] == {}


@then('I should find package {package} {version} has no recommendation')
def find_package_versions(context, package, version):
    """I should find a particular package has no recommendation."""
    json_data = context.response.json()
    for item in json_data:
        try:
            if item['package'] == package and item['version'] == version:
                assert item['recommendation'] == {}
        except KeyError:
            pass


@then('I should find package {package} {version} has {rec_version} recommended version')
def find_recommended_version(context, package, version, rec_version):
    """I should be able to validate recommended version."""
    json_data = context.response.json()
    for item in json_data:
        try:
            if item['package'] == package and item['version'] == version:
                assert item['recommended_versions'] == rec_version
        except KeyError:
            pass


@then('I should find snyk id {vid} and {score} for package {package} and version {version}')
def find_snyk_id(context, package, version, vid, score):
    """I should be able to find snyk vuln id."""
    json_data = context.response.json()
    for item in json_data:
        try:
            if item['package'] == package and item['version'] == version:
                find_synk_vuln_id(item, vid, score)
        except KeyError:
            pass


@then('I should find snyk id {vid} for package {package} and version {version} as private')
def find_for_private_vuln(context, package, version, vid):
    """Find for private vulnerability in result."""
    json_data = context.response.json()
    for item in json_data:
        try:
            if item['package'] == package and item['version'] == version:
                find_privates(item, vid)
        except KeyError:
            pass


@then('I should find one or more unknown packages in result')
def check_if_package_exists(context):
    """I should not find a particular package in result."""
    json_data = context.response.json()
    for item in json_data:
        is_unknown = item['package_unknown']
        if is_unknown:
            assert "name" in item
            assert "version" in item


@then('I should not find any vulnerablities in result')
def check_for_no_vuln(context):
    """I should not find any vulnerabilities in result."""
    json_data = context.response.json()
    for item in json_data:
        assert 'package' in item
        assert 'version' in item
        assert "package_unknown" in item
        assert item["package_unknown"] is False
        assert 'recommendation' in item, "{} has vulnerablity".format(item['package'])
        assert item['recommendation'] == {}


@then('I should not find any registered user fields')
def check_for_exposed(context):
    """Exposed fields for free user check."""
    json_data = context.response.json()
    for item in json_data:
        check_for_registered_user_feilds(item)
