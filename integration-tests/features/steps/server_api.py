"""Basic checks for the server API."""
from behave import given, then, when
import requests

from src.utils import *
from src.authorization_tokens import *
from src.attribute_checks import *
from src.schema_validator import *


@when('I access {url:S}')
def access_url(context, url):
    """Access the service API using the HTTP GET method."""
    context.response = requests.get(context.coreapi_url + url)


@when('I access {url:S} with authorization token')
def access_url_with_authorization_token(context, url):
    """Access the service API using the HTTP GET method."""
    context.response = requests.get(context.coreapi_url + url,
                                    headers=authorization(context))


@when('I access {url:S} without valid values')
def check_submit_feedback(context, url):
    payload = {
        "stack_id": "1234-569586048",
        "recommendation_type": "companion",
        "package_name": "blah-blah",
        "feedback_type": True,
        "ecosystem": None
    }
    context.response = requests.post(context.coreapi_url + url,
                                     data=payload)


@then('I should see {num:d} ecosystems')
def check_ecosystems(context, num):
    """Check if the API call returns correct number of ecosystems."""
    ecosystems = context.response.json()['items']
    assert len(ecosystems) == num
    for e in ecosystems:
        # assert that there is 'ecosystem' field in every ecosystem
        assert 'ecosystem' in e


@then('I should see {num:d} versions ({versions}), all for {ecosystem}/{package} package')
def check_versions(context, num=0, versions='', ecosystem='', package=''):
    """Check the versions for the selected ecosystems and package."""
    versions = split_comma_separated_list(versions)
    vrsns = context.response.json()['items']
    assert len(vrsns) == num
    for v in vrsns:
        assert v['ecosystem'] == ecosystem
        assert v['package'] == package
        assert v['version'] in versions


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
