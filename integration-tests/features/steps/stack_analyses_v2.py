# Copyright © 2020 Red Hat Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Dharmendra G Patel <dhpatel@redhat.com>
#
"""End to end tests for Stack Analyses V2 API endpoints."""
import os
import time
import logging
import requests
from behave import when, then
from urllib.parse import urljoin
from src.attribute_checks import check_attribute_presence
from src.parsing import parse_token_clause, parse_valid_clause
from src.attribute_checks import check_timestamp
from src.json_utils import get_value_using_path
from src.stack_analysis_common import get_json_data, check_frequency_count


logger = logging.getLogger(__file__)

ECOSYSTEM_TO_MANIFEST_NAME_MAP = {
    'pypi': 'pylist.json',
    'npm': 'npmlist.json',
    'maven': 'dependencies.txt'
    'golang': 'golist.json'
}


def get_endpoint(context):
    """Get endpoint for the stack analysis v2."""
    return urljoin(context.threescale_preview_url, '/api/v2/stack-analyses')


def post_request(context, ecosystem, manifest, with_user_key, with_valid_user_key,
                 show_transitives, is_user_registered=False, is_invalid=False):
    """Send stack analyses v2 post request based on params."""
    logger.debug('ecosystem: {} manifest: {} with_user_key: {} '
                 'with_valid_user_key: {}'.format(ecosystem, manifest, with_user_key,
                                                  with_valid_user_key))
    context.manifest = manifest
    if is_invalid:
        is_user_registered = True
        uuid = 'e48793e0-681e-45ce-b4d0-0fd992df1095g'
    else:
        uuid = context.uuid
    # set default values
    print(is_invalid)
    files = {}
    data = {'show_transitive': show_transitives}
    # Add ecosystem if not None
    if ecosystem != 'None':
        data['ecosystem'] = ecosystem
    # Read manifest if not None
    if manifest != 'None':
        filename = 'data/{}'.format(manifest)
        files['manifest'] = (ECOSYSTEM_TO_MANIFEST_NAME_MAP.get(ecosystem, 'invalid_name.json'),
                             open(filename, 'rb'))
        data['file_path'] = os.path.abspath(os.path.dirname(filename))

    if with_user_key and is_user_registered:
        if with_valid_user_key:
            headers = {"uuid": uuid}
            print(headers)
            params = {'user_key': context.three_scale_preview_user_key}
        else:
            params = {'user_key': 'INVALID_USER_KEY_FOR_TESTING'}
        logger.debug('POST {} files: {} data: {} params: {}'.format(get_endpoint(context),
                                                                    files, data, params))
        response = requests.post(get_endpoint(context), headers=headers, files=files, data=data,
                                 params=params)
    elif with_user_key:
        if with_valid_user_key:
            params = {'user_key': context.three_scale_preview_user_key}
        else:
            params = {'user_key': 'INVALID_USER_KEY_FOR_TESTING'}
        logger.debug('POST {} files: {} data: {} params: {}'.format(get_endpoint(context),
                                                                    files, data, params))
        response = requests.post(get_endpoint(context), files=files, data=data,
                                 params=params)
    else:
        response = requests.post(get_endpoint(context), files=files, data=data)

    logger.debug('status_code: {} response: {}'.format(response.status_code, response.text))
    context.response = response


