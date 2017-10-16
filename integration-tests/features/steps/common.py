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

import jwt
from jwt.contrib.algorithms.pycrypto import RSAAlgorithm

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

DEFAULT_AUTHORIZATION_TOKEN_FILENAME = "private_key.pem"

jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))


@given('System is in initial state')
def initial_state(context):
    """Restart the system to the known initial state."""
    context.restart_system(context)


@given('System is running')
def running_system(context):
    """Ensure that the system is running, (re)start it if necesarry."""
    if not context.is_running(context):
        initial_state(context)


@given('Jobs debug API is running')
def running_jobs_debug_api(context):
    """Wait for the job debug REST API to be available."""
    if not context.is_jobs_debug_api_running(context):
        context.wait_for_jobs_debug_api_service(context, 60)


@when("I obtain TGT in {service} service")
def get_tgt_in_service(context, service):
    """Obtain TGT in specified container via `docker exec` and returns
    output of klist."""
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


@when("I perform kerberized {method} request to {url}")
def perform_kerberized_request(context, method, url):
    """Call REST API on coreapi-server."""
    command = "curl -s -X {method} --negotiate -u : " + \
              "http://coreapi-server:5000{url}".format(method=method, url=url)
    context.kerb_request = \
        context.exec_command_in_container(context.client, context.container,
                                          command)


def contains_alternate_node(json_resp):
    """Check for the existence of alternate node in the stack analysis."""
    result = json_resp.get('result')
    return bool(result) and isinstance(result, list) \
        and (result[0].get('recommendation', {}) or {}).get('alternate', None) is not None


@when('I access anitya {url}')
def anitya_url(context, url):
    """Access the Anitya service API using the HTTP GET method."""
    context.response = requests.get(context.anitya_url + url)


@when('I access jobs API {url:S}')
def jobs_api_url(context, url):
    """Access the jobs service API using the HTTP GET method."""
    context.response = requests.get(context.jobs_api_url + url)


@when('I access jobs API {url:S} with authorization token')
def jobs_api_url_with_authorization_token(context, url):
    """Access the jobs service API using the HTTP GET method."""
    context.response = requests.get(context.jobs_api_url + url,
                                    headers=jobs_api_authorization(context))


@when('I read list of jobs')
@when('I read list of jobs with type {type}')
@when('I read list of jobs {token} authorization token')
@when('I read list of jobs with type {type} {token} authorization token')
def list_of_jobs(context, type=None, token=None):
    '''Read list of jobs via job API.'''
    endpoint = job_endpoint(context)
    if type is not None:
        endpoint += "?job_type=" + type
    use_token = parse_token_clause(token)
    if use_token:
        context.response = requests.get(endpoint, headers=jobs_api_authorization(context))
    else:
        context.response = requests.get(endpoint)


@when('I access {url:S}')
def access_url(context, url):
    """Access the service API using the HTTP GET method."""
    context.response = requests.get(context.coreapi_url + url)


@when('I access {url:S} with authorization token')
def access_url_with_authorization_token(context, url):
    """Access the service API using the HTTP GET method."""
    context.response = requests.get(context.coreapi_url + url,
                                    headers=authorization(context))


@when("I post {is_valid} input to the {endpoint} endpoint {token} authorization token")
def post_input_to_user_feedback(context, is_valid, endpoint, token):
    """Send feedback to user feedback endpoint."""
    use_token = parse_token_clause(token)
    api_url = urljoin(context.coreapi_url, endpoint)
    if is_valid == "valid":
        data = {"request_id": "test_id", "feedback": [{"ques": "what", "ans": "got it"}]}
    else:
        data = {"request_id": "test_id"}
    if use_token:
        response = requests.post(api_url, json=data,
                                 headers=authorization(context))
    else:
        response = requests.post(api_url, json=data)
    context.response = response


def job_metadata_filename(metadata):
    return "data/{metadata}".format(metadata=metadata)


