"""Basic checks for the server API."""
from behave import then, when
from urllib.parse import urljoin

import requests
import time

from src.utils import split_comma_separated_list
from src.authorization_tokens import authorization
from src.attribute_checks import check_and_get_attribute, check_timestamp, check_hash_value
from src.schema_validator import validate_schema
from src.parsing import parse_token_clause


@when('I access {url:S}')
def access_url(context, url):
    """Access the service API using the HTTP GET method."""
    context.response = requests.get(context.coreapi_url + url)


@when('I access the {url:S} endpoint using the HTTP GET method')
@when('I call the {url:S} endpoint using the HTTP GET method')
def access_url_get_method(context, url):
    """Access the service API using the HTTP GET method."""
    context.response = requests.get(context.coreapi_url + url)


@when('I access the {url:S} endpoint using the HTTP PUT method')
@when('I call the {url:S} endpoint using the HTTP PUT method')
def access_url_put_method(context, url):
    """Access the service API using the HTTP PUT method."""
    context.response = requests.put(context.coreapi_url + url)


@when('I access the {url:S} endpoint using the HTTP POST method')
@when('I call the {url:S} endpoint using the HTTP POST method')
def access_url_post_method(context, url):
    """Access the service API using the HTTP POST method."""
    context.response = requests.post(context.coreapi_url + url)


@when('I access the {url:S} endpoint using the HTTP PATCH method')
@when('I call the {url:S} endpoint using the HTTP PATCH method')
def access_url_patch_method(context, url):
    """Access the service API using the HTTP PATCH method."""
    context.response = requests.patch(context.coreapi_url + url)


@when('I access the {url:S} endpoint using the HTTP DELETE method')
@when('I call the {url:S} endpoint using the HTTP DELETE method')
def access_url_delete_method(context, url):
    """Access the service API using the HTTP DELETE method."""
    context.response = requests.delete(context.coreapi_url + url)


@when('I access the {url:S} endpoint using the HTTP HEAD method')
@when('I call the {url:S} endpoint using the HTTP HEAD method')
def access_url_head_method(context, url):
    """Access the service API using the HTTP HEAD method."""
    context.response = requests.head(context.coreapi_url + url)


@when('I access the {url:S} {repeat_count:d} times with {delay:d} seconds delay')
def access_url_repeatedly(context, url, repeat_count, delay):
    """Access the service API using the HTTP GET method repeatedly."""
    context.api_call_results = []
    url = context.coreapi_url + url

    # repeatedly call REST API endpoint and collect HTTP status codes
    # into list assigned to the context
    for i in range(repeat_count):
        response = requests.get(url)
        context.api_call_results.append(response.status_code)
        time.sleep(delay)


@when('I access {url:S} with authorization token')
@when('I access the {url:S} endpoint using the HTTP GET method and authorization token')
def access_url_with_authorization_token(context, url):
    """Access the service API using the HTTP GET method."""
    context.response = requests.get(context.coreapi_url + url,
                                    headers=authorization(context))


@when('I access the {url:S} endpoint using the HTTP PUT method and authorization token')
@when('I call the {url:S} endpoint using the HTTP PUT method and authorization token')
def access_url_put_method_with_authorization(context, url):
    """Access the service API using the HTTP PUT method and authorization token."""
    context.response = requests.put(context.coreapi_url + url,
                                    headers=authorization(context))


@when('I access the {url:S} endpoint using the HTTP POST method and authorization token')
@when('I call the {url:S} endpoint using the HTTP POST method and authorization token')
def access_url_post_method_with_authorization(context, url):
    """Access the service API using the HTTP POST method and authorization token."""
    context.response = requests.post(context.coreapi_url + url,
                                     headers=authorization(context))


@when('I access the {url:S} endpoint using the HTTP PATCH method and authorization token')
@when('I call the {url:S} endpoint using the HTTP PATCH method and authorization token')
def access_url_patch_method_with_authorization(context, url):
    """Access the service API using the HTTP PATCH method and authorization token."""
    context.response = requests.patch(context.coreapi_url + url,
                                      headers=authorization(context))


@when('I access the {url:S} endpoint using the HTTP DELETE method and authorization token')
@when('I call the {url:S} endpoint using the HTTP DELETE method and authorization token')
def access_url_delete_method_with_authorization(context, url):
    """Access the service API using the HTTP DELETE method and authorization token."""
    context.response = requests.delete(context.coreapi_url + url,
                                       headers=authorization(context))


@when('I access the {url:S} endpoint using the HTTP HEAD method and authorization token')
@when('I call the {url:S} endpoint using the HTTP HEAD method and authorization token')
def access_url_head_method_with_authorization(context, url):
    """Access the service API using the HTTP HEAD method and authorization token."""
    context.response = requests.head(context.coreapi_url + url,
                                     headers=authorization(context))


@when('I access {url:S} without valid values')
def check_submit_feedback_without_valid_values(context, url):
    """Access the submit-feedback API using the HTTP POST method with invalid payload."""
    payload = {
        "stack_id": "1234-569586048",
        "recommendation_type": "companion",
        "package_name": "blah-blah",
        "feedback_type": True,
        "ecosystem": None
    }
    context.response = requests.post(context.coreapi_url + url,
                                     headers=authorization(context),
                                     data=payload)


