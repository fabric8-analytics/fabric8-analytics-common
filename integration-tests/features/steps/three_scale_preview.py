"""Tests for stack-analyses, component-analyses, submit-feedback API via 3scale."""
import requests
import os
import time

from behave import when, then, given
from urllib.parse import urljoin
from src.parsing import parse_token_clause
from src.stack_analysis_common import contains_alternate_node


def threescale_preview_endpoint_url(context, endpoint, epv=[]):
    """Return url for the endpoint of threescale_preview."""
    _endpoints = {'stack-analyses': '/api/v1/stack-analyses/',
                  'component-analyses': '/api/v1/component-analyses/{}/{}/{}/',  # eco, pkg, ver
                  'submit-feedback': '/api/v1/submit-feedback/'
                  }
    endpoint = _endpoints.get(endpoint)
    if not endpoint:
        raise ValueError("Provide the supported endpoint name"
                         "[stack-analyses, component-analyses, submit-feedback]")
    return urljoin(context.threescale_preview_url, endpoint.format(*epv))


def perform_component_analysis(context, ecosystem, package, version, use_user_key, rate):
    """Call API endpoint to analysis for component."""
    context.duration = None
    start_time = time.time()
    url = threescale_preview_endpoint_url(
        context, 'component-analyses', [ecosystem, package, version])
    if use_user_key:
        for _ in range(rate):
            context.response = requests.get(
                url, params={'user_key': context.three_scale_preview_user_key})
            # break the loop if rate limit exceeded
            if context.response.status_code == 429:
                break
    else:
        context.response = requests.get(url)
    end_time = time.time()
    context.duration = end_time - start_time


def send_manifest_to_stack_analyses(context, manifest, name, endpoint, user_key, rate, origin,
                                    ecosystem):
    """Send the selected manifest file to stack analyses."""
    filename = 'data/{manifest}'.format(manifest=manifest)
    manifest_file_dir = os.path.dirname(filename)
    path_to_manifest_file = os.path.abspath(manifest_file_dir)

    # please note that the trick with (None, path_to_manifest_file) has to be
    # used here so the REST API call would work properly. It is similar to use
    # curl -F 'manifest[]=@filename' -F 'filePath[]=PATH_TO_FILE'
    files = {'manifest[]': (name, open(filename, 'rb')),
             'filePath[]': (None, path_to_manifest_file)}
    if user_key:
        for _ in range(rate):
            response = requests.post(endpoint, files=files, params={
                                    'user_key': context.three_scale_preview_user_key},
                                    headers={'origin': origin, 'ecosystem': ecosystem})
            # break the loop if rate limit exceeded
            if response.status_code == 429:
                break
    else:
        response = requests.post(endpoint, files=files)
    context.response = response


def test_stack_analyses_with_deps_file(context, manifest, endpoint, user_key, rate,
                                       ecosystem, origin):
    """Send the selected dependencies file for stack analysis."""
    filename = 'data/{manifest}'.format(manifest=manifest)
    manifest_file_dir = os.path.abspath(os.path.dirname(filename))

    context.manifest = manifest

    # in the new API version the manifest names are hard coded
    if ecosystem == "pypi":
        # only two manifest names are supported ATM:
        # 1) pylist.json
        # 2) requirements.txt
        if manifest.endswith(".json"):
            manifest = "pylist.json"
        else:
            manifest = "requirements.txt"
    elif ecosystem == "node":
        # only two manifest names are supported ATM:
        # 1) packages.json
        # 2) npm.json
        manifest = "npmlist.json"
    elif ecosystem == "maven":
        # only two manifest names are supported ATM:
        # 1) pox.xml
        # 2) dependencies.txt
        manifest = "dependencies.txt"
    files = {'manifest[]': (manifest, open(filename, 'rb')),
             'filePath[]': (None, manifest_file_dir)}
    if user_key:
        response = requests.post(endpoint, files=files, params={
                                 'user_key': context.three_scale_preview_user_key},
                                 headers={'origin': origin, 'ecosystem': ecosystem})
    else:
        response = requests.post(endpoint, files=files)
    context.response = response


@given('Three scale preview service is running')
def running_component_search_api(context):
    """Check three scale preview service is available."""
    assert context.is_3scale_preview_running(context)


@when("I send NPM package manifest {manifest} to stack analysis through "
      "3scale gateway {user_key} user_key")
@when("I send NPM package manifest {manifest} to stack analysis {rate:d} times"
      " in a minute through 3scale gateway {user_key} user_key")
def npm_manifest_stack_analysis(context, manifest, version=3, user_key="without", rate=1):
    """Send the NPM package manifest file to the stack analyses."""
    endpoint = threescale_preview_endpoint_url(context, 'stack-analyses')
    use_user_key = parse_token_clause(user_key)
    send_manifest_to_stack_analyses(context, manifest, 'npmlist.json',
                                    endpoint, use_user_key, rate, ecosystem='npm', origin='vscode')


@when("I send Python package manifest {manifest} to stack analysis through "
      "3scale gateway {user_key} user_key")
@when("I send Python package manifest {manifest} to stack analysis {rate:d} times"
      " in a minute through 3scale gateway {user_key} user_key")
