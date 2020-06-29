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
}


def get_endpoint(context):
    """Get endpoint for the stack analysis v2."""
    return urljoin(context.threescale_preview_url, '/api/v2/stack-analyses/')


def post_request(context, ecosystem, manifest, with_user_key, with_valid_user_key):
    """Send stack analyses v2 post request based on params."""
    logger.debug('ecosystem: {} manifest: {} with_user_key: {} '
                 'with_valid_user_key: {}'.format(ecosystem, manifest, with_user_key,
                                                  with_valid_user_key))
    context.manifest = manifest

    # set default values
    files = {}
    data = {'show_transitive': 'false'}

    # Add ecosystem if not None
    if ecosystem != 'None':
        data['ecosystem'] = ecosystem

    # Read manifest if not None
    if manifest != 'None':
        filename = 'data/{}'.format(manifest)
        files['manifest'] = (ECOSYSTEM_TO_MANIFEST_NAME_MAP.get(ecosystem, 'invalid_name.json'),
                             open(filename, 'rb'))
        data['file_path'] = os.path.abspath(os.path.dirname(filename))

    if with_user_key:
        if with_valid_user_key:
            params = {'user_key': context.three_scale_preview_user_key}
        else:
            params = {'user_key': 'INVALID_USER_KEY_FOR_TESTING'}
        logger.debug('POST {} files: {} data: {} params: {}'.format(get_endpoint(context),
                                                                    files, data, params))
        response = requests.post(get_endpoint(context), files=files, data=data, params=params)
    else:
        response = requests.post(get_endpoint(context), files=files, data=data)

    logger.debug('status_code: {} response: {}'.format(response.status_code, response.text))
    context.response = response


@when('I wait for stack analysis v2 to finish {token} user key')
def wait_for_completion(context, token='without'):
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

    id = context.response.json().get('id')
    context.stack_analysis_id = id
    logger.debug('SA V2 Request id: {}'.format(id))

    url = urljoin(get_endpoint(context), id)
    logger.debug('Get API url: {}'.format(url))

    for _ in range(timeout // sleep_amount):
        if with_user_key:
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
    assert is_component_present, 'Component not present'


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
def send_request(context, ecosystem=None, manifest=None, token='without', valid='valid'):
    """Send the ecosystem package manifest file to the stack analysis v2."""
    # Ecosystem is mandatory
    assert ecosystem is not None

    # Convert token text into a valid bool
    with_user_key = parse_token_clause(token)

    # Convert valid clause to bool
    with_valid_user_key = parse_valid_clause(valid)

    # Send SA request
    post_request(context, ecosystem, manifest, with_user_key, with_valid_user_key)


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