@when('I wait for stack analysis v2 to finish {token} user key')
@when('I wait for stack analysis v2 to finish {token} user key {user} uuid')
def wait_for_completion(context, token='without', user='without'):
    """Try to wait for the stack analysis to be finished.

    This step assumes that stack analysis has been started previously and
    thus that the request id is known

    Current API implementation returns just three HTTP codes:
    200 OK : analysis is already finished
    202 Accepted: analysis is started or is in progress (or other state!)
    401 UNAUTHORIZED : missing or improper user key
    408 Timeout: Request timeout.
    """
    context.duration = None
    start_time = time.time()

    timeout = context.stack_analysis_timeout  # in seconds
    sleep_amount = 10  # we don't have to overload the API with too many calls
    with_user_key = parse_token_clause(token)
    is_user_registered = parse_token_clause(user)

    id = context.response.json().get('id')
    context.stack_analysis_id = id
    logger.debug('SA V2 Request id: {}'.format(id))

    url = urljoin(get_endpoint(context) + '/', id)
    logger.debug('Get API url: {}'.format(url))

    for _ in range(timeout // sleep_amount):
        if with_user_key and is_user_registered:
            uuid = context.uuid
            headers = {"uuid": uuid}
            params = {'user_key': context.three_scale_preview_user_key}
            context.response = requests.get(url, headers=headers, params=params)
        elif with_user_key:
            params = {'user_key': context.three_scale_preview_user_key}
            context.response = requests.get(url, params=params)
        else:
            context.response = requests.get(url)
        status_code = context.response.status_code
        logger.debug('status_code: {}'.format(status_code))
        if status_code == 200:
            break
        # 429 (Rate Limit) code should be checked later
        elif status_code == 429:
            break
        # 403 code should be checked later
        elif status_code == 403:
            break
        # 401 code should be checked later
        elif status_code == 401:
            break
        elif status_code != 202:
            raise Exception('Bad HTTP status code {c}'.format(c=status_code))
        time.sleep(sleep_amount)
    else:
        raise Exception('Timeout waiting for the stack analysis results')

    end_time = time.time()
    # compute the duration
    # plase note that duration==None in case of any errors (which is to be expected)
    context.duration = end_time - start_time


def check_rate_limit(context, ecosystem, manifest, rate, with_user_key, with_valid_user_key):
    """Call API endpoint to v2 analysis for component."""
    context.duration = None
    start_time = time.time()
    for _ in range(rate):
        post_request(context, ecosystem, manifest, with_user_key, with_valid_user_key)
        # break the loop if rate limit exceeded
        if context.response.status_code == 429:
            break
    end_time = time.time()
    # compute the duration
    # Note that duration==None in case of any errors (which is to be expected)
    context.duration = end_time - start_time


def get_analyzed_components(context):
    """Return all analyzed components from the deserialized JSON file."""
    json_data = get_json_data(context)

    components = get_value_using_path(json_data, 'analyzed_dependencies')
    assert components is not None

    return components


def check_equal_expectation_for_array(context, path, expected):
    """Check equality check for array object count."""
    json_data = get_json_data(context)
    actual_count = len(get_value_using_path(json_data, path))
    assert actual_count == expected, \
        "Found {} object(s) at {}, but {} is expected".format(
            actual_count, path, expected)


def check_equal_expectation_for_int(context, path, expected):
    """Check equality check for array object count."""
    json_data = get_json_data(context)
    actual_count = get_value_using_path(json_data, path)
    assert actual_count == expected, \
        "Found {} object(s) at {}, but {} is expected".format(
            actual_count, path, expected)


def check_vulenrability_attributes(vul):
    """Verify all attributes are present for given vulenerability."""
    check_attribute_presence(vul, 'id')
    check_attribute_presence(vul, 'url')
    check_attribute_presence(vul, 'cvss')
    check_attribute_presence(vul, 'cwes')
    check_attribute_presence(vul, 'title')
    check_attribute_presence(vul, 'cve_ids')
    check_attribute_presence(vul, 'cvss_v3')
    check_attribute_presence(vul, 'severity')


def check_premium_vuln_attributes(vul):
    """Verify all premium attributes present in result."""
    check_attribute_presence(vul, 'description')
    check_attribute_presence(vul, 'exploit')
    check_attribute_presence(vul, 'fixable')
    check_attribute_presence(vul, 'fixed_in')
    check_attribute_presence(vul, 'malicious')
    check_attribute_presence(vul, 'patch_exists')
    check_attribute_presence(vul, 'references')


def check_dependency_attributes(ad):
    """Verify all attributes are present for given dependencies."""
    check_attribute_presence(ad, 'url')
    check_attribute_presence(ad, 'name')
    check_attribute_presence(ad, 'github')
    check_attribute_presence(ad, 'version')
    check_attribute_presence(ad, 'licenses')
    check_attribute_presence(ad, 'ecosystem')
    check_attribute_presence(ad, 'dependencies')
    check_attribute_presence(ad, 'latest_version')
    check_attribute_presence(ad, 'recommended_version')
    check_attribute_presence(ad, 'public_vulnerabilities')
    check_github_attributes(ad['github'])
    for v in ad['public_vulnerabilities']:
        check_vulenrability_attributes(v)

    check_attribute_presence(ad, 'private_vulnerabilities')
    for v in ad['private_vulnerabilities']:
        check_vulenrability_attributes(v)

    check_attribute_presence(ad, 'vulnerable_dependencies')
    # Loop through transitive dependencies only if they are present.
    if ad['vulnerable_dependencies']:
        for d in ad['vulnerable_dependencies']:
            check_dependency_attributes(d)


def verify_vulnerability_count(context, component, vulnerability, expected):
    """Check vulnerabiltiy count for given type of vulnerability."""
    json_data = get_json_data(context)
    check_attribute_presence(json_data, 'analyzed_dependencies')

    is_component_present = False
    for dep in json_data['analyzed_dependencies']:
        if dep['name'] == component:
            is_component_present = True
            actual = len(dep[vulnerability])
            assert actual == expected, \
                'Component {} have {} {} but expected {}'.format(component, actual,
                                                                 vulnerability, expected)
    assert is_component_present, 'Component {} not present'.format(component)


def verify_dependency_count(context, component, expected):
    """Check dependency count for given component."""
    json_data = get_json_data(context)
    check_attribute_presence(json_data, 'analyzed_dependencies')

    is_component_present = False
    for dep in json_data['analyzed_dependencies']:
        if dep['name'] == component:
            is_component_present = True
            dependencies = dep['dependencies']
            print(dep)
            actual = len(dependencies)
            assert actual == expected, \
                'Component {} have {} deps but expected {}'.format(component, actual,
                                                                   expected)
    assert is_component_present, 'Component {} not present'.format(component)


def verify_valid_data_companion(context, component, latest_version):
    """Check valid data in companion packages."""
    json_data = get_json_data(context)
    check_attribute_presence(json_data, 'recommendation')

    is_component_present = False
    for dep in json_data['recommendation']['companion']:
        if dep['name'] == component:
            is_component_present = True
            actual_version = dep['latest_version']
            assert actual_version == latest_version, \
                'Component {} have {} but expected {}'.format(component, actual_version,
                                                              latest_version)
    assert is_component_present, 'Component {} not present'.format(component)


def verify_license_data(context, component, license_c):
    """Licenses check."""
    json_data = get_json_data(context)
    check_attribute_presence(json_data, 'analyzed_dependencies')
    is_component_present = False
    for dep in json_data['analyzed_dependencies']:
        if dep['name'] == component:
            is_component_present = True
            assert "licenses" in dep, 'Licenses not found'
            licenses = dep["licenses"]
            for lic in licenses:
                if lic == license_c:
                    assert lic == license_c
    assert is_component_present, 'Component {} not present'.format(component)


def verify_severity_analyzed_deps(context, component, title, severity, vulenerability):
    """Check valid vulenerability title and severity."""
    json_data = get_json_data(context)
    check_attribute_presence(json_data, 'analyzed_dependencies')
    is_component_present = False
    for dep in json_data['analyzed_dependencies']:
        if dep['name'] == component:
            is_component_present = True
            if vulenerability == 'public_vulnerabilities':
                for vuln in dep['public_vulnerabilities']:
                    if vuln['title'] == title:
                        assert vuln['severity'] == severity, "severity not matched"
            elif vulenerability == 'private_vulnerabilities':
                for vuln in dep['private_vulnerabilities']:
                    if vuln['title'] == title:
                        assert vuln['severity'] == severity, "severity not matched"
    assert is_component_present, 'Component {} not present'.format(component)


def check_github_attributes(ad):
    """Check all the analyzed deps for github object."""
    check_attribute_presence(ad, "size")
    check_attribute_presence(ad, "issues")
    check_attribute_presence(ad, "used_by")
    check_attribute_presence(ad, "watchers")
    check_attribute_presence(ad, "forks_count")
    check_attribute_presence(ad, "pull_requests")
    check_attribute_presence(ad, "total_releases")
    check_attribute_presence(ad, "stargazers_count")
    check_attribute_presence(ad, "contributors")
    check_attribute_presence(ad, "open_issues_count")
    check_attribute_presence(ad, "dependent_projects")
    check_attribute_presence(ad, "first_release_date")
    check_attribute_presence(ad, "latest_release_duration")


def check_for_distinct_license(context, licenses):
    """Verify lisense analysis data."""
    json_data = get_json_data(context)
    check_attribute_presence(json_data, 'license_analysis')
    license_analysis = json_data['license_analysis']
    license_found = False
    for lic in license_analysis['distinct_licenses']:
        if lic == licenses:
            license_found = True
    assert license_found, "The Given License was not found."


def verify_valid_data_analyzed_deps(context, component, latest_version, version,
                                    recommended_version, vulenerability, vid, cvss):
    """Check valid data in companion packages."""
    json_data = get_json_data(context)
    check_attribute_presence(json_data, 'analyzed_dependencies')

    is_component_present = False
    for dep in json_data['analyzed_dependencies']:
        if dep['name'] == component:
            is_component_present = True
            is_vuln_id_present = False
            actual_version = dep['latest_version']
            if vulenerability == 'public_vulnerabilities':
                for vuln in dep['public_vulnerabilities']:
                    if vuln['id'] == vid:
                        check_vulenrability_attributes(vuln)
                        assert str(vuln['cvss']) == cvss, 'CVSS score not matched'
                        is_vuln_id_present = True
            elif vulenerability == 'private_vulnerabilities':
                for vuln in dep['private_vulnerabilities']:
                    if vuln['id'] == vid:
                        check_vulenrability_attributes(vuln)
                        assert str(vuln['cvss']) == cvss, 'CVSS score not matched'
                        is_vuln_id_present = True
            assert is_vuln_id_present, 'Invalid vulnerability not found'
            assert actual_version == latest_version, \
                'Component {} have {} but expected latest {}'.format(component, actual_version,
                                                                     latest_version)
            assert dep['version'] == version, \
                'Component {} have {} but expected version{}'.format(component, dep['version'],
                                                                     version)
            assert dep['recommended_version'] == recommended_version, \
                'Component {} have {} but expected {}'.format(component, dep['recommended_version'],
                                                              recommended_version)
    assert is_component_present, 'Component {} not present'.format(component)


@when('I access the {url} endpoint using the HTTP {action} method {token} user key')
def access_url_method(context, url, action, token='without'):
    """Access the service API using the HTTP method and with/without user key."""
    # Convert token text into a valid bool
    with_user_key = parse_token_clause(token)
    params = {}
    if with_user_key:
        params = {'user_key': context.three_scale_preview_user_key}

    if action == 'GET':
        context.response = requests.get(get_endpoint(context) + url, params=params)
    elif action == 'PUT':
        context.response = requests.put(get_endpoint(context) + url, params=params)
    elif action == 'HEAD':
        context.response = requests.head(get_endpoint(context) + url, params=params)
    elif action == 'DELETE':
        context.response = requests.delete(get_endpoint(context) + url, params=params)


@when('I send {ecosystem} package request with manifest {manifest} '
      'to stack analysis v2 {token} {valid} user key')
@when('I send {ecosystem} package request with manifest {manifest} '
      'to stack analysis v2 {token} {valid} user key {trans} transitives')
@when('I send {ecosystem} package request with manifest {manifest} '
      'to stack analysis v2 {token} {valid} user key {uuid} uuid')
@when('I send {ecosystem} package request with manifest {manifest} '
      'to stack analysis v2 {token} {valid} user key {invalid} invalid uuid')
def send_request(context, ecosystem=None, manifest=None, token='without',
                 valid='valid', trans="without", uuid="without", invalid="without"):
    """Send the ecosystem package manifest file to the stack analysis v2."""
    # Ecosystem is mandatory
    assert ecosystem is not None

    # Convert token text into a valid bool
    with_user_key = parse_token_clause(token)
    is_user_registered = parse_token_clause(uuid)
    is_invalid = parse_token_clause(invalid)
    print(is_invalid)

    # Convert valid clause to bool
    with_valid_user_key = parse_valid_clause(valid)

    with_transitives = parse_token_clause(trans)
    post_request(context, ecosystem, manifest, with_user_key, with_valid_user_key,
                 with_transitives, is_user_registered, is_invalid)
    # Send SA request


@then('I should find the external request id equals to id returned by '
      'stack analysis v2 post request')
def check_get_request_id(context):
    """Check the ID of stack analysis."""
    previous_id = context.stack_analysis_id
    assert previous_id is not None

    json_data = get_json_data(context)

    id_name = 'external_request_id'
    check_attribute_presence(json_data, id_name)
    request_id = json_data[id_name]
    logger.debug('Post id: {} Get id: {}'.format(previous_id, request_id))
    assert request_id is not None
    assert previous_id == request_id


@then('I should get stack analyses v2 response with all attributes')
def check_response_attributes(context):
    """Check mandatory attributes presence for stack analyses v2 response."""
    json_data = get_json_data(context)

    # Validate root level attributes.
    check_attribute_presence(json_data, 'version')
    check_attribute_presence(json_data, 'started_at')
    check_timestamp(json_data.get('started_at'))
    check_attribute_presence(json_data, 'ended_at')
    check_timestamp(json_data.get('ended_at'))
    check_attribute_presence(json_data, 'external_request_id')
    check_attribute_presence(json_data, 'registration_status')
    check_attribute_presence(json_data, 'manifest_file_path')
    check_attribute_presence(json_data, 'manifest_name')
    check_attribute_presence(json_data, 'ecosystem')
    check_attribute_presence(json_data, 'unknown_dependencies')
    check_attribute_presence(json_data, 'license_analysis')
    check_attribute_presence(json_data, 'recommendation')
    check_attribute_presence(json_data, 'registration_link')
    check_attribute_presence(json_data, 'analyzed_dependencies')

    # Validate recommendation object.
    recommendation = json_data['recommendation']
    check_attribute_presence(recommendation, 'companion')
    check_attribute_presence(recommendation, 'manifest_file_path')
    check_attribute_presence(recommendation, 'usage_outliers')


@then('I should find the proper outlier record for the {component} component for stack analyses v2')
def check_outliers(context, component):
    """Check the outlier record in the stack analysis."""
    json_data = get_json_data(context)

    path = 'recommendation/usage_outliers'
    usage_outliers = get_value_using_path(json_data, path)
    check_frequency_count(usage_outliers, component)


@then('I should find {expected:n} analyzed dependencies for stack analyses v2')
def check_analyzed_dependencies_count(context, expected=1):
    """Check number of analyzed dependencies."""
    check_equal_expectation_for_array(context, 'analyzed_dependencies', expected)


@then('I should find {expected:n} unknown dependencies for stack analyses v2')
def check_unknown_dependencies_count(context, expected):
    """Check number of unknown dependencies."""
    check_equal_expectation_for_array(context, 'unknown_dependencies', expected)


@then('I should find {expected:n} unknown licenses for stack analyses v2')
def check_unknown_licenses_count(context, expected):
    """Check number of unknown licenses."""
    check_equal_expectation_for_array(context, 'license_analysis/unknown_licenses/unknown',
                                      expected)


@then('I should find {expected:n} distinct licenses for stack analyses v2')
def check_distinct_license_count(context, expected):
    """Check number of distinct licenses."""
    check_equal_expectation_for_array(context, 'license_analysis/distinct_licenses', expected)


@then('I should find {expected:n} usage outliers for stack analyses v2')
def check_usage_outliers_count(context, expected):
    """Check number of usage outliers."""
    check_equal_expectation_for_array(context, 'recommendation/usage_outliers', expected)


@then('I should find registration link for stack analyses v2')
def check_for_registration_link(context):
    """Check for presence of registration link."""
    json_data = get_json_data(context)

    # Validate root level attributes.
    check_attribute_presence(json_data, 'registration_link')


@then('I should find all attribute about analyzed dependencies for stack analyses v2')
def check_analysed_dependencies_attributes(context):
    """Check all attributes presence for analysed dependencies."""
    json_data = get_json_data(context)
    for ad in json_data['analyzed_dependencies']:
        check_dependency_attributes(ad)


@when('I start stack analyses v2 for {ecosystem} package with {manifest} manifest for {rate:d} '
      'times in a minute {user_key} {valid} user key')
def start_rate_limit_requests(context, ecosystem, manifest, rate, user_key='with', valid='valid'):
    """Multiple SA request within given time window to generate 429 (rate limit)."""
    # Convert token text into a valid bool
    with_user_key = parse_token_clause(user_key)

    # Convert valid clause to bool
    with_valid_user_key = parse_valid_clause(valid)

    # Perform loop to send requested number of request and compute duration.
    check_rate_limit(context, ecosystem, manifest, rate, with_user_key, with_valid_user_key)


@then('I should get {expected:d} public vulnerabilities for {component}')
def verify_public_vulnerabilty_count(context, expected, component):
    """Verify number of public vulnerabilites."""
    verify_vulnerability_count(context, component, 'public_vulnerabilities', expected)


@then('I should get {expected:d} private vulnerabilities for {component}')
def verify_private_vulnerabilty_count(context, expected, component):
    """Verify number of private vulnerabilites."""
    verify_vulnerability_count(context, component, 'private_vulnerabilities', expected)


@then('I should get {expected:d} transitive vulnerabilities for {component}')
def verify_transitive_vulnerabilty_count(context, expected, component):
    """Verify number of transitive vulnerabilites."""
    verify_vulnerability_count(context, component, 'vulnerable_dependencies', expected)


@then('I should get latest version {version} for {component} in campanion packages')
def verify_companion(context, version, component):
    """Verify campanion packages."""
    verify_valid_data_companion(context, component, version)


@then('I should find {component} with {version} {latest_version} {expected} with '
      '{vid} and {cvss} for {mode} vulnerbilities')
def verify_valid_data(context, component, latest_version, version, expected, vid, cvss, mode):
    """Verify data validation."""
    if mode == "public":
        verify_valid_data_analyzed_deps(context, component, latest_version, version, expected,
                                        "public_vulnerabilities", vid, cvss)
    else:
        verify_valid_data_analyzed_deps(context, component, latest_version, version, expected,
                                        "private_vulnerabilities", vid, cvss)


@then('I should find License {licensee} for {component} in analyzed dependencies')
def verify_comp_license(context, component, licensee):
    """Verify License for components."""
    verify_license_data(context, component, licensee)


@then('I should find {title} and {severity} for {component} in {mode} vulnerbilities')
def verify_title_severity(context, title, severity, component, mode):
    """Verify severity and title."""
    if mode == "public":
        verify_severity_analyzed_deps(context, component, title, severity,
                                      "public_vulnerabilities")
    else:
        verify_severity_analyzed_deps(context, component, title, severity,
                                      "private_vulnerabilities")


@then('I should be able to validate github data for all dependencies')
def verify_github_data(context):
    """Verify the github data."""
    json_data = get_json_data(context)
    check_attribute_presence(json_data, 'analyzed_dependencies')
    for dep in json_data['analyzed_dependencies']:
        check_github_attributes(dep['github'])


@then('I should get {expected:d} transitive dependencies for {component}')
def verify_transitive_dependencies_count(context, expected, component):
    """Verify number of transitive vulnerabilites."""
    verify_dependency_count(context, component, expected)


@then('I should find distinct license {licenses} for license analysis')
def verify_distinct_license(context, licenses):
    """Verify the checks for distinct licenses."""
    check_for_distinct_license(context, licenses)


@then('I should find premium vulnerablities in result')
def verify_premium_feilds(context):
    """I should verify the registered user feilds in result."""
    json_data = get_json_data(context)
    check_attribute_presence(json_data, 'analyzed_dependencies')
    for dep in json_data['analyzed_dependencies']:
        if dep['public_vulnerabilities'] != []:
            for vuln in dep['public_vulnerabilities']:
                check_vulenrability_attributes(vuln)
                check_premium_vuln_attributes(vuln)
        elif dep['private_vulnerabilities'] != []:
            for vuln in dep['private_vulnerabilities']:
                check_vulenrability_attributes(vuln)
                check_premium_vuln_attributes(vuln)
