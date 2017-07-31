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

import jwt
from jwt.contrib.algorithms.pycrypto import RSAAlgorithm


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


def authorization(context):
    return {'Authorization': 'Bearer {token}'.format(token=context.token)}


def perform_component_search(context, component, use_token):
    url = urljoin(context.coreapi_url, "api/v1/component-search/{component}".format(component=component))
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
def read_analysis_for_component(context, ecosystem, component, version):
    """Read component analysis (or an error message) for the selected
    ecosystem."""
    url = component_analysis_url(context, ecosystem, component, version)
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
def finish_analysis_for_component(context, ecosystem, component, version):
    """Try to wait for the component analysis to be finished.

    Current API implementation returns just two HTTP codes:
    200 OK : analysis is already finished
    404 NOT FOUND: analysis is started or is in progress
    """

    timeout = 600      # in seconds
    sleep_amount = 10  # we don't have to overload the API with too many calls

    url = component_analysis_url(context, ecosystem, component, version)

    for _ in range(timeout//sleep_amount):
        status_code = requests.get(url).status_code
        if status_code == 200:
            break
        elif status_code != 404:
            raise Exception('Bad HTTP status code {c}'.format(c=status_code))
        time.sleep(sleep_amount)
    else:
        raise Exception('Timeout waiting for the component analysis results')


@when("I wait for stack analysis to finish")
@when("I wait for stack analysis version {version} to finish {token} authorization token")
def wait_for_stack_analysis_completion(context, version="1", token="without"):
    """Try to wait for the stack analysis to be finished.

    This step assumes that stack analysis has been started previously and
    thus that the job ID is known

    Current API implementation returns just three HTTP codes:
    200 OK : analysis is already finished
    202 Accepted: analysis is started or is in progress (or other state!)
    401 UNAUTHORIZED : missing or inproper authorization token
    """

    timeout = 600      # in seconds
    sleep_amount = 10  # we don't have to overload the API with too many calls
    use_token = parse_token_clause(token)

    id = context.response.json().get("id")
    context.stack_analysis_id = id
    url = urljoin(stack_analysis_endpoint(context, version), id)

    for _ in range(timeout//sleep_amount):
        if use_token:
            context.response = requests.get(url, headers=authorization(context))
        else:
            context.response = requests.get(url)
        status_code = context.response.status_code
        # 401 code should be checked later
        if status_code in (200, 401):
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


@when('I access jobs API {url}')
def jobs_api_url(context, url):
    """Access the jobs service API using the HTTP GET method."""
    context.response = requests.get(context.jobs_api_url + url)


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
    files = {'manifest[]': (name, open(filename, 'rb')),
             'filePath[]': path_to_manifest_file}
    if use_token:
        response = requests.post(endpoint, files=files,
                                 headers=authorization(context))
    else:
        response = requests.post(endpoint, files=files)
    context.response = response


def stack_analysis_endpoint(context, version):
    endpoint = {"1": "/api/v1/stack-analyses/",
                "2": "/api/v1/stack-analyses-v2/"}.get(version)
    if endpoint is None:
        raise Exception("Wrong version specified: {v}".format(v=version))
    return urljoin(context.coreapi_url, endpoint)


def parse_token_clause(token_clause):
    use_token = {"with": True,
                 "without": False}.get(token_clause)
    if use_token is None:
        raise Exception("Wrong clause specified: {t}".format(t=token_clause))
    return use_token


@when("I send NPM package manifest {manifest} to stack analysis")
@when("I send NPM package manifest {manifest} to stack analysis version {version} {token} authorization token")
def npm_manifest_stack_analysis(context, manifest, version="1", token="without"):
    endpoint = stack_analysis_endpoint(context, version)
    use_token = parse_token_clause(token)
    send_manifest_to_stack_analysis(context, manifest, 'package.json',
                                    endpoint, use_token)


@when("I send Python package manifest {manifest} to stack analysis")
@when("I send Python package manifest {manifest} to stack analysis version {version} {token} authorization token")
def python_manifest_stack_analysis(context, manifest, version="1", token="without"):
    endpoint = stack_analysis_endpoint(context, version)
    use_token = parse_token_clause(token)
    send_manifest_to_stack_analysis(context, manifest, 'requirements.txt',
                                    endpoint, use_token)


@when("I send Maven package manifest {manifest} to stack analysis")
@when("I send Maven package manifest {manifest} to stack analysis version {version} {token} authorization token")
def maven_manifest_stack_analysis(context, manifest, version="1", token="without"):
    endpoint = stack_analysis_endpoint(context, version)
    use_token = parse_token_clause(token)
    send_manifest_to_stack_analysis(context, manifest, 'pom.xml',
                                    endpoint, use_token)


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


def job_endpoint(context, job_id):
    """Return URL for given job id that can be used to job state manipulation."""
    url = "{jobs_api_url}api/v1/jobs".format(
           jobs_api_url=context.jobs_api_url)
    if job_id is not None:
        url = "{url}/{job_id}".format(url=url, job_id=job_id)
    return url


@when("I post a job metadata {metadata} with state {state}")
def perform_post_job(context, metadata, state):
    """API call to create a new job using the provided metadata."""
    filename = job_metadata_filename(metadata)
    endpoint = flow_sheduling_endpoint(context, state)
    context.response = context.send_json_file(endpoint, filename)


@when("I post a job metadata {metadata} with job id {job_id} and state {state}")
def perform_post_job(context, metadata, job_id, state):
    """API call to create a new job using the provided metadata and set a job to given state."""
    filename = job_metadata_filename(metadata)
    endpoint = flow_sheduling_endpoint(context, state, job_id)
    context.response = context.send_json_file(endpoint, filename)


@when("I delete job without id")
@when("I delete job with id {job_id}")
def delete_job(context, job_id=None):
    """API call to delete a job with given ID."""
    endpoint = job_endpoint(context, job_id)
    context.response = requests.delete(endpoint)


@when("I set status for job with id {job_id} to {status}")
def set_job_status(context, job_id, status):
    """API call to set job status."""
    endpoint = job_endpoint(context, job_id)
    url = "{endpoint}?state={status}".format(endpoint=endpoint, status=status)
    context.response = requests.put(url)


@when("I reset status for the job service")
@when("I set status for job service to {status}")
def set_job_service_status(context, status=None):
    """API call to set or reset job service status."""
    url = "{jobs_api_url}api/v1/service/state".format(
            jobs_api_url=context.jobs_api_url)
    if status is not None:
        url = "{url}?state={status}".format(url=url, status=status)
    context.response = requests.put(url)


@when("I clean all failed jobs")
def clean_all_failed_jobs(context):
    """API call to clean up all failed jobs."""
    url = "{url}api/v1/jobs/clean-failed".format(url=context.jobs_api_url)
    context.response = requests.delete(url)


@when("I ask for analyses report for ecosystem {ecosystem}")
def access_analyses_report(context, ecosystem):
    """API call to get analyses report for selected ecosystem."""
    url = "{url}api/v1/debug/analyses-report?ecosystem={ecosystem}".format(
           url=context.jobs_api_url, ecosystem=ecosystem)
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


@then('I should see {num:d} jobs')
def check_jobs(context, num):
    """
    check the number of jobs
    """
    jsondata = context.response.json()
    jobs = jsondata['jobs']
    jobs_count = jsondata['jobs_count']
    assert len(jobs) == num
    assert jobs_count == num


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


@then('I should receive JSON response with the correct id')
def check_id_in_json_response(context):
    """Check the ID attribute in the JSON response.

    Check if ID is in a format like: '477e85660c504b698beae2b5f2a28b4e'
    ie. it is a string with 32 characters containing 32 hexadecimal digits
    """
    id = context.response.json().get("id")
    assert id is not None
    assert isinstance(id, str) and len(id) == 32
    assert all(char in string.hexdigits for char in id)


def check_timestamp(timestamp):
    """Check if the string contains proper timestamp value."""
    assert timestamp is not None
    assert isinstance(timestamp, str)
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
    resp = context.response
    assert resp['status'] == "success"
    assert len(resp['id']) > 0


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
        err = "Stack analyses could not be completed within {t} seconds".format(t=iter*retry_interval)

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


@then('I should find the attribute request_id equals to id returned by stack analysis request')
def check_stack_analysis_id(context):
    previous_id = context.stack_analysis_id
    request_id = context.response.json().get("request_id")
    assert previous_id is not None
    assert request_id is not None
    assert previous_id == request_id


@then('I should find analyzed dependency named {package} with version {version} in the stack analysis')
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


@when('I acquire the authorization token')
def acquire_authorization_token(context):
    recommender_token = os.environ.get("RECOMMENDER_API_TOKEN")
    if recommender_token is not None:
        context.token = recommender_token
    else:
        generate_authorization_token(context, DEFAULT_AUTHORIZATION_TOKEN_FILENAME)


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
    for usage_outlier in usage_outliers:
        if usage_outlier["package_name"] == package_name:
            probability = usage_outlier["outlier_prbability"]
            assert probability is not None
            v = float(probability)
            assert v >= threshold_value and v <= 1.0
            return
    raise Exception("Can not find usage outlier for the package {p}".format(p=package_name))


@then('I should find the proper outlier record for the {component} component')
def stack_analysis_check_outliers(context, component):
    json_data = context.response.json()
    threshold = context.outlier_probability_threshold
    path = "result/0/recommendations/usage_outliers"
    usage_outliers = get_value_using_path(json_data, path)
    check_outlier_probability(usage_outliers, component, threshold)


def check_sentiment(analyzed_packages):
    for package in analyzed_packages:

        assert "sentiment" in package
        sentiment = package["sentiment"]

        if sentiment:
            assert "latest_comment" in sentiment, \
                "'latest_comment' attribute is expected in the node 'sentiment', " \
                "found: %s attributes" % ", ".join(sentiment.keys())

            assert "overall_score" in sentiment, \
                "'overall_score' attribute is expected in the node 'sentiment', " \
                "found: %s attributes" % ", ".join(sentiment.keys())

            overall_score = float(sentiment["overall_score"])

            assert overall_score >= -1.0 and overall_score <= 1.0, \
                "overall_score should fall within -1..1 range, " \
                "found %f value instead" % overall_score

            if overall_score == 0.0:
                if "magnitude" in sentiment:
                    magnitude = float(sentiment["magnitude"])
                    assert magnitude == 0, \
                        "magnitude value should be zero, " \
                        "found %f value instead" % magnitude

            else:  # if magnitude  > 0 then  overall_score   =  -1 to + 1
                assert "magnitude" in sentiment, \
                    "'overall_score is set to nonzero value, " \
                    "but no magnitude was found'"
                magnitude = float(sentiment["magnitude"])
                assert magnitude > 0, \
                    "magnitude value should be greater than zero, " \
                    "found %f value instead" % magnitude


@then('I should find the proper sentiment values in the stack analysis response')
def stack_analysis_check_sentiment(json_data):
    """The structure of sentiment details is:
                        "sentiment": {
                            "latest_comment": "",
                            "magnitude": 0,
                            "overall_score": 0
                        },

    Expected values for these attributes:
    magnitude:  :   >= 0
    overall_score :  -1,  to +1

    usecase:

    if magnitude == 0  then  overall_score   =  0
    if magnitude  > 0 then  overall_score   =  -1 to + 1

    It is applicable for all three blocks of stack analysis response, namely:
        alternate, companion and dependencies.
    """
    json_data = context.response.json()
    recommendations_node = get_value_using_path(json_data,
                                                "result/0/recommendations")
    user_stack_info_node = get_value_using_path(json_data,
                                                "result/0/user_stack_info")

    alternate_node = recommendations_node["alternate"]
    companion_node = recommendations_node["companion"]
    dependencies_node = user_stack_info_node["dependencies"]

    check_sentiment(alternate_node)
    check_sentiment(companion_node)
    check_sentiment(dependencies_node)