def flow_sheduling_endpoint(context, state, job_id=None):
    """Return URL to flow-scheduling with the given state and job ID."""
    if job_id:
        return "{jobs_api_url}api/v1/jobs/flow-scheduling?state={state}&job_id={job_id}".\
               format(jobs_api_url=context.jobs_api_url, state=state, job_id=job_id)
    else:
        return "{jobs_api_url}api/v1/jobs/flow-scheduling?state={state}".\
               format(jobs_api_url=context.jobs_api_url, state=state)


def job_endpoint(context, job_id=None):
    """Return URL for given job id that can be used to job state manipulation."""
    url = "{jobs_api_url}api/v1/jobs".format(
           jobs_api_url=context.jobs_api_url)
    if job_id is not None:
        url = "{url}/{job_id}".format(url=url, job_id=job_id)
    return url


def send_json_file_to_job_api(context, endpoint, filename, use_token):
    """Send the given file to the selected job API endpoints. If the use_token
    is set, send the 'auth-token' header with the token taken from the
    context environment."""
    if use_token:
        headers = jobs_api_authorization(context)
        context.response = context.send_json_file(endpoint, filename, headers)
    else:
        context.response = context.send_json_file(endpoint, filename)


@when("I post a job metadata {metadata} with state {state}")
@when("I post a job metadata {metadata} with state {state} {token} authorization token")
def perform_post_job(context, metadata, state, token="without"):
    """API call to create a new job using the provided metadata. The token
    parameter can be set to 'with', 'without', or 'using'."""
    filename = job_metadata_filename(metadata)
    endpoint = flow_sheduling_endpoint(context, state)
    use_token = parse_token_clause(token)
    send_json_file_to_job_api(context, endpoint, filename, use_token)


def get_unique_job_id(context, job_id):
    if 'job_id_prefix' in context:
        return "{uuid}_{job_id}".format(uuid=context.job_id_prefix, job_id=job_id)
    else:
        return job_id


@when("I post a job metadata {metadata} with job id {job_id} and state {state}")
@when("I post a job metadata {metadata} with job id {job_id} and state {state} {token} "
      "authorization token")
def perform_post_job_with_state(context, metadata, job_id, state, token="without"):
    """API call to create a new job using the provided metadata and set a job
    to given state. The token parameter can be set to 'with', 'without', or
    'using'."""
    filename = job_metadata_filename(metadata)
    job_id = get_unique_job_id(context, job_id)
    endpoint = flow_sheduling_endpoint(context, state, job_id)
    use_token = parse_token_clause(token)
    send_json_file_to_job_api(context, endpoint, filename, use_token)


@when("I delete job without id")
@when("I delete job without id {token} authorization token")
@when("I delete job with id {job_id}")
@when("I delete job with id {job_id} {token} authorization token")
def delete_job(context, job_id=None, token="without"):
    """API call to delete a job with given ID."""
    job_id = get_unique_job_id(context, job_id)
    endpoint = job_endpoint(context, job_id)
    use_token = parse_token_clause(token)
    if use_token:
        context.response = requests.delete(endpoint, headers=jobs_api_authorization(context))
    else:
        context.response = requests.delete(endpoint)


@when("I set status for job with id {job_id} to {status}")
@when("I set status for job with id {job_id} to {status} {token} authorization token")
def set_job_status(context, job_id, status, token="without"):
    """API call to set job status."""
    endpoint = job_endpoint(context, job_id)
    url = "{endpoint}?state={status}".format(endpoint=endpoint, status=status)
    use_token = parse_token_clause(token)
    if use_token:
        context.response = requests.put(url, headers=jobs_api_authorization(context))
    else:
        context.response = requests.put(url)


@when("I reset status for the job service")
@when("I set status for job service to {status}")
@when("I set status for job service to {status} {token} authorization token")
def set_job_service_status(context, status=None, token="without"):
    """API call to set or reset job service status."""
    url = "{jobs_api_url}api/v1/service/state".format(
            jobs_api_url=context.jobs_api_url)
    use_token = parse_token_clause(token)
    if status is not None:
        url = "{url}?state={status}".format(url=url, status=status)
    if use_token:
        context.response = requests.put(url, headers=jobs_api_authorization(context))
    else:
        context.response = requests.put(url)


