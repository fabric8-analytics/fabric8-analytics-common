"""Common test steps and checks."""
import string
import datetime
import json
import time
import os
import re

from behave import given, then, when
from urllib.parse import urljoin
import jsonschema
import requests
import uuid

import botocore
from botocore.exceptions import ClientError
from src.attribute_checks import *
from src.MockedResponse import *
from src.s3interface import *
from src.utils import *
from src.json_utils import *
from src.parsing import *
from src.authorization_tokens import *


# Do not remove - kept for debugging
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


@given('System is in initial state')
def initial_state(context):
    """Restart the system to the known initial state."""
    context.restart_system(context)


@given('System is running')
def running_system(context):
    """Ensure that the system is running, (re)start it if necesarry."""
    if not context.is_running(context):
        initial_state(context)


@given('{directory} directory exists')
def does_data_directory_exists(context, directory):
    """Ensure that the specified directory exists."""
    assert os.path.isdir(directory), \
        "The specified directory '{directory}' does not exist".format(directory=directory)


@when("I obtain TGT in {service} service")
def get_tgt_in_service(context, service):
    """Obtain TGT in specified container via `docker exec` and returns output of klist."""
    context.container = context.run_command_in_service(context, service,
                                                       ["sleep", "10"])
    assert context.container
    # just in case
    context.exec_command_in_container(context.client, context.container,
                                      'kdestroy')

    # this may take ages if you are not on network: I'm currently writing this
    # in train and I had no wifi nor ethernet and the command would never
    # finish; when I connected to train's wifi it started to work just fine;
    # can you imagine?
    kinit_command = 'bash -c "echo user | kinit user@EXAMPLE.COM"'
    context.exec_command_in_container(context.client, context.container,
                                      kinit_command)
    klist_out = context.exec_command_in_container(context.client,
                                                  context.container, 'klist')
    assert "Valid starting" in klist_out


@then('I should receive empty JSON response')
@then('I should see empty analysis')
def check_json_empty_response(context):
    """Check that the JSON response is empty."""
    assert is_empty_json_response(context)


@then('I should receive nonempty JSON response')
def check_json_nonempty_response(context):
    """Check that the JSON response is not empty."""
    assert not is_empty_json_response(context)


@then('I should receive nempty JSON response from S3')
def check_json_nempty_response_from_s3(context):
    """Check that the JSON response from S3 is empty."""
    assert is_empty_json_response_from_s3(context)


@then('I should receive nonempty JSON response from S3')
def check_json_nonempty_response_from_s3(context):
    """Check that the JSON response from S3 is not empty."""
    assert not is_empty_json_response_from_s3(context)


@then('I should get {status:d} status code')
def check_status_code(context, status):
    """Check the HTTP status code returned by the REST API."""
    assert context.response.status_code == status


@then('I should receive JSON response containing the {key} key')
def check_json_response_contains_key(context, key):
    """Check that the JSON response contains given key."""
    assert key in context.response.json()


@then('I should receive JSON response with the {key} key set to {value}')
def check_json_value_under_key(context, key, value):
    """Check that the JSON response contains given value under selected key."""
    assert context.response.json().get(key) == value


@then('I should receive JSON response with the correct id')
def check_id_in_json_response(context):
    """Check the ID attribute in the JSON response.

    Check if ID is in a format like: '477e85660c504b698beae2b5f2a28b4e'
    ie. it is a string with 32 characters containing 32 hexadecimal digits
    """
    check_id_value_in_json_response(context, "id")


@then('I should receive JSON response with the correct timestamp in attribute {attribute}')
def check_timestamp_in_json_attribute(context, attribute):
    """Check the timestamp stored in the JSON response.

    Check if the attribute in the JSON response object contains
    proper timestamp value
    """
    check_timestamp_in_json_response(context, attribute)


