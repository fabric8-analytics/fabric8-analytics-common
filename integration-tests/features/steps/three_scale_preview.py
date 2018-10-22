"""Tests for stack-analyses, component-analyses, submit-feedback API via 3scale."""
import requests
import os
import time

from behave import when, then, given
from urllib.parse import urljoin
from src.parsing import parse_token_clause


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


def send_manifest_to_stack_analyses(context, manifest, name, endpoint, user_key, rate):
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
                                    'user_key': context.three_scale_preview_user_key})
            # break the loop if rate limit exceeded
            if response.status_code == 429:
                break
    else:
        response = requests.post(endpoint, files=files)
    context.response = response


def contains_alternate_node(json_resp):
    """Check for the existence of alternate node in the stack analysis."""
    result = json_resp.get('result')
    return bool(result) and isinstance(result, list) \
        and (result[0].get('recommendation', {}) or {}).get('alternate', None) is not None


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
    send_manifest_to_stack_analyses(context, manifest, 'package.json',
                                    endpoint, use_user_key, rate)


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
    timeout = context.stack_analysis_timeout  # in seconds
    sleep_amount = 15  # we don't have to overload the API with too many calls
    use_user_key = parse_token_clause(user_key)

    id = context.response.json().get("id")
    context.stack_analysis_id = id
    url = urljoin(threescale_preview_endpoint_url(context, 'stack-analyses'), id)

    for _ in range((timeout // sleep_amount) + rate):
        if rate > 1:
            sleep_amount = 0  # to get rate limit exceeded we have to overload API calls
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
        time.sleep(sleep_amount)
    else:
        raise Exception('Timeout waiting for the stack analysis results')


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