@when("I clean all failed jobs")
@when("I clean all failed jobs {token} authorization token")
def clean_all_failed_jobs(context, token="without"):
    """API call to clean up all failed jobs."""
    url = "{url}api/v1/jobs/clean-failed".format(url=context.jobs_api_url)
    use_token = parse_token_clause(token)
    if use_token:
        context.response = requests.delete(url, headers=jobs_api_authorization(context))
    else:
        context.response = requests.delete(url)


@when('I logout from the job service')
@when('I logout from the job service {token} authorization token')
def logout_from_the_jobs_service(context, token='without'):
    url = "{jobs_api_url}api/v1/logout".format(
            jobs_api_url=context.jobs_api_url)
    use_token = parse_token_clause(token)
    if use_token:
        headers = jobs_api_authorization(context)
        context.response = requests.put(url, headers)
    else:
        context.response = requests.put(url)


@when('I access the job service endpoint to generate token')
def job_service_generate_token(context):
    url = "{jobs_api_url}api/v1/generate-token".format(
            jobs_api_url=context.jobs_api_url)
    context.response = requests.get(url)


@then('I should be redirected to {url}')
def check_redirection(context, url):
    assert context.response is not None
    assert context.response.history is not None
    assert context.response.url is not None
    assert context.response.url.startswith(url)


@when("I ask for analyses report for ecosystem {ecosystem}")
@when("I ask for analyses report for ecosystem {ecosystem} {token} authorization token")
@when("I ask for analyses report for ecosystem {ecosystem} from date {from_date} {token} "
      "authorization token")
@when("I ask for analyses report for ecosystem {ecosystem} to date {to_date} {token} "
      "authorization token")
@when("I ask for analyses report for ecosystem {ecosystem} between dates {from_date} {to_date} "
      "{token} authorization token")
def access_analyses_report(context, ecosystem, from_date=None, to_date=None, token="without"):
    """API call to get analyses report for selected ecosystem."""
    use_token = parse_token_clause(token)
    url = "{url}api/v1/debug/analyses-report?ecosystem={ecosystem}".format(
           url=context.jobs_api_url, ecosystem=ecosystem)
    if from_date is not None:
        url += "&from_date=" + from_date
    if to_date is not None:
        url += "&to_date=" + to_date
    if use_token:
        headers = jobs_api_authorization(context)
        context.response = requests.get(url, headers=headers)
    else:
        context.response = requests.get(url)


@then("I should get API token")
def check_api_token(context):
    try:
        j = json.loads(context.kerb_request)
    except ValueError:
        print(context.kerb_request)
        raise
    assert j["token"]


@then('I should see {num:d} ecosystems')
def check_ecosystems(context, num):
    """
    check if the API call returns correct number of ecosystems
    """
    ecosystems = context.response.json()['items']
    assert len(ecosystems) == num
    for e in ecosystems:
        # assert that there is 'ecosystem' field in every ecosystem
        assert 'ecosystem' in e


def get_jobs_count(context):
    jsondata = context.response.json()
    jobs = jsondata['jobs']
    return jsondata['jobs_count']


@then('I should see {num:d} jobs')
def check_jobs(context, num):
    """
    check the number of jobs
    """
    jobs_count = get_jobs_count(context)
    assert len(jobs) == num
    assert jobs_count == num


@then('I should see N jobs')
def check_jobs(context):
    """Check and remember the number of jobs."""
    jobs_count = get_jobs_count(context)
    context.jobs_count = jobs_count


@then('I should see N+{num:d} jobs')
def check_jobs(context, num):
    """Check the relative jobs count and remember the number of jobs."""

    assert context.jobs_count is not None, \
        "Please use 'I should see N jobs' test step first"

    old_jobs_count = context.jobs_count
    jobs_count = get_jobs_count(context)
    expected = old_jobs_count + num

    assert jobs_count == expected, "Expected %d jobs, but %d found instead" % \
        (expected, jobs_count)

    # remember the new number
    context.jobs_count = jobs_count


def get_job_by_id(jobs, job_id):
    return next((job for job in jobs if job["job_id"] == job_id), None)


