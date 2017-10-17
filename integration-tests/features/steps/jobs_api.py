"""Tests for jobs API endpoints."""
import requests

from behave import given, then, when
from urllib.parse import urljoin

from src.parsing import *
from src.utils import *
from src.authorization_tokens import *


@when('I read list of jobs')
@when('I read list of jobs with type {type}')
@when('I read list of jobs {token} authorization token')
@when('I read list of jobs with type {type} {token} authorization token')
def list_of_jobs(context, type=None, token=None):
    """Read list of jobs via job API."""
    endpoint = job_endpoint(context)
    if type is not None:
        endpoint += "?job_type=" + type
    use_token = parse_token_clause(token)
    if use_token:
        context.response = requests.get(endpoint, headers=jobs_api_authorization(context))
    else:
        context.response = requests.get(endpoint)


@then('I should see proper analyses report')
def check_job_debug_analyses_report(context):
    """Check the analyses report returned by job API."""
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


def flow_sheduling_endpoint(context, state, job_id=None):
    """Return URL to flow-scheduling with the given state and job ID."""
    if job_id:
        return "{jobs_api_url}api/v1/jobs/flow-scheduling?state={state}&job_id={job_id}".\
               format(jobs_api_url=context.jobs_api_url, state=state, job_id=job_id)
    else:
        return "{jobs_api_url}api/v1/jobs/flow-scheduling?state={state}".\
               format(jobs_api_url=context.jobs_api_url, state=state)


def job_metadata_filename(metadata):
    """Construct relative filename to job metadata."""
    return "data/{metadata}".format(metadata=metadata)


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
    """API call to create a new job using the provided metadata.

    The token parameter can be set to 'with', 'without', or 'using'.
    """
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


