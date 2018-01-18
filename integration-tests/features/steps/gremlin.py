"""Tests for Gremlin database."""
import os
import requests

from behave import given, then, when
from urllib.parse import urljoin
import time
from src.json_utils import *
from src.utils import split_comma_separated_list
from src.graph_db_query import Query

import logging

# set up the logging for this module
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# no data should have timestamp with earlier date than 2015-01-01, simply because
# this project was started after this date
BAYESSIAN_PROJECT_START_DATE = time.mktime(time.strptime("2015-01-01", "%Y-%m-%d"))


@when('I access Gremlin API')
def gremlin_url_access(context):
    """Access the Gremlin service API using the HTTP POST method."""
    post_query(context, "")


@when('I ask Gremlin to find all vertexes having property {name} set to {value}')
def gremlin_search_vertexes(context, name, value):
    """Perform simple query to the Gremlin for all vertexes having the specified property."""
    query = Query().has(name, value)
    post_query(context, query)


@when('I ask Gremlin to find number of vertexes for the ecosystem {ecosystem}')
def gremlin_search_vertexes_for_the_ecosystem(context, ecosystem):
    """Perform simple query to the Gremlin for all vertexes having the specified property."""
    query = Query().has("pecosystem", ecosystem).count()
    post_query(context, query)


@when('I ask Gremlin to find all versions of the package {package:S} in the ecosystem {ecosystem}')
def gremlin_find_package(context, package, ecosystem):
    """Try to find all versions of the given package in the selected ecosystem."""
    query = Query().has("ecosystem", ecosystem).has("name", package).out("has_version")
    post_query(context, query)


@when('I ask Gremlin to find the package {package:S} version {version} in the ecosystem '
      '{ecosystem}')
def gremlin_find_package_version(context, package, version, ecosystem):
    """Try to find the package with version in the selected ecosystem."""
    query = Query().has("pecosystem", ecosystem).has("pname", package).has("version", version)
    post_query(context, query)


@when('I ask Gremlin to find the package {package:S} in the ecosystem {ecosystem}')
def gremlin_find_package(context, package, ecosystem):
    """Try to find the package in the selected ecosystem."""
    query = Query().has("ecosystem", ecosystem).has("name", package)
    post_query(context, query)


@when('I remember the current time')
def remember_current_time(context):
    """Remember the current time for further checks."""
    context.current_time = time.time()


@when('I read the last update time for the package {package:S} version {version} in the ecosystem'
      ' {ecosystem}')
def gremlin_read_last_update_time(context, package, version, ecosystem):
    """Read the last update timestamp."""
    query = Query().has("pecosystem", ecosystem).has("pname", package).has("version", version).\
        first().value("last_updated")
    post_query(context, query)


@when('I wait for the update in the graph database for the package {package:S} version {version}'
      ' in the ecosystem {ecosystem}')
def wait_for_update_in_graph_db(context, package, version, ecosystem):
    """Wait until the package metadata is not updated in the graph database."""
    timeout = 300 * 60
    sleep_amount = 10  # we don't want to overload the graph db, so 10 seconds seems to be good
    max_iters = timeout // sleep_amount

    start_time = time.time()
    log.info("start time: " + str(start_time))

    for i in range(max_iters):
        gremlin_read_last_update_time(context, package, version, ecosystem)
        timestamp = get_timestamp_from_gremlin(context)
        log.info("Iteration {i} of {max}: start time: {t1}, timestamp: {t2}".format(i=i,
                                                                                    max=max_iters,
                                                                                    t1=start_time,
                                                                                    t2=timestamp))
        if timestamp > start_time:
            return
        time.sleep(sleep_amount)
    raise Exception('Timeout waiting for the new package metadata in graph DB!')


def post_query(context, query):
    """Post the already constructed query to the Gremlin."""
    data = {"gremlin": str(query)}
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
def check_vertexes_count(context, num=0):
    """Check the number of vertexes returned in Gremlin response."""
    data, meta = get_results_from_gremlin(context)
    vertexes = len(data)
    assert vertexes == num, "Expected %d vertexes, but got %d instead" % (num, vertexes)


@then('I should find at least one such vertex')
def check_vertexes_cound(context):
    """Check the number of vertexes returned in Gremlin response."""
    data, meta = get_results_from_gremlin(context)
    vertexes = len(data)
    assert vertexes > 0, "Expected at least one vertex, but got zero instead"


def get_node_value_from_properties_returned_by_gremlin(context, node_name):
    """Try to retrieve node value from the 'properties' node returned by Gremlin."""
    data, meta = get_results_from_gremlin(context)
    assert len(data) == 1, "Expected preciselly one vertex with package data"
    assert data[0] is not None
    properties = check_and_get_attribute(data[0], "properties")
    node = check_and_get_attribute(properties, node_name)
    assert node[0] is not None
    return check_and_get_attribute(node[0], "value")


@then('I should find at least one package in the Gremlin response')
@then('I should find at least {expected:d} packages in the Gremlin response')
def check_number_of_packages_returned(context, expected=1):
    """Check the number of returned packages."""
    data, meta = get_results_from_gremlin(context)
    found = len(data)

    assert found >= expected, \
        "Expected at least %d packages, but %d was found instead" % (expected, found)