@then('I should find job with ID {job_id}')
@then('I should find job with ID {job_id} and state {state}')
def find_job(context, job_id, state=None):
    """
    check if job with given ID is returned from the service and optionally if
    the job status has expected value
    """
    jsondata = context.response.json()
    jobs = jsondata['jobs']
    job_id = get_unique_job_id(context, job_id)
    job_ids = [job["job_id"] for job in jobs]
    assert job_id in job_ids
    if state is not None:
        job = get_job_by_id(jobs, job_id)
        assert job is not None
        assert job["state"] is not None
        assert job["state"] == state


@then('I should not find job with ID {job_id}')
def should_not_find_job_by_id(context, job_id):
    """
    check if job with given ID does not exist
    """
    jsondata = context.response.json()
    jobs = jsondata['jobs']
    job_id = get_unique_job_id(context, job_id)
    job_ids = [job["job_id"] for job in jobs]
    assert job_id not in job_ids


@then('I should see {num:d} versions ({versions}), all for {ecosystem}/{package} package')
def check_versions(context, num=0, versions='', ecosystem='', package=''):
    versions = split_comma_separated_list(versions)
    vrsns = context.response.json()['items']
    assert len(vrsns) == num
    for v in vrsns:
        assert v['ecosystem'] == ecosystem
        assert v['package'] == package
        assert v['version'] in versions


@then('I should receive empty JSON response')
@then('I should see empty analysis')
def check_json(context):
    assert is_empty_json_response(context)


@then('I should get {status:d} status code')
def check_status_code(context, status):
    """Check the HTTP status code returned by the REST API."""
    assert context.response.status_code == status


@then('I should receive JSON response containing the {key} key')
def check_json_response(context, key):
    assert key in context.response.json()