def python_manifest_stack_analysis(context, manifest, version=3, user_key="without", rate=1):
    """Send the NPM package manifest file to the stack analyses."""
    endpoint = threescale_preview_endpoint_url(context, 'stack-analyses')
    use_user_key = parse_token_clause(user_key)
    send_manifest_to_stack_analyses(context, manifest, 'pylist.json',
                                    endpoint, use_user_key, rate, ecosystem='pypi', origin='vscode')


@when("I test {ecosystem} dependencies file {manifest} for stack analysis from {origin} "
      "through 3scale gateway {user_key} user_key")
def scale_process_deps_file(context, ecosystem, manifest, origin, rate=1,
                            user_key="without"):
    """Test stack analyses of an ecosystem specific dependencies file from an integration point."""
    endpoint = threescale_preview_endpoint_url(context, 'stack-analyses')
    use_user_key = parse_token_clause(user_key)
    test_stack_analyses_with_deps_file(context, manifest, endpoint, use_user_key,
                                       rate, ecosystem.lower(), origin)


@when("I send Maven package manifest {manifest} to stack analysis through "
      "3scale gateway {user_key} user_key")
@when("I send Maven package manifest {manifest} to stack analysis {rate:d} times"
      " in a minute through 3scale gateway {user_key} user_key")
def maven_manifest_stack_analysis(context, manifest, version=3, user_key="without", rate=1):
    """Send the NPM package manifest file to the stack analyses."""
    endpoint = threescale_preview_endpoint_url(context, 'stack-analyses')
    use_user_key = parse_token_clause(user_key)
    send_manifest_to_stack_analyses(context, manifest, 'dependencies.txt',
                                    endpoint, use_user_key, rate, ecosystem='maven',
                                    origin='vscode')


def pause_between_stack_analysis_requests(sleep_amount, rate):
    """Perform a pause between two stack analysis requests."""
    if rate > 1:
        sleep_amount = 0  # to get rate limit exceeded we have to overload API calls
    time.sleep(sleep_amount)


@when("I call stack analysis {rate:d} times in a minute {user_key} user_key")
@when("I wait for stack analysis to finish {user_key} user_key")
def wait_for_stack_analysis_completion(context, user_key="without", rate=1):
    """Try to wait for the stack analysis to be finished.

    This step assumes that stack analysis has been started previously and
    thus that the job ID is known

    Current API implementation returns just three HTTP codes:
    200 OK : analysis is already finished
    202 Accepted: analysis is started or is in progress (or other state!)
    403 UNAUTHORIZED : missing or improper user_key
    """
    context.duration = None
    start_time = time.time()
    timeout = context.stack_analysis_timeout  # in seconds
    sleep_amount = 15  # we don't have to overload the API with too many calls
    use_user_key = parse_token_clause(user_key)

    id = context.response.json().get("id")
    context.stack_analysis_id = id
    url = urljoin(threescale_preview_endpoint_url(context, 'stack-analyses'), id)

    for _ in range((timeout // sleep_amount) + rate):
        if use_user_key:
            context.response = requests.get(
                url, params={'user_key': context.three_scale_preview_user_key})
        else:
            context.response = requests.get(url)
        status_code = context.response.status_code
        if status_code == 200:
            json_resp = context.response.json()
            if contains_alternate_node(json_resp) and rate <= 1:
                break
        # 429 (Rate Limit) code should be checked later
        elif status_code == 429:
            break
        # 403 code should be checked later
        elif status_code == 403:
            break
        elif status_code != 202:
            raise Exception('Bad HTTP status code {c}'.format(c=status_code))
        pause_between_stack_analysis_requests(sleep_amount, rate)
    else:
        raise Exception('Timeout waiting for the stack analysis results')
    end_time = time.time()
    context.duration = end_time - start_time


@then("I should get {response_txt} text response")
def check_rate_limit_response(context, response_txt):
    """Verify the response text."""
    assert response_txt == context.response.text


@when("I start component analyses {ecosystem}/{package}/{version} {user_key} user_key")
@when("I start component analyses {ecosystem}/{package}/{version} {rate:d} "
      "times in a minute {user_key} user_key")
def start_component_analysis(context, ecosystem, package, version, user_key, rate=1):
    """Analyse the given component."""
    use_user_key = parse_token_clause(user_key)
    perform_component_analysis(context, ecosystem, package, version, use_user_key, rate)


@when('I access {url:S} without valid values via 3scale gateway')
@when('I access {url:S} without valid values {rate:d} times in a minute via 3scale gateway')
def check_submit_feedback_3scale(context, url, rate=1):
    """Access the submit-feedback API using the HTTP POST method."""
    payload = {
        "stack_id": "1234-569586048",
        "recommendation_type": "companion",
        "package_name": "blah-blah",
        "feedback_type": True,
        "ecosystem": None
    }
    for _ in range(rate):
        _resp = requests.post(threescale_preview_endpoint_url(context, 'submit-feedback'),
                              params={'user_key': context.three_scale_preview_user_key},
                              data=payload)
        # break the loop if rate limit exceeded
        context.response = _resp
        if _resp.status_code == 429:
            break