@when('I access {url:S} without any payload')
def check_submit_feedback_without_any_payload(context, url):
    """Access the submit-feedback API using the HTTP POST method with no payload."""
    payload = None
    context.response = requests.post(context.coreapi_url + url,
                                     headers=authorization(context),
                                     data=payload)


@when('I access {url:S} with empty payload')
def check_submit_feedback_with_empty_payload(context, url):
    """Access the submit-feedback API using the HTTP POST method with empty payload."""
    payload = {}
    context.response = requests.post(context.coreapi_url + url,
                                     headers=authorization(context),
                                     data=payload)


@then('I should see {num:d} ecosystems')
def check_ecosystems(context, num):
    """Check if the API call returns correct number of ecosystems."""
    ecosystems = context.response.json()['items']
    assert len(ecosystems) == num
    for e in ecosystems:
        # assert that there is 'ecosystem' field in every ecosystem
        assert 'ecosystem' in e


def check_package_version(v, ecosystem, package, versions):
    """Check package version."""
    assert v['ecosystem'] == ecosystem
    assert v['package'] == package
    assert v['version'] in versions


@then('I should see {num:d} versions ({versions}), all for {ecosystem}/{package} package')
def check_versions(context, num=0, versions='', ecosystem='', package=''):
    """Check the versions for the selected ecosystems and package."""
    versions = split_comma_separated_list(versions)
    vrsns = context.response.json()['items']
    assert len(vrsns) == num
    for v in vrsns:
        check_package_version(v, ecosystem, package, versions)


@then('I should find the endpoint {endpoint} in the list of supported endpoints')
def check_endpoint_in_paths(context, endpoint):
    """Check the existence of given endpoint in the list of all supported endpoints."""
    data = context.response.json()
    paths = check_and_get_attribute(data, "paths")
    assert endpoint in paths, "Cannot find the expected endpoint {e}".format(
        e=endpoint)


@then('I should find the schema {schema} version {version} in the list of supported schemas')
def check_schema_existence(context, schema, version, selector=None):
    """Check the existence of given schema."""
    data = context.response.json()
    if selector is not None:
        api_schemas = check_and_get_attribute(data, selector)
        schema = check_and_get_attribute(api_schemas, schema)
    else:
        schema = check_and_get_attribute(data, schema)
    check_and_get_attribute(schema, version)


@then('I should find the schema {schema} version {version} in the list of supported schemas '
      'for API calls')
def check_schema_existence_api_call(context, schema, version):
    """Check the existence of given schema (API calls)."""
    check_schema_existence(context, schema, version, "api")


@then('I should find the schema {schema} version {version} in the list of component analyses '
      'schemas')
def check_schema_existence_component_analyses(context, schema, version):
    """Check the existence of given schema (component analyses)."""
    check_schema_existence(context, schema, version, "component_analyses")


@then('I should find the schema version {version} in the list of schema versions')
def check_schema_version(context, version):
    """Check the existence of schema version."""
    data = context.response.json()
    check_and_get_attribute(data, version)


@then('I should find valid schema in the server response')
def check_valid_schema(context):
    """Check if the schema is valid, validation is performed against metaschema."""
    data = context.response.json()
    validate_schema(data)


def generate_data_for_user_feedback(is_valid):
    """Generate data for generating user feedback."""
    if is_valid == "valid":
        return {"request_id": "test_id", "feedback": [{"ques": "what", "ans": "got it"}]}
    elif is_valid == "invalid":
        return {"foo": "x", "bar": "y", "baz": []}
    elif is_valid == "incomplete":
        return {"request_id": "test_id"}
    elif is_valid == "empty":
        return {}
    else:
        return None


@when("I post {is_valid} input to the {endpoint} endpoint {token} authorization token")
def post_input_to_user_feedback(context, is_valid, endpoint, token):
    """Send feedback to user feedback endpoint."""
    use_token = parse_token_clause(token)
    api_url = urljoin(context.coreapi_url, endpoint)
    data = generate_data_for_user_feedback(is_valid)
    if use_token:
        response = requests.post(api_url, json=data,
                                 headers=authorization(context))
    else:
        response = requests.post(api_url, json=data)
    context.response = response


@then("I should find the correct commit hash in the JSON response")
def check_hash_attribute(context):
    """Check the commit hash in the JSON response."""
    response = context.response
    assert response is not None
    data = response.json()
    commit_hash = check_and_get_attribute(data, "commit_hash")
    check_hash_value(commit_hash)


@then("I should find the correct committed at timestamp in the JSON response")
def check_timestamp_attribute(context):
    """Check the commited at timestamp in the JSON response."""
    response = context.response
    assert response is not None
    data = response.json()
    timestamp = check_and_get_attribute(data, "committed_at")
    # we are not interested much in +100 offsets etc.
    template = "2000-01-01 10:20:30"
    assert len(timestamp) >= len(template), "Invalid timestamp %s" % timestamp
    t = timestamp[0:len(template)]
    check_timestamp(t)