@then('I should receive JSON response with the {key} key set to {value}')
def check_json_value_under_key(context, key, value):
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
    """Check the timestamp stored in selected attribute

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


@then("I should get a valid request ID")
def check_stack_analyses_request_id(context):
    """Check the ID attribute in the JSON response.

    Check if ID is in a format like: '477e85660c504b698beae2b5f2a28b4e'
    ie. it is a string with 32 characters containing 32 hexadecimal digits
    """
    check_id_value_in_json_response(context, "request_id")


@then("I should find the status attribute set to success")
def check_stack_analyses_request_id(context):
    response = context.response
    json_data = response.json()

    check_attribute_presence(json_data, 'status')

    assert json_data['status'] == "success"


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


@then('I should find the attribute request_id equals to id returned by stack analysis request')
def check_stack_analysis_id(context):
    previous_id = context.stack_analysis_id

    json_data = context.response.json()
    assert json_data is not None

    check_attribute_presence(json_data, "request_id")
    request_id = json_data["request_id"]

    assert previous_id is not None
    assert request_id is not None
    assert previous_id == request_id


@then('I should find analyzed dependency named {package} with version {version} in the stack '
      'analysis')
def check_analyzed_dependency(context, package, version):
    jsondata = context.response.json()
    assert jsondata is not None
    path = "result/0/user_stack_info/analyzed_dependencies"
    analyzed_dependencies = get_value_using_path(jsondata, path)
    assert analyzed_dependencies is not None
    for analyzed_dependency in analyzed_dependencies:
        if analyzed_dependency["package"] == package \
           and analyzed_dependency["version"] == version:
            break
    else:
        raise Exception('Package {package} with version {version} not found'.
                        format(package=package, version=version))


@then('I should find the following analyzed dependencies ({packages}) in the stack analysis')
def check_all_analyzed_dependency(context, packages):
    packages = split_comma_separated_list(packages)
    jsondata = context.response.json()
    assert jsondata is not None
    path = "result/0/user_stack_info/analyzed_dependencies"
    analyzed_dependencies = get_value_using_path(jsondata, path)
    assert analyzed_dependencies is not None
    dependencies = get_attribute_values(analyzed_dependencies, "package")
    for package in packages:
        if package not in dependencies:
            raise Exception('Package {package} not found'.format(package=package))


@when('I generate authorization token from the private key {private_key}')
def generate_authorization_token(context, private_key):
    expiry = datetime.datetime.utcnow() + datetime.timedelta(days=90)
    userid = "testuser"

    path_to_private_key = 'data/{private_key}'.format(private_key=private_key)
    # initial value
    context.token = None

    with open(path_to_private_key) as fin:
        private_key = fin.read()

        payload = {
            'exp': expiry,
            'iat': datetime.datetime.utcnow(),
            'sub': userid
        }
        token = jwt.encode(payload, key=private_key, algorithm='RS256')
        decoded = token.decode('utf-8')
        # print(decoded)
        context.token = decoded


@then('I should get the proper authorization token')
def is_proper_authorization_token(context):
    assert context.token is not None


@then('I should get the proper job API authorization token')
def is_proper_authorization_token(context):
    assert context.jobs_api_token is not None


@when('I acquire the authorization token')
def acquire_authorization_token(context):
    recommender_token = os.environ.get("RECOMMENDER_API_TOKEN")
    # log.info ("TOKEN: {}\n\n".format(recommender_token))
    if recommender_token is not None:
        context.token = recommender_token
    else:
        generate_authorization_token(context, DEFAULT_AUTHORIZATION_TOKEN_FILENAME)


@when('I acquire job API authorization token')
def acquire_jobs_api_authorization_token(context):
    context.jobs_api_token = os.environ.get("JOB_API_TOKEN")
    # TODO: authorization via GitHub?


@then('I should see proper information about job API tokens')
def check_job_api_tokens_information(context):
    '''Check the tokens information returned by job API.'''

    json_data = context.response.json()
    assert json_data is not None

    assert "tokens" in json_data
    tokens = json_data["tokens"]

    assert len(tokens) > 0

    for token in tokens:
        assert "token" in token
        assert "rate" in token
        assert "resources" in token

        rate_token = token["rate"]
        check_job_token_attributes(rate_token)

        resources = token["resources"]

        token_names = ["core", "graphql", "search"]

        for token_name in token_names:
            assert token_name in resources
            check_job_token_attributes(resources[token_name])


@then('I should see proper analyses report')
def check_job_debug_analyses_report(context):
    '''Check the analyses report returned by job API.'''
    json_data = context.response.json()
    assert json_data is not None

    assert "now" in json_data
    check_timestamp(json_data["now"])

    assert "report" in json_data
    report = json_data["report"]

    attributes = ["analyses", "analyses_finished", "analyses_finished_unique",
                  "analyses_unfinished", "analyses_unique", "packages",
                  "packages_finished", "versions"]

    for attribute in attributes:
        assert attribute in report
        assert int(report[attribute]) >= 0


@when('I connect to the AWS S3 database')
def connect_to_aws_s3(context):
    '''Try to connect to the AWS S3 database using the given access key,
    secret access key, and region name.'''
    context.s3interface.connect()


@then('I should see {bucket} bucket')
def find_bucket_in_s3(context, bucket):
    '''Check if bucket with given name can be found and can be read by
    current AWS S3 database user.'''
    assert context.s3interface.does_bucket_exist(bucket)


def package_key_into_s3(ecosystem, package):
    return "{ecosystem}/{package}.json".format(ecosystem=ecosystem,
                                               package=package)


def package_data_key_into_s3(ecosystem, package, metadata):
    return "{ecosystem}/{package}/{metadata}.json".format(ecosystem=ecosystem,
                                                          package=package,
                                                          metadata=metadata)


def component_key_into_s3(ecosystem, package, version):
    return "{ecosystem}/{package}/{version}.json".format(ecosystem=ecosystem,
                                                         package=package,
                                                         version=version)


@when('I read component toplevel metadata for the package {package} version {version} in ecosystem '
      '{ecosystem} from the AWS S3 database bucket {bucket}')
def read_core_data_from_bucket(context, package, version, ecosystem, bucket):
    key = component_key_into_s3(ecosystem, package, version)
    s3_data = context.s3interface.read_object(bucket, key)
    assert s3_data is not None
    context.s3_data = s3_data


@when('I read {selector} metadata for the package {package} in ecosystem '
      '{ecosystem} from the AWS S3 database bucket {bucket}')
def read_core_package_data_from_bucket(context, selector, package, ecosystem, bucket):
    # At this moment, the following selectors can be used:
    # package toplevel
    # GitHub details
    # keywords tagging
    # libraries io
    if selector == "package toplevel":
        key = package_key_into_s3(ecosystem, package)
    else:
        metadata = S3Interface.selector_to_key(selector)
        key = package_data_key_into_s3(ecosystem, package, metadata)

    s3_data = context.s3interface.read_object(bucket, key)
    assert s3_data is not None
    context.s3_data = s3_data


@then('I should find the correct package toplevel metadata for package {package} '
      'from ecosystem {ecosystem}')
def check_package_toplevel_file(context, package, ecosystem):
    data = context.s3_data

    check_attribute_presence(data, 'id')
    assert int(data['id'])

    check_attribute_presence(data, 'package_id')
    assert int(data['package_id'])

    check_attribute_presence(data, 'analyses')

    check_attribute_presence(data, 'started_at')
    check_timestamp(data['started_at'])

    check_attribute_presence(data, 'finished_at')
    check_timestamp(data['finished_at'])


@when('I wait for new toplevel data for the package {package} version {version} in ecosystem '
      '{ecosystem} in the AWS S3 database bucket {bucket}')
def wait_for_job_toplevel_file(context, package, version, ecosystem, bucket):
    timeout = 300 * 60
    sleep_amount = 10

    key = component_key_into_s3(ecosystem, package, version)

    start_time = datetime.datetime.now(datetime.timezone.utc)

    for _ in range(timeout // sleep_amount):
        current_date = datetime.datetime.now(datetime.timezone.utc)
        try:
            last_modified = context.s3interface.read_object_metadata(bucket, key,
                                                                     "LastModified")
            delta = current_date - last_modified
            # print(current_date, "   ", last_modified, "   ", delta)
            if delta.days == 0 and delta.seconds < sleep_amount * 2:
                # print("done!")
                read_core_data_from_bucket(context, package, version, ecosystem, bucket)
                return
        except ClientError as e:
            print("No analyses yet (waiting for {t})".format(t=current_date - start_time))
        time.sleep(sleep_amount)
    raise Exception('Timeout waiting for the job metadata in S3!')


@when('I remember timestamps from the last component toplevel metadata')
def remember_timestamps_from_job_toplevel_data(context):
    data = context.s3_data
    context.job_timestamp_started_at = data['started_at']
    context.job_timestamp_finished_at = data['finished_at']

    # print("\n\nRemember")
    # print(context.job_timestamp_started_at)
    # print(context.job_timestamp_finished_at)


@then('I should find that timestamps from current toplevel metadata are newer than '
      'remembered timestamps')
def check_new_timestamps(context):
    data = context.s3_data

    # print("\n\nCurrent")
    # print(data['started_at'])
    # print(data['finished_at'])

    check_attribute_presence(data, 'started_at')
    check_timestamp(data['started_at'])

    check_attribute_presence(data, 'finished_at')
    check_timestamp(data['finished_at'])

    remembered_started_at = parse_timestamp(context.job_timestamp_started_at)
    remembered_finished_at = parse_timestamp(context.job_timestamp_finished_at)
    current_started_at = parse_timestamp(data['started_at'])
    current_finished_at = parse_timestamp(data['finished_at'])

    assert current_started_at > remembered_started_at, \
        "Current metadata are not newer: failed on started_at attributes comparison"
    assert current_finished_at > remembered_finished_at, \
        "Current metadata are not newer: failed on finished_at attributes comparison"


@when('I generate unique job ID prefix')
def generate_job_id_prefix(context):
    context.job_id_prefix = uuid.uuid1()


@when('I mock API response by {filename} file')
def read_json_file(context, filename):
    context.response = MockedResponse(filename)


@when('I mock S3 data by content of {filename} file')
def read_json_file_for_s3(context, filename):
    context.s3_data = MockedResponse.json_load(filename)
