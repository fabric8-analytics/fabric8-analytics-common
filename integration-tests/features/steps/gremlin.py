"""Tests for Gremlin database."""
import os
import requests

from behave import given, then, when
from urllib.parse import urljoin
from src.json_utils import *


@when('I access Gremlin API')
def gremlin_url_access(context):
    """Access the Gremlin service API using the HTTP POST method."""
    post_query(context, "")


@when('I ask Gremlin to find all vertexes having property {name} set to {value}')
def gremlin_search_vertexes(context, name, value):
    """Perform simple query to the Gremlin for all vertexes having the specified property."""
    query = 'g.V().has("{name}", "{value}")'.format(name=name, value=value)
    post_query(context, query)


@when('I ask Gremlin to find number of vertexes for the ecosystem {ecosystem}')
def gremlin_search_vertexes_for_the_ecosystem(context, ecosystem):
    """Perform simple query to the Gremlin for all vertexes having the specified property."""
    query = 'g.V().has("pecosystem", "{ecosystem}").count()'.format(ecosystem=ecosystem)
    post_query(context, query)


def post_query(context, query):
    """Post the already constructed query to the Gremlin."""
    data = {"gremlin": query}
    context.response = requests.post(context.gremlin_url, json=data)


@then('I should get valid Gremlin response')
def valid_gremlin_response(context):
    """Check that the Gremlin response is valid."""
    check_request_id_value_in_json_response(context, "requestId")

    data = context.response.json()
    assert data, "Gremlin does not send a proper response"

    check_gremlin_status_node(data)
    check_gremlin_result_node(data)


@then('I should get zero vertexes')
@then('I should get {num:d} vertexes')
def check_vertexes_cound(context, num=0):
    """Check the number of vertexes returned in Gremlin response."""
    data, meta = get_results_from_gremlin(context)
    vertexes = len(data)
    assert vertexes == num, "Expected %d vertexes, but got %d instead" % (num, vertexes)


@then('I should find at least one such vertex')
def check_vertexes_cound(context):
    """Check the number of vertexes returned in Gremlin response."""
    data, meta = get_results_from_gremlin(context)
    vertexes = len(data)
    assert vertexes > 0, "Expected at least one vertex, but got zero instead" % vertexes


def get_results_from_gremlin(context):
    """Try to take the results from the Gremlin response."""
    data = context.response.json()
    result = check_and_get_attribute(data, "result")
    data = check_and_get_attribute(result, "data")
    meta = check_and_get_attribute(result, "meta")
    return data, meta


def check_gremlin_status_node(data):
    """Check the basic structure of the 'status' node in Gremlin response."""
    status = check_and_get_attribute(data, "status")
    message = check_and_get_attribute(status, "message")
    code = check_and_get_attribute(status, "code")
    attributes = check_and_get_attribute(status, "attributes")

    assert message == ""
    assert code == 200


def check_gremlin_result_node(data):
    """Check the basic structure of the 'result' node in Gremlin response."""
    result = check_and_get_attribute(data, "result")
    data = check_and_get_attribute(result, "data")
    meta = check_and_get_attribute(result, "meta")

    assert type(data) is list
    assert type(meta) is dict
