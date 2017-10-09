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

# Do not remove - kept for debugging
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

STACK_ANALYSIS_CONSTANT_FILE_URL = "https://raw.githubusercontent.com/" \
    "fabric8-analytics/fabric8-analytics-stack-analysis/master/" \
    "analytics_platform/kronos/pgm/src/pgm_constants.py"

STACK_ANALYSIS_OUTLIER_PROBABILITY_CONSTANT_NAME = \
    "KRONOS_OUTLIER_PROBABILITY_THRESHOLD_VALUE"

DEFAULT_AUTHORIZATION_TOKEN_FILENAME = "private_key.pem"

jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))


def split_comma_separated_list(l):
    return [i.strip() for i in l.split(',')]


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


@given('Component search service is running')
def running_component_search_api(context):
    """Wait for the component search REST API to be available."""
    if not context.is_component_search_service_running(context):
        context.wait_for_component_search_service(context, 60)


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


def jobs_api_authorization(context):
    return {'auth-token': '{token}'.format(token=context.jobs_api_token)}


def authorization(context):
    return {'Authorization': 'Bearer {token}'.format(token=context.token)}


def perform_component_search(context, component, use_token):
    path = "api/v1/component-search/{component}".format(component=component)
    url = urljoin(context.coreapi_url, path)
    if use_token:
        context.response = requests.get(url, headers=authorization(context))
    else:
        context.response = requests.get(url)


@when("I search for component {component} without authorization token")
def search_for_component_without_token(context, component):
    """Search for given component via the component search REST API call."""
    perform_component_search(context, component, False)


@when("I search for component {component} with authorization token")
def search_for_component_with_token(context, component):
    """Search for given component via the component search REST API call."""
    perform_component_search(context, component, True)


@when("I read {ecosystem}/{component}/{version} component analysis")
@when("I read {ecosystem}/{component}/{version} component analysis "
      "{token} authorization token")
def read_analysis_for_component(context, ecosystem, component, version, token='without'):
    """Read component analysis (or an error message) for the selected
    ecosystem."""
    url = component_analysis_url(context, ecosystem, component, version)

    use_token = parse_token_clause(token)

    if use_token:
        context.response = requests.get(url, headers=authorization(context))
    else:
        context.response = requests.get(url)


def component_analysis_url(context, ecosystem, component, version):
    """Construct URL for the component analyses REST API call."""
    return urljoin(context.coreapi_url,
                   'api/v1/component-analyses/{e}/{c}/{v}'.format(e=ecosystem,
                                                                  c=component,
                                                                  v=version))


@when("I start analysis for component {ecosystem}/{component}/{version}")
def start_analysis_for_component(context, ecosystem, component, version):
    """Start the component analysis.
    Start the analysis for given component and version in selected ecosystem.
    Current API implementation returns just two HTTP codes:
    200 OK : analysis is already finished
    401 UNAUTHORIZED : missing or inproper authorization token
    404 NOT FOUND : analysis is started or is in progress
    It means that this test step should check if 200 OK is NOT returned
    """

    url = component_analysis_url(context, ecosystem, component, version)

    # first check that the analysis is really new
    response = requests.get(url)

    # remember the response for further test steps
    context.response = response

    if response.status_code == 200:
        raise Exception('Bad state: the analysis for component has been '
                        'finished already')
    elif response.status_code not in (401, 404):
        raise Exception('Improper response: expected HTTP status code 401 or 404, '
                        'received {c}'.format(c=response.status_code))


@when("I wait for {ecosystem}/{component}/{version} component analysis to finish")
@when("I wait for {ecosystem}/{component}/{version} component analysis to finish "
      "{token} authorization token")