@then('I should find that all found packages have valid timestamp with the last update time')
def check_timestamp_for_all_packages_in_gremlin_response(context):
    """Check if the last_updated attribute exists and if it contain proper timestamp."""
    now = time.time()
    data, meta = get_results_from_gremlin(context)

    for package in data:
        properties = check_and_get_attribute(package, "properties")
        last_updated = check_and_get_attribute(properties, "last_updated")
        value = check_and_get_attribute(last_updated[0], "value")
        assert value >= BAYESSIAN_PROJECT_START_DATE
        assert value <= now


@then('I should find that the package data is {comparison} than remembered time')
def package_data_timestamp_comparison_with_remembered_time(context, comparison):
    """Check if the last_updated attribute is older or newer than remembered time.

    The timestamp is checked for all package versions.
    """
    remembered_time = context.current_time
    data, meta = get_results_from_gremlin(context)

    for package in data:
        properties = check_and_get_attribute(package, "properties")
        last_updated = check_and_get_attribute(properties, "last_updated")
        value = check_and_get_attribute(last_updated[0], "value")
        if comparison == "older":
            assert value < remembered_time
        elif comparison == "newer":
            assert value > remembered_time


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

    # this node should be empty
    assert not attributes


def check_gremlin_result_node(data):
    """Check the basic structure of the 'result' node in Gremlin response."""
    result = check_and_get_attribute(data, "result")
    data = check_and_get_attribute(result, "data")
    meta = check_and_get_attribute(result, "meta")

    assert type(data) is list
    assert type(meta) is dict


@then('I should find the following properties ({properties}) in all found packages')
def check_properties_in_results(context, properties):
    """Check if all given properties can be found in all packages returned by Gremlin."""
    data, meta = get_results_from_gremlin(context)

    expected_properties = split_comma_separated_list(properties)

    # we need to check if all expected properties are really returned by the Gremlin
    for package in data:
        check_attribute_presence(package, "properties")
        properties = package["properties"].keys()

        assert properties is not None

        for expected_property in expected_properties:
            if expected_property not in properties:
                raise Exception("Required property could not be found: {prop}".format(
                                prop=expected_property))


@then('I should not find any property apart from ({properties}) in all found packages')
def check_unexpected_properties_in_results(context, properties):
    """Check if only given optional properties can be found in all packages returned by Gremlin."""
    data, meta = get_results_from_gremlin(context)

    expected_properties = split_comma_separated_list(properties)

    for package in data:
        check_attribute_presence(package, "properties")
        properties = package["properties"].keys()

        assert properties is not None

        for prop in properties:
            # check that the property is contained in a list of expected properties
            if prop not in expected_properties:
                raise Exception("Unexpected property has been found: {prop}".format(
                                prop=prop))


def get_timestamp_from_gremlin(context):
    """Get the value of timestamp attribute."""
    data, meta = get_results_from_gremlin(context)
    assert len(data) == 1
    return data[0]


@then('I should get a valid timestamp represented as UNIX time')
def check_unix_timestamp(context):
    """Check that only proper timestamp is returned in Gremlin response."""
    timestamp = get_timestamp_from_gremlin(context)
    assert type(timestamp) is float


@then('I should find that the returned timestamp is {comparison} than remembered time')
def check_package_version_timestamp_comparison_with_remembered_time(context, comparison):
    """Check if the last_updated attribute is older or newer than remembered time."""
    remembered_time = context.current_time
    timestamp = get_timestamp_from_gremlin(context)
    if comparison == "older":
        assert timestamp < remembered_time
    elif comparison == "newer":
        assert timestamp > remembered_time


def read_property_value_from_gremlin_response(context, property_name):
    """Read property value from the Gremlin response with all checks."""
    data, meta = get_results_from_gremlin(context)
    package = data[0]
    properties = check_and_get_attribute(package, "properties")

    # try to retrieve list of id+value pairs
    id_values = check_and_get_attribute(properties, property_name)

    # we expect list with one value only
    assert type(id_values) is list and len(id_values) == 1
    id_value = id_values[0]

    # check the content of 'value' attribute
    return check_and_get_attribute(id_value, "value")


@then('I should find that the {property_name} property is set to {expected_value} in the package '
      'properties')
def check_property_value(context, property_name, expected_value):
    """Check if the property is set to expected value for the first package returned by Gremlin."""
    value = read_property_value_from_gremlin_response(context, property_name)

    assert value == expected_value, ("The property {p} value is set to '{value}', not to "
                                     "'{expected_value}").format(p=property_name, value=value,
                                                                 expected_value=expected_value)


@then('I should find that the {property_name} property has numeric value greater than or equal '
      'to {expected:d}')
def check_numeric_property_value(context, property_name, expected):
    """Check if the property has assigned numeric value that is greater than or equal to X."""
    value = read_property_value_from_gremlin_response(context, property_name)

    numeric = convert_to_number(value)
    assert numeric >= expected, ("The property {p} value is set to '{value}', but it should be "
                                 "greater than or equal to {expected").format(p=property_name,
                                                                              value=value,
                                                                              expected=expected)


def convert_to_number(value):
    """Convert the value, that can be string, int, or float, to number."""
    if isinstance(value, (int, float)):
        return value

    scale = get_scale(value)
    if scale is not None:
        return float(value[:-1]) * scale
    else:
        return float(value)


def get_scale(value):
    """Get the scale for a numeric value stored as a string.

    The scale is used for store libio attributes, dunno why.
    """
    scales = {
        "k": 1000,
        "m": 1000000}
    return scales.get(value[-1].lower())
