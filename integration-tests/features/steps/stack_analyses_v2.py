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
"""Tests for API endpoints that performs stack analysis V2 API."""

import requests
import time
import os
from behave import when, then
from urllib.parse import urljoin
from src.attribute_checks import check_attribute_presence
from src.parsing import parse_token_clause, parse_valid_clause
from src.attribute_checks import check_timestamp

ECOSYSTEM_TO_MANIFEST_NAME_MAP = {
    'pypi': 'pylist.json',
    'npm': 'npmlist.json',
    'maven': 'dependencies.txt'
}


def get_sav2_endpoint(context):
    """Return endpoint for the stack analysis v2."""
    # Two available endpoints for stack analysis are /stack-analyses and /analyse
    return urljoin(context.threescale_preview_url, '/api/v2/stack-analyses/')


def post_sav2(context, ecosystem, manifest, with_user_key, is_valid):
    """Send stack analyses v2 post request based on params."""
    print('ecosystem: {} manifest: {} with_user_key: {} '
          'is_valid: {}'.format(ecosystem, manifest, with_user_key, is_valid))
    context.manifest = manifest

    # set default values
    files = {}
    data = {}

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
        if is_valid:
            params = {'user_key': context.three_scale_preview_user_key}
        else:
            params = {'user_key': 'INVALID_USER_KEY_FOR_TESTING'}
        print(f'POST {get_sav2_endpoint(context)} files: {files} data: {data} params: {params}')
        response = requests.post(get_sav2_endpoint(context), files=files, data=data, params=params)
    else:
        response = requests.post(get_sav2_endpoint(context), files=files, data=data)

    print('status_code: {} response: {}'.format(response.status_code, response.text))
    context.response = response


@when('I access the {url} endpoint using the HTTP {action} method {token} user key')
def access_url_put_method_with_authorization(context, url, action, token='without'):
    """Access the service API using the HTTP method and with/without user key."""
    # Convert token text into a valid bool
    with_user_key = parse_token_clause(token)
    params = {}
    if with_user_key:
        params = {'user_key': context.three_scale_preview_user_key}

    if action == 'GET':
        context.response = requests.get(get_sav2_endpoint(context) + url, params=params)
    elif action == 'PUT':
        context.response = requests.put(get_sav2_endpoint(context) + url, params=params)
    elif action == 'HEAD':
        context.response = requests.head(get_sav2_endpoint(context) + url, params=params)
    elif action == 'DELETE':
        context.response = requests.delete(get_sav2_endpoint(context) + url, params=params)


@when('I send {ecosystem} package request with manifest {manifest} '
      'to stack analysis v2 {token} {valid} user key')
def send_sav2_request(context, ecosystem=None, manifest=None, token='without', valid='valid'):
    """Send the ecosystem package manifest file to the stack analysis."""
    # Ecosystem is mandatory
    assert ecosystem is not None

    # Convert token text into a valid bool
    with_user_key = parse_token_clause(token)

    # Convert valid clause to bool
    is_valid = parse_valid_clause(valid)

    # Send SA request
    post_sav2(context, ecosystem, manifest, with_user_key, is_valid)


@when('I wait for stack analysis v2 to finish {token} user key')
def wait_for_sav2_completion(context, token='without'):
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
    print('SA V2 Request id: {}'.format(id))

    url = urljoin(get_sav2_endpoint(context), id)
    print('Get API url: {}'.format(url))

    for _ in range(timeout // sleep_amount):
        if with_user_key:
            params = {'user_key': context.three_scale_preview_user_key}
            context.response = requests.get(url, params=params)
        else:
            context.response = requests.get(url)
        status_code = context.response.status_code
        print('status_code: {} response: {}'.format(status_code, context.response.text))
        if status_code == 200:
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


@then('I should find the external request id equals to id returned by '
      'stack analysis v2 post request')
def check_sav2_get_request_id(context):
    """Check the ID of stack analysis."""
    previous_id = context.stack_analysis_id
    assert previous_id is not None

    json_data = context.response.json()
    assert json_data is not None

    id_name = 'external_request_id'
    check_attribute_presence(json_data, id_name)
    request_id = json_data[id_name]
    print('Post id: {} Get id: {}'.format(previous_id, request_id))
    assert request_id is not None
    assert previous_id == request_id


@then('I should get stack analyses v2 response with all attributes')
def check_sav2_response_attributes(context):
    """Check mandatory attributes presence for stack analyses v2 response."""
    json_data = context.response.json()
    assert json_data is not None

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