def finish_analysis_for_component(context, ecosystem, component, version, token='without'):
    """Try to wait for the component analysis to be finished.

    Current API implementation returns just two HTTP codes:
    200 OK : analysis is already finished
    404 NOT FOUND: analysis is started or is in progress
    """

    timeout = context.component_analysis_timeout  # in seconds
    sleep_amount = 10  # we don't have to overload the API with too many calls

    use_token = parse_token_clause(token)

    url = component_analysis_url(context, ecosystem, component, version)

    for _ in range(timeout // sleep_amount):
        if use_token:
            status_code = requests.get(url, headers=authorization(context)).status_code
        else:
            status_code = requests.get(url).status_code
        if status_code == 200:
            break
        elif status_code != 404:
            raise Exception('Bad HTTP status code {c}'.format(c=status_code))
        time.sleep(sleep_amount)
    else:
        raise Exception('Timeout waiting for the component analysis results')


def parse_timestamp(string):
    timeformat = '%Y-%m-%dT%H:%M:%S.%f'
    return datetime.datetime.strptime(string, timeformat)


def contains_alternate_node(json_resp):
    """Check for the existence of alternate node in the stack analysis."""
    result = json_resp.get('result')
    return bool(result) and isinstance(result, list) \
        and (result[0].get('recommendation', {}) or {}).get('alternate', None) is not None


@when("I wait for stack analysis to finish")
@when("I wait for stack analysis to finish {token} authorization token")
@when("I wait for stack analysis version {version} to finish {token} authorization token")
def wait_for_stack_analysis_completion(context, version="2", token="without"):
    """Try to wait for the stack analysis to be finished.

    This step assumes that stack analysis has been started previously and
    thus that the job ID is known

    Current API implementation returns just three HTTP codes:
    200 OK : analysis is already finished
    202 Accepted: analysis is started or is in progress (or other state!)
    401 UNAUTHORIZED : missing or inproper authorization token
    """

    timeout = context.stack_analysis_timeout  # in seconds
    sleep_amount = 10  # we don't have to overload the API with too many calls
    use_token = parse_token_clause(token)

    id = context.response.json().get("id")
    context.stack_analysis_id = id
    # log.info("REQUEST ID: {}\n\n".format(context.stack_analysis_id))
    url = urljoin(stack_analysis_endpoint(context, version), id)
    # log.info("RECOMMENDER API URL: {}\n\n".format(url))

    for _ in range(timeout // sleep_amount):
        if use_token:
            context.response = requests.get(url, headers=authorization(context))
        else:
            context.response = requests.get(url)
        status_code = context.response.status_code
        # log.info("%r" % context.response.json())
        if status_code == 200:
            json_resp = context.response.json()
            if contains_alternate_node(json_resp):
                # log.info('Recommendation found')
                break
        # 401 code should be checked later
        elif status_code == 401:
            break
        elif status_code != 202:
            raise Exception('Bad HTTP status code {c}'.format(c=status_code))
        time.sleep(sleep_amount)
    else:
        raise Exception('Timeout waiting for the stack analysis results')


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


@when("I post a valid {manifest} to {url}")
def perform_valid_manifest_post(context, manifest, url):
    """Post a manifest to selected core API endpont."""
    filename = "data/{manifest}".format(manifest=manifest)
    files = {'manifest[]': open(filename, 'rb')}
    endpoint = "{coreapi_url}{url}".format(coreapi_url=context.coreapi_url, url=url)
    response = requests.post(endpoint, files=files)
    response.raise_for_status()
    context.response = response.json()
    print(response.json())


def send_manifest_to_stack_analysis(context, manifest, name, endpoint, use_token):
    """Send the selected manifest file to stack analysis."""
    filename = 'data/{manifest}'.format(manifest=manifest)
    manifest_file_dir = os.path.dirname(filename)
    path_to_manifest_file = os.path.abspath(manifest_file_dir)

    # please note that the trick with (None, path_to_manifest_file) has to be
    # used here so the REST API call would work properly. It is similar to use
    # curl -F 'manifest[]=@filename' -F 'filePath[]=PATH_TO_FILE'
    files = {'manifest[]': (name, open(filename, 'rb')),
             'filePath[]': (None, path_to_manifest_file)}
    if use_token:
        response = requests.post(endpoint, files=files,
                                 headers=authorization(context))
    else:
        response = requests.post(endpoint, files=files)
    context.response = response


def stack_analysis_endpoint(context, version):
    # please note that the stack analysis v2 now becames the only available endpoint
    endpoint = {"1": "/api/v1/stack-analyses-v1/",
                "2": "/api/v1/stack-analyses/"}.get(version)
    if endpoint is None:
        raise Exception("Wrong version specified: {v}".format(v=version))
    return urljoin(context.coreapi_url, endpoint)


def parse_token_clause(token_clause):
    use_token = {"with": True,
                 "using": True,
                 "without": False}.get(token_clause)
    if use_token is None:
        raise Exception("Wrong clause specified: {t}".format(t=token_clause))
    return use_token


@when("I send NPM package manifest {manifest} to stack analysis")
@when("I send NPM package manifest {manifest} to stack analysis {token} authorization token")
@when("I send NPM package manifest {manifest} to stack analysis version {version} {token} "
      "authorization token")
def npm_manifest_stack_analysis(context, manifest, version="2", token="without"):
    endpoint = stack_analysis_endpoint(context, version)
    use_token = parse_token_clause(token)
    send_manifest_to_stack_analysis(context, manifest, 'package.json',
                                    endpoint, use_token)


@when("I send Python package manifest {manifest} to stack analysis")
@when("I send Python package manifest {manifest} to stack analysis {token} authorization token")
@when("I send Python package manifest {manifest} to stack analysis version {version} {token} "
      "authorization token")
def python_manifest_stack_analysis(context, manifest, version="2", token="without"):
    endpoint = stack_analysis_endpoint(context, version)
    use_token = parse_token_clause(token)
    send_manifest_to_stack_analysis(context, manifest, 'requirements.txt',
                                    endpoint, use_token)


@when("I send Maven package manifest {manifest} to stack analysis")
@when("I send Maven package manifest {manifest} to stack analysis {token} authorization token")
@when("I send Maven package manifest {manifest} to stack analysis version {version} {token} "
      "authorization token")
def maven_manifest_stack_analysis(context, manifest, version="2", token="without"):
    endpoint = stack_analysis_endpoint(context, version)
    use_token = parse_token_clause(token)
    send_manifest_to_stack_analysis(context, manifest, 'pom.xml',
                                    endpoint, use_token)


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


@then('I should see 0 components')
@then('I should see {num:d} components ({components}), all from {ecosystem} ecosystem')
def check_components(context, num=0, components='', ecosystem=''):
    components = split_comma_separated_list(components)

    json_data = context.response.json()

    search_results = json_data['result']
    assert len(search_results) == num
    for search_result in search_results:
        assert search_result['ecosystem'] == ecosystem
        assert search_result['name'] in components


def print_search_results(search_results):
    print("\n\n\n")
    print("The following components can be found")
    for r in search_results:
        print(r)
    print("\n\n\n")


@then('I should find the analysis for the component {component} from ecosystem {ecosystem}')
def check_component_analysis_existence(context, component, ecosystem):
    json_data = context.response.json()
    search_results = json_data['result']

    for search_result in search_results:
        if search_result['ecosystem'] == ecosystem and \
           search_result['name'] == component:
            return

    # print_search_results(search_results)

    raise Exception('Component {component} for ecosystem {ecosystem} could not be found'.
                    format(component=component, ecosystem=ecosystem))


@then('I should not find the analysis for the {component} from ecosystem {ecosystem}')
def check_component_analysis_nonexistence(context, component, ecosystem):
    json_data = context.response.json()
    search_results = json_data['result']

    for search_result in search_results:
        if search_result['ecosystem'] == ecosystem and \
           search_result['name'] == component:
            raise Exception('Component {component} for ecosystem {ecosystem} was found'.
                            format(component=component, ecosystem=ecosystem))


@then('I should see {num:d} versions ({versions}), all for {ecosystem}/{package} package')
def check_versions(context, num=0, versions='', ecosystem='', package=''):
    versions = split_comma_separated_list(versions)
    vrsns = context.response.json()['items']
    assert len(vrsns) == num
    for v in vrsns:
        assert v['ecosystem'] == ecosystem
        assert v['package'] == package
        assert v['version'] in versions


def _is_empty_json_response(context):
    return context.response.json() == {}


@then('I should receive empty JSON response')
@then('I should see empty analysis')
def check_json(context):
    assert _is_empty_json_response(context)


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


def check_id_value(context, id_attribute_name):
    """Check the ID attribute in the JSON response.

    Check if ID is in a format like: '477e85660c504b698beae2b5f2a28b4e'
    ie. it is a string with 32 characters containing 32 hexadecimal digits
    """
    response = context.response
    json_data = response.json()

    assert json_data is not None

    check_attribute_presence(json_data, id_attribute_name)
    id = json_data[id_attribute_name]

    assert id is not None
    assert isinstance(id, str) and len(id) == 32
    assert all(char in string.hexdigits for char in id)


@then('I should receive JSON response with the correct id')
def check_id_in_json_response(context):
    """Check the ID attribute in the JSON response.

    Check if ID is in a format like: '477e85660c504b698beae2b5f2a28b4e'
    ie. it is a string with 32 characters containing 32 hexadecimal digits
    """
    check_id_value(context, "id")


def check_audit_metadata(data):
    """Check if all common attributes can be found in the audit node
    in the component or package metadata."""
    assert "_audit" in data
    audit = data["_audit"]

    assert "version" in audit
    assert audit["version"] == "v1"

    assert "started_at" in audit
    check_timestamp(audit["started_at"])

    assert "ended_at" in audit
    check_timestamp(audit["ended_at"])


def check_timestamp(timestamp):
    """Check if the string contains proper timestamp value."""
    assert timestamp is not None
    assert isinstance(timestamp, str)

    # some attributes contains timestamp without the millisecond part
    # so we need to take care of it
    if len(timestamp) == len("YYYY-mm-dd HH:MM:SS") and '.' not in timestamp:
        timestamp += '.0'

    assert len(timestamp) >= len("YYYY-mm-dd HH:MM:SS.")

    # we have to support the following formats:
    #    2017-07-19 13:05:25.041688
    #    2017-07-17T09:05:29.101780
    # -> it is needed to distinguish the 'T' separator
    #
    # (please see https://www.tutorialspoint.com/python/time_strptime.htm for
    #  an explanation how timeformat should look like)

    timeformat = "%Y-%m-%d %H:%M:%S.%f"
    if timestamp[10] == "T":
        timeformat = "%Y-%m-%dT%H:%M:%S.%f"

    # just try to parse the string to check whether
    # the ValueError exception is raised or not
    datetime.datetime.strptime(timestamp, timeformat)


@then('I should receive JSON response with the correct timestamp in attribute {attribute}')
def check_timestamp_in_json_response(context, attribute):
    """Check the timestamp stored in the JSON response.

    Check if the attribute in the JSON response object contains
    proper timestamp value
    """
    timestamp = context.response.json().get(attribute)
    check_timestamp(timestamp)


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
    check_id_value(context, "request_id")


@then("I should find the status attribute set to success")
def check_stack_analyses_request_id(context):
    response = context.response
    json_data = response.json()

    check_attribute_presence(json_data, 'status')

    assert json_data['status'] == "success"


@then("stack analyses response is available via {url}")
def check_stack_analyses_response(context, url):
    """Check the stack analyses response available on the given URL."""
    response = context.response
    resp = response.json()

    assert len(resp["results"]) >= 1
    request_id = resp["results"][0]["id"]
    url = "{base_url}{endpoint}{request_id}".format(
                base_url=context.coreapi_url,
                endpoint=url, request_id=request_id)
    get_resp = requests.get(url)
    if get_resp.status_code == 202:  # in progress
        # Allowing enough retries for component analyses to complete
        retry_count = 30
        retry_interval = 20
        iter = 0
        while iter < retry_count:
            iter += 1
            get_resp = requests.get(url)
            if get_resp.status_code != 202:  # not in progress
                break
            time.sleep(retry_interval)

    if iter == retry_count:
        err = "Stack analyses could not be completed within {t} seconds".format(
            t=iter * retry_interval)

    resp_json = get_resp.json()

    # ensure that the stack analyses result has been asserted in the loop
    assert resp_json.get("status") == "success", err

    # ensure that the response is in accordance to the Stack Analyses schema
    schema = requests.get(resp_json["schema"]["url"]).json()
    jsonschema.validate(resp_json, schema)


def get_value_using_path(obj, path):
    """Get the attribute value using the XMLpath-like path specification.
    Return any attribute stored in the nested object and list hierarchy using
    the 'path' where path consists of:
        keys (selectors)
        indexes (in case of arrays)
    separated by slash, ie. "key1/0/key_x".

    Usage:
    get_value_using_path({"x" : {"y" : "z"}}, "x"))   -> {"y" : "z"}
    get_value_using_path({"x" : {"y" : "z"}}, "x/y")) -> "z"
    get_value_using_path(["x", "y", "z"], "0"))       -> "x"
    get_value_using_path(["x", "y", "z"], "1"))       -> "y"
    get_value_using_path({"key1" : ["x", "y", "z"],
                          "key2" : ["a", "b", "c", "d"]}, "key1/1")) -> "y"
    get_value_using_path({"key1" : ["x", "y", "z"],
                          "key2" : ["a", "b", "c", "d"]}, "key2/1")) -> "b"
    """

    keys = path.split("/")
    for key in keys:
        if key.isdigit():
            obj = obj[int(key)]
        else:
            obj = obj[key]
    return obj


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


def download_file_from_url(url):
    """Download file from the given URL and do basic check of response."""
    response = requests.get(url)
    assert response.status_code == 200
    assert response.text is not None
    return response.text


def parse_float_value_from_text_stream(text, key):
    """Go through all lines of the text file, find the line with given key
    and parse float value specified here"""
    regexp = key + "\s*=\s*(\d.\d*)"
    for line in text.split("\n"):
        if line.startswith(key):
            match = re.fullmatch(regexp, line)
            assert match is not None
            assert match.lastindex == 1
            return float(match.group(1))


@when('I download and parse outlier probability threshold value')
def download_and_parse_outlier_probability_threshold_value(context):
    """Special step that is needed to get the stack analysis outlier
    probability threshold."""
    content = download_file_from_url(STACK_ANALYSIS_CONSTANT_FILE_URL)
    context.outlier_probability_threshold = parse_float_value_from_text_stream(
        content, STACK_ANALYSIS_OUTLIER_PROBABILITY_CONSTANT_NAME)


@then('I should have outlier probability threshold value between {min:f} and {max:f}')
def check_outlier_probability_threshold_value(context, min, max):
    v = context.outlier_probability_threshold
    assert v is not None
    assert v >= min
    assert v <= max


def check_outlier_probability(usage_outliers, package_name, threshold_value):
    """Try to find outlier probability for given package is found and that
    its probability is within permitted range."""

    # NOTE: there's a typo in the attribute name (issue #73)
    # the following line should be updated after the issue ^^^ will be fixed
    outlier_probability_attribute = "outlier_prbability"

    for usage_outlier in usage_outliers:
        if usage_outlier["package_name"] == package_name:
            assert outlier_probability_attribute in usage_outlier, \
                "'%s' attribute is expected in the node, " \
                "found: %s attributes " % (outlier_probability_attribute,
                                           ", ".join(usage_outlier.keys()))
            probability = usage_outlier[outlier_probability_attribute]
            assert probability is not None
            v = float(probability)
            assert v >= threshold_value and v <= 1.0, \
                "outlier_prbability value should fall within %f..1.0 range, "\
                "found %f value instead" % (threshold_value, v)
            return
    raise Exception("Can not find usage outlier for the package {p}".format(p=package_name))


@then('I should find the proper outlier record for the {component} component')
def stack_analysis_check_outliers(context, component):
    json_data = context.response.json()
    threshold = context.outlier_probability_threshold
    # log.info('Usage outlier threshold: %r' % threshold)
    path = "result/0/recommendation/usage_outliers"
    usage_outliers = get_value_using_path(json_data, path)
    check_outlier_probability(usage_outliers, component, threshold)


@then('I should find that total {count} outliers are reported')
def check_outlier_count(context, count=2):
    json_data = context.response.json()
    path = "result/0/recommendation/usage_outliers"
    usage_outliers = get_value_using_path(json_data, path)
    assert len(usage_outliers) == int(count)


@then('I should find that valid outliers are reported')
def check_outlier_validity(context):
    json_data = context.response.json()
    threshold = 0.9
    path = "result/0/recommendation/usage_outliers"
    usage_outliers = get_value_using_path(json_data, path)
    for usage_outlier in usage_outliers:
        # log.info("PACKAGE: {}".format(usage_outlier["package_name"]))
        check_outlier_probability(usage_outliers, usage_outlier["package_name"], threshold)


def check_licenses(node, expected_licenses):
    for item in node:
        licenses = item["licenses"]
        assert licenses is not None
        for license in licenses:
            if license not in expected_licenses:
                raise Exception("Unexpected license found: {license}".format(
                                license=license))


@then('I should find the following licenses ({licenses}) under the path {path}')
def stack_analysis_check_licenses(context, licenses, path):
    licenses = split_comma_separated_list(licenses)
    json_data = context.response.json()
    node = get_value_using_path(json_data, path)
    assert node is not None
    check_licenses(node, licenses)


def get_attribute_values(list, attribute_name):
    return [item[attribute_name] for item in list]


def get_analyzed_packages(json_data):
    """Get names of all analyzed packages."""
    path = "result/0/user_stack_info/analyzed_dependencies"
    analyzed_packages = get_value_using_path(json_data, path)
    return get_attribute_values(analyzed_packages, "package")


def get_companion_packages(json_data):
    """Get names of all packages in companion list."""
    path = "result/0/recommendation/companion"
    companion = get_value_using_path(json_data, path)
    return get_attribute_values(companion, "name")


@then('I should find that none analyzed package can be found in companion packages as well')
def stack_analysis_check_companion_packages(context):

    json_data = context.response.json()

    # those two lists should have no element in common
    analyzed_packages = get_analyzed_packages(json_data)
    companion_packages = get_companion_packages(json_data)

    for companion_package in companion_packages:
        assert companion_package not in analyzed_packages, \
            "The analyzed package '%s' is found in companion packages as well" \
            % companion_package


@then('I should get {field_name} field in stack report')
def verify_stack_level_license_info(context, field_name):
    json_data = context.response.json()
    path = 'result/0/user_stack_info'
    user_stack_info = get_value_using_path(json_data, path)
    assert user_stack_info.get(field_name, None) is not None


def replaces_component(replacement, component, version):
    assert "replaces" in replacement
    replaces = replacement["replaces"]
    for replace in replaces:
        assert "name" in replace
        assert "version" in replace
        if replace["name"] == component and replace["version"] == version:
            return True
    return False


def find_replacements(alternates, component, version):
    return [replacement
            for replacement in alternates
            if replaces_component(replacement, component, version)]


@then('I should find that the component {component} version {version} can be replaced by '
      'component {replaced_by} version {replacement_version}')
def stack_analysis_check_replaces(json_data, component, version, replaced_by, replacement_version):
    """Check that the component is replaced by the given package
       and version."""
    json_data = context.response.json()
    path = "result/0/recommendation/alternate"
    alternates = get_value_using_path(json_data, path)
    replacements = find_replacements(alternates, component, version)

    for replacement in replacements:
        if replacement["name"] == replaced_by and \
           replacement["version"] == replacement_version:
            break
    else:
        raise Exception("Can not found expected replacement for the component"
                        " {component} {version}".format(component=component,
                                                        version=version))


@then('I should find that the component {component} version {version} has only one replacement')
@then('I should find that the component {component} version {version} has '
      '{expected_replacements:d} replacements')
def stack_analysis_check_replaces_count(json_data, component, version, expected_replacements=1):
    """Check that the component is replaced only once in the alternate
       analysis."""
    json_data = context.response.json()
    path = "result/0/recommendation/alternate"
    alternates = get_value_using_path(json_data, path)
    replacements = find_replacements(alternates, component, version)
    replacements_count = len(replacements)

    assert replacements_count == expected_replacements, \
        "there must be just %d replacement(s), " \
        "but %d replacements have been found" % (expected_replacements, replacements_count)


def get_user_components(json_data):
    path = "result/0/user_stack_info/analyzed_dependencies"
    return get_value_using_path(json_data, path)


def get_alternate_components(json_data):
    path = "result/0/recommendation/alternate"
    return get_value_using_path(json_data, path)


def check_attribute_presence(node, attribute_name):
    '''Check the attribute presence in the dictionary. To be used for deserialized JSON data etc.'''
    assert attribute_name in node, \
        "'%s' attribute is expected in the node, " \
        "found: %s attributes " % (attribute_name, ", ".join(node.keys()))


def check_and_get_attribute(node, attribute_name):
    '''Check the attribute presence and if the attribute is found, return its value.'''
    check_attribute_presence(node, attribute_name)
    return node[attribute_name]


def perform_alternate_components_validation(json_data):
    user_components = get_user_components(json_data)

    # in order to use the 'in' operator later we need to have a sequence
    # of dictionaries with 'name' and 'version' keys
    user_components = [{"name": c["package"],
                        "version": c["version"]} for c in user_components]
    alternate_components = get_alternate_components(json_data)

    for alternate_component in alternate_components:

        check_attribute_presence(alternate_component, "name")

        check_attribute_presence(alternate_component, "replaces")
        replaces = alternate_component["replaces"]

        for replace in replaces:
            check_attribute_presence(replace, "name")
            r_name = replace["name"]

            check_attribute_presence(replace, "version")
            r_version = replace["version"]

            assert replace in user_components,  \
                "The component %s version %s does not replace any user " \
                "component" % (r_name, r_version)


@then('I should find that alternate components replace user components')
def stack_analysis_validate_alternate_components(context):
    json_data = context.response.json()
    assert json_data is not None, \
        "JSON response from the previous request does not exist"
    perform_alternate_components_validation(json_data)


def check_cve_value(cve):
    pattern = "CVE-([0-9]{4})-[0-9]{4,}"

    match = re.fullmatch(pattern, cve)
    assert match is not None, "Improper CVE number %s" % cve

    year = int(re.fullmatch(pattern, cve).group(1))
    current_year = datetime.datetime.now().year

    # well the lower limit is a bit arbitrary
    # (according to SRT guys it should be 1999)
    assert year >= 1999 and year <= current_year


def check_cvss_value(cvss):
    score = float(cvss)
    # TODO: check the specificaion how to calculate the maximum possible value
    # https://www.first.org/cvss/specification-document
    assert score >= 0.0, "CVSS score must be >= 0.0"
    assert score <= 10.0, "CVSS score must be <= 10.0"


def check_security_node(context, path):
    json_data = context.response.json()
    assert json_data is not None

    components = get_value_using_path(json_data, path)
    assert components is not None

    for component in components:
        check_attribute_presence(component, "security")
        cve_items = component["security"]
        for cve_item in cve_items:
            check_attribute_presence(cve_item, "CVE")
            check_attribute_presence(cve_item, "CVSS")
            cve = cve_item["CVE"]
            cvss = cve_item["CVSS"]
            check_cve_value(cve)
            check_cvss_value(cvss)


@then('I should find the security node for all dependencies')
def stack_analysis_check_security_node_for_dependencies(context):
    check_security_node(context, "result/0/user_stack_info/dependencies")


@then('I should find the security node for all alternate components')
def stack_analysis_check_security_node_for_alternate_components(context):
    check_security_node(context, "result/0/recommendation/alternate")


@then('I should find the {cve} security issue for the dependency {package}')
def check_security_issue_existence(context, cve, package):
    '''Check if the security issue CVE-yyyy-xxxx can be found for the given
    analyzed package.'''
    json_data = context.response.json()
    assert json_data is not None

    path = "result/0/user_stack_info/dependencies"
    components = get_value_using_path(json_data, path)
    assert components is not None

    for component in components:
        if component["name"] == package:
            check_attribute_presence(component, "security")
            cve_items = component["security"]
            for cve_item in cve_items:
                check_attribute_presence(cve_item, "CVE")
                if cve_item["CVE"] == cve:
                    return
            else:
                raise Exception('Could not find the CVE {c} for the '
                                'package {p}'.format(c=cve, p=package))
    else:
        raise Exception('Could not find the analyzed package {p}'
                        .format(p=package))


def check_job_token_attributes(token):
    attribs = ["limit", "remaining", "reset"]
    for attr in attribs:
        assert attr in token
        assert int(token[attr]) >= 0


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


def selector_to_key(selector):
    return selector.lower().replace(" ", "_")


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
        metadata = selector_to_key(selector)
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


def check_status_attribute(data):
    check_attribute_presence(data, "status")
    assert data["status"] in ["success", "error"]


def release_string(ecosystem, package, version=None):
    return "{e}:{p}:{v}".format(e=ecosystem, p=package, v=version)


def check_release_attribute(data, ecosystem, package, version=None):
    check_attribute_presence(data, "_release")
    assert data["_release"] == release_string(ecosystem, package, version)


def check_schema_attribute(data, expected_schema_name, expected_schema_version):
    check_attribute_presence(data, "schema")

    schema = data["schema"]
    name = check_and_get_attribute(schema, "name")
    version = check_and_get_attribute(schema, "version")

    assert name == expected_schema_name, "Schema name '{n1}' is different from " \
        "expected name '{n2}'".format(n1=name, n2=expected_schema_name)

    assert version == expected_schema_version, "Schema version {v1} is different from expected " \
        "version {v2}".format(v1=version, v2=expected_schema_version)


@then('I should find the correct GitHub details metadata for package {package} '
      'from ecosystem {ecosystem}')
def check_github_details_file(context, package, ecosystem):
    data = context.s3_data

    check_audit_metadata(data)
    check_release_attribute(data, ecosystem, package)
    check_status_attribute(data)

    check_attribute_presence(data, "summary")
    check_attribute_presence(data, "details")

    check_schema_attribute(data, "github_details", "1-0-4")


@then('I should find empty details about GitHub repository')
def check_empty_github_details(context):
    details = get_details_node(context)
    assert not details, "Empty 'details' node is expected"


@then('I should find the correct keywords tagging metadata for package {package} '
      'from ecosystem {ecosystem}')
def check_keywords_tagging_file(context, package, ecosystem):
    data = context.s3_data

    check_audit_metadata(data)
    check_release_attribute(data, ecosystem, package)
    check_status_attribute(data)

    details = get_details_node(context)
    check_attribute_presence(details, "package_name")
    check_attribute_presence(details, "repository_description")


@then('I should find the correct libraries io metadata for package {package} '
      'from ecosystem {ecosystem}')
def check_libraries_io_file(context, package, ecosystem):
    data = context.s3_data

    check_audit_metadata(data)
    check_release_attribute(data, ecosystem, package)
    check_status_attribute(data)


@then('I should find the correct component core data for package {package} version {version} '
      'from ecosystem {ecosystem}')
def check_component_core_data(context, package, version, ecosystem):
    pass


@then('I should find the correct dependency snapshot data for package {package} version {version} '
      'from ecosystem {ecosystem}')
def check_component_dependency_snapshot_data(context, package, version, ecosystem):
    data = context.s3_data

    check_audit_metadata(data)
    check_release_attribute(data, ecosystem, package, version)
    check_schema_attribute(data, "dependency_snapshot", "1-0-0")

    status = check_and_get_attribute(data, "status")
    assert status == "success"


@then('I should find {num:d} runtime details in dependency snapshot')
def check_runtime_dependency_count(context, num):
    data = context.s3_data

    details = check_and_get_attribute(data, "details")
    runtime = check_and_get_attribute(details, "runtime")

    cnt = len(runtime)
    assert cnt == num, "Expected {n1} runtime details, but found {n2}".format(n1=num, n2=cnt)


@then('I should find {num:d} dependencies in dependency snapshot summary')
def check_runtime_dependency_count_in_summary(context, num):
    data = context.s3_data

    summary = check_and_get_attribute(data, "summary")
    dependency_counts = check_and_get_attribute(summary, "dependency_counts")
    runtime_count = check_and_get_attribute(dependency_counts, "runtime")

    cnt = int(runtime_count)
    assert cnt == num, "Expected {n1} runtime dependency counts, but found {n2}".format(
        n1=num, n2=cnt)


@then('I should find the correct digest data for package {package} version {version} '
      'from ecosystem {ecosystem}')
def check_component_digest_data(context, package, version, ecosystem):
    pass


@then('I should find the correct keywords tagging data for package {package} version {version} '
      'from ecosystem {ecosystem}')
def check_component_keywords_tagging_data(context, package, version, ecosystem):
    pass


@then('I should find the correct Red Hat downstream data for package {package} version {version} '
      'from ecosystem {ecosystem}')
def check_component_redhat_downstream_data(context, package, version, ecosystem):
    pass


@then('I should find the correct security issues data for package {package} version {version} '
      'from ecosystem {ecosystem}')
def check_component_security_issues_data(context, package, version, ecosystem):
    pass


@then('I should find the correct source licenses data for package {package} version {version} '
      'from ecosystem {ecosystem}')
def check_component_source_licenses_data(context, package, version, ecosystem):
    pass


def get_details_node(context):
    data = context.s3_data

    return check_and_get_attribute(data, 'details')


def get_releases_node_from_libraries_io(context):
    details = get_details_node(context)

    return check_and_get_attribute(details, 'releases')


@then('I should find that the latest package version {version} was published on {date}')
def check_latest_package_version_publication(context, version, date):
    '''Check the latest package version and publication date.'''
    releases = get_releases_node_from_libraries_io(context)

    latest_release = check_and_get_attribute(releases, 'latest')

    check_attribute_presence(latest_release, "version")
    check_attribute_presence(latest_release, "published_at")

    stored_version = latest_release["version"]
    stored_date = latest_release["published_at"]

    assert stored_version == version, \
        "Package latest version differs, {v} is expected, but {f} is found instead".\
        format(v=version, f=stored_version)

    assert latest_release["published_at"] == date, \
        "Package latest release data differs, {d} is expected, but {f} is found instead".\
        format(d=date, f=stored_date)


@then('I should find that the recent package version {version} was published on {date}')
def check_recent_package_version_publication(context, version, date):
    releases = get_releases_node_from_libraries_io(context)

    # TODO: update together with https://github.com/openshiftio/openshift.io/issues/1040
    latest_release = check_and_get_attribute(releases, 'latest')

    recent_releases = check_and_get_attribute(latest_release, 'recent')

    # try to find the exact version published at given date
    for v, published_at in recent_releases.items():
        if v == version and date == published_at:
            return

    # nothing was found
    raise Exception('Can not find the package recent version {v} published at {d}'.format(
        v=version, d=date))


@then('I should find {expected_count:d} releases for this package')
def check_releases_count(context, expected_count):
    releases = get_releases_node_from_libraries_io(context)

    releases_count = check_and_get_attribute(releases, 'count')

    assert int(releases_count) == expected_count, \
        "Expected {e} releases, but found {f}".format(e=expected_count, f=releases_count)


@then('I should find {expected_repo_count:d} dependent repositories for this package')
def check_dependent_repositories_count(context, expected_repo_count):
    details = get_details_node(context)

    dependent_repositories = check_and_get_attribute(details, 'dependent_repositories')

    repo_count = check_and_get_attribute(dependent_repositories, 'count')

    assert int(repo_count) == expected_repo_count, \
        "Expected {e} repositories, but found {f} instead".format(e=expected_repo_count,
                                                                  f=repo_count)


@then('I should find {expected_dependents_count:d} dependent projects for this package')
def check_dependents_count(context, expected_dependents_count):
    details = get_details_node(context)

    dependents = check_and_get_attribute(details, 'dependents')

    dependents_count = check_and_get_attribute(dependents, 'count')

    assert int(dependents_count) == expected_dependents_count, \
        "Expected {e} dependents, but found {f} instead".format(e=expected_dependents_count,
                                                                f=dependents_count)


@then('I should find the correct component toplevel metadata for package {package} '
      'version {version} ecosystem {ecosystem} with latest version {latest}')
def check_component_toplevel_file(context, package, version, ecosystem, latest):
    data = context.s3_data

    check_attribute_presence(data, 'ecosystem')
    assert data['ecosystem'] == ecosystem

    check_attribute_presence(data, 'package')
    assert data['package'] == package

    check_attribute_presence(data, 'version')
    assert data['version'] == version

    check_attribute_presence(data, 'latest_version')
    assert data['latest_version'] == latest

    release = "{ecosystem}:{package}:{version}".format(ecosystem=ecosystem,
                                                       package=package,
                                                       version=version)
    check_attribute_presence(data, 'release')
    assert data['release'] == release

    check_attribute_presence(data, 'started_at')
    check_timestamp(data['started_at'])

    check_attribute_presence(data, 'finished_at')
    check_timestamp(data['finished_at'])


@then('I should find the weight for the word {word} in the {where}')
def check_weight_for_word_in_keywords_tagging(context, word, where):
    selector = selector_to_key(where)
    assert selector in ["package_name", "repository_description"]

    details = get_details_node(context)
    word_dict = check_and_get_attribute(details, selector)

    check_attribute_presence(word_dict, word)
    assert float(word_dict[word]) > 0.0


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


class MockedResponse():
    def __init__(self, filename):
        with open(filename) as data_file:
            self.content = json.load(data_file)

    def json(self):
        return self.content


@when('I mock API response by {filename} file')
def read_json_file(context, filename):
    context.response = MockedResponse(filename)


@when('I mock S3 data by content of {filename} file')
def read_json_file(context, filename):
    with open(filename) as data_file:
        context.s3_data = json.load(data_file)