@then('I should find proper timestamp under the path {path}')
def check_timestamp_under_path(context, path):
    """Check the timestamp stored in selected attribute.

    Check if timestamp value can be found in the JSON response object
    under the given path.
    """
    jsondata = context.response.json()
    assert jsondata is not None
    timestamp = get_value_using_path(jsondata, path)
    check_timestamp(timestamp)


@when('I wait {num:d} seconds')
@then('I wait {num:d} seconds')
def pause_scenario_execution(context, num):
    """Pause the test for provided number of seconds."""
    time.sleep(num)


@then('I should see {state} analysis result for {ecosystem}/{package}/{version}')
def check_analysis_result(context, state, ecosystem, package, version):
    """Check the analysis result for given ecosystem, package, and version."""
    # TODO: reduce cyclomatic complexity
    res = context.response.json()
    if state == 'incomplete':
        assert res['ecosystem'] == ecosystem
        assert res['package'] == package
        assert res['version'] == version
        assert datetime.datetime.strptime(res["started_at"], "%Y-%m-%dT%H:%M:%S.%f")
    elif state == 'complete':
        assert datetime.datetime.strptime(res["finished_at"], "%Y-%m-%dT%H:%M:%S.%f")
        analyzers_keys = context.get_expected_component_analyses(ecosystem)
        actual_keys = set(res["analyses"].keys())
        missing, unexpected = context.compare_analysis_sets(actual_keys,
                                                            analyzers_keys)
        err_str = 'unexpected analyses: {}, missing analyses: {}'
        assert not missing and not unexpected, err_str.format(unexpected, missing)
        analyzers_with_standard_schema = set(analyzers_keys)
        analyzers_with_standard_schema -= context.NONSTANDARD_ANALYSIS_FORMATS
        for a in analyzers_with_standard_schema:
            a_keys = set(res["analyses"].get(a, {}).keys())
            if not a_keys and a in context.UNRELIABLE_ANALYSES:
                continue
            assert a_keys.issuperset({"details", "status", "summary"}), a_keys


@then('Result of {ecosystem}/{package}/{version} should be valid')
def validate_analysis_result(context, ecosystem, package, version):
    """Validate results of the analysis."""
    res = context.response.json()
    # make sure analysis has finished
    assert res['finished_at'] is not None
    # we want to validate top-level analysis and worker results that have "schema" defined
    structures_to_validate = [res]
    for _, worker_result in res['analyses'].items():
        # TODO: in future we want to mandate that all workers have their schemas,
        #  so we'll remove the condition
        if 'schema' in worker_result:
            structures_to_validate.append(worker_result)

    for struct in structures_to_validate:
        schema = requests.get(struct['schema']['url']).json()
        jsonschema.validate(struct, schema)


@then('I should find the value {value} under the path {path} in the JSON response')
def find_value_under_the_path(context, value, path):
    """Check if the value (attribute) can be found in the JSON output."""
    jsondata = context.response.json()
    assert jsondata is not None
    v = get_value_using_path(jsondata, path)
    assert v is not None
    # fallback for int value in the JSON file
    if type(v) is int:
        assert v == int(value)
    else:
        assert v == value


@then('I should find the null value under the path {path} in the JSON response')
def find_null_value_under_the_path(context, path):
    """Check if the value (attribute) can be found in the JSON output."""
    jsondata = context.response.json()
    assert jsondata is not None
    v = get_value_using_path(jsondata, path)
    assert v is None


@then('I should find the timestamp value under the path {path} in the JSON response')
def find_timestamp_value_under_the_path(context, path):
    """Check if the value (attribute) can be found in the JSON output."""
    jsondata = context.response.json()
    assert jsondata is not None
    v = get_value_using_path(jsondata, path)
    assert v is not None
    check_timestamp(v)


@when('I mock API response by {filename} file')
def read_json_file(context, filename):
    """Mock the API response by content of given data file."""
    context.response = MockedResponse(filename)


@when('I mock S3 data by content of {filename} file')
def read_json_file_for_s3(context, filename):
    """Mock the S3 data by content of given data file."""
    context.s3_data = MockedResponse.json_load(filename)
