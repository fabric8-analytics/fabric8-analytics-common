"""Tests for Gremlin database."""
import requests
import pprint

from behave import then, when
from semantic_version import Version
import time
from src.attribute_checks import check_and_get_attribute, check_attribute_presence, check_cve_value
from src.json_utils import check_request_id_value_in_json_response
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
def gremlin_find_all_versions_of_package(context, package, ecosystem):
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
def check_non_zero_vertexes_count(context):
    """Check the number of vertexes returned in Gremlin response."""
    data, meta = get_results_from_gremlin(context)
    vertexes = len(data)
    assert vertexes > 0, "Expected at least one vertex, but got zero instead"


def get_node_value_from_properties_returned_by_gremlin(context, node_name):
    """Try to retrieve node value from the 'properties' node returned by Gremlin."""
    data, meta = get_results_from_gremlin(context)
    assert len(data) == 1, "Expected precisely one vertex with package data"
    assert data[0] is not None
    properties = check_and_get_attribute(data[0], "properties")
    return get_node_value(properties, node_name)


@then('I should find the package {package} name in the Gremlin response')
def check_package_name(context, package):
    """Check the package name in Gremlin response."""
    name = get_node_value_from_properties_returned_by_gremlin(context, "name")
    assert name == package, \
        "Returned package name '{name}' is different from expected name '{package}'" \
        .format(name=name, package=package)


@then('I should find the ecosystem {ecosystem} name in the Gremlin response')
def check_ecosystem_name(context, ecosystem):
    """Check the ecosystem name in Gremlin response."""
    name = get_node_value_from_properties_returned_by_gremlin(context, "ecosystem")
    assert name == ecosystem, \
        "Returned ecosystem name '{name}' is different from expected name '{ecosystem}'" \
        .format(name=name, ecosystem=ecosystem)


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
    data, meta = get_results_from_gremlin(context)

    for package in data:
        properties = check_and_get_attribute(package, "properties")
        test_last_updated_attribute(properties)


def check_last_updated_value(comparison, value, remembered_time):
    """Check the 'last_update' attribute for data item stored in Gremlin."""
    if comparison == "older":
        assert value < remembered_time, "The last_updated attribute is less than current time"
    elif comparison == "newer":
        assert value > remembered_time, "The last_updated attribute is higher than current time"
    else:
        raise Exception("Wrong 'comparison' argument in test step {}".format(comparison))


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
        check_last_updated_value(comparison, value, remembered_time)


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
                # print examined data so users would know what happened
                formatted_data = pprint.pformat(package)
                message = "Required property could not be found: {prop}\n" \
                          "Tested Gremlin results:\n{r}"
                raise Exception(message.format(prop=expected_property, r=formatted_data))


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


@then('I should find that the {property_name} property is higher than or equal to '
      '{expected_value} in the package properties')
def check_latest_version_property_value(context, property_name, expected_value):
    """Check if the latest_version property contains expected value."""
    value = read_property_value_from_gremlin_response(context, property_name)
    try:
        assert Version.coerce(value) >= Version(expected_value)
    except Exception:
        data, meta = get_results_from_gremlin(context)
        print("Metadata returned by Gremlin:")
        pprint.pprint(meta)
        print("Data returned by Gremlin:")
        pprint.pprint(data)
        raise


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


@then('I should find that all information about package have correct structure')
def check_package_structure(context):
    """Check all items with package metadata returned by Gremlin."""
    data, meta = get_results_from_gremlin(context)
    assert len(data) == 1, "Exactly one vertex expected, but {n} has been found".format(n=len(data))

    # now we know we have exactly one vertex, so let's check its content
    item = data[0]

    labelValue = check_and_get_attribute(item, "label")
    assert labelValue == "vertex" or labelValue == "Package"

    properties = check_and_get_attribute(item, "properties")
    test_last_updated_attribute(properties)
    test_vertex_label(properties, "Package")
    test_github_related_properties(properties, False)
    test_libio_related_properties(properties, False)


@then('I should find that all information about package versions have correct structure')
def check_package_versions_structure(context):
    """Check all items with package version metadata returned by Gremlin."""
    data, meta = get_results_from_gremlin(context)
    assert len(data) > 0, "At least one vertex expected, but 0 has been found"

    # check all n items found in data
    for item in data:
        labelValue = check_and_get_attribute(item, "label")
        assert labelValue is not None
        # the following check is blocked by: 1934
        # assert labelValue == "vertex" or labelValue == "Version"
        properties = check_and_get_attribute(item, "properties")
        test_last_updated_attribute(properties)
        test_cm_loc(properties)
        test_cm_num_files(properties)
        test_cm_avg_cyclomatic_complexity(properties)
        test_cve_ids(properties)


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


def test_last_updated_attribute(properties):
    """Check that the 'last_updated' attribute contains proper timestamp."""
    now = time.time()
    last_updated = check_and_get_attribute(properties, "last_updated")
    value = check_and_get_attribute(last_updated[0], "value")
    assert value >= BAYESSIAN_PROJECT_START_DATE
    assert value <= now


def get_node_value(properties, property_name):
    """Retrieve the value of node taken from properties returned by Gremlin.

    Please note, that each property is an array of id+value pairs and in
    this case we are interested only in the first pair.
    """
    node = check_and_get_attribute(properties, property_name)
    assert node[0] is not None
    return check_and_get_attribute(node[0], "value")


def check_integer_property_value(properties, property_name, additional_check=None):
    """Check if the node value is valid integer."""
    value = get_node_value(properties, property_name)
    assert type(value) is int

    # additional_check might be lambda expression
    if additional_check is not None:
        assert additional_check(value),\
            "Additional check has failed for the integer value {v}".format(v=value)


def check_libio_number_property_value(properties, property_name, additional_check=None):
    """Check the 'numeric' value used in libraries.io properties.

    Such values are stored as string with format like:
    100
    92.9K
    10M

    Please see https://github.com/openshiftio/openshift.io/issues/2023 for further info.
    """
    value = get_node_value(properties, "libio_dependents_projects")
    value = convert_to_number(value)
    # additional_check might be lambda expression
    if additional_check is not None:
        assert additional_check(value),\
            "Additional check has failed for the numeric value {v}".format(v=value)


def check_float_property_value(properties, property_name, additional_check=None):
    """Check if the node value is valid float."""
    value = get_node_value(properties, property_name)
    assert type(value) is float

    # additional_check might be lambda expression
    if additional_check is not None:
        assert additional_check(value),\
            "Additional check has failed for the floating point value {v}".format(v=value)


def check_string_property_value(properties, property_name, expected_value):
    """Check if the node value is a string with expected value."""
    value = get_node_value(properties, property_name)
    assert value == expected_value, "Property '{p}' should have the value '{e}', " + \
        "but the value '{v}' was found instead.".format(p=property_name, e=expected_value, v=value)


def test_cm_loc(properties, expected_property=False):
    """Check the property 'cm_loc'."""
    if expected_property or "cm_loc" in properties:
        check_integer_property_value(properties, "cm_loc")


def test_cm_avg_cyclomatic_complexity(properties, expected_property=False):
    """Check the property 'cm_avg_cyclomatic_complexity'."""
    if expected_property or "cm_avg_cyclomatic_complexity" in properties:
        check_float_property_value(properties, "cm_avg_cyclomatic_complexity")


def test_cm_num_files(properties, expected_property=False):
    """Check the property 'cm_num_files'."""
    if expected_property or "cm_num_files" in properties:
        check_integer_property_value(properties, "cm_num_files")


def perform_libio_property_check(expected_properties, properties, property_name):
    """Return true if the selected Libio property should be checked."""
    return expected_properties or property_name in properties


def test_libio_related_properties(properties, expected_properties=False):
    """Check all properties related to Libraries.io."""
    if perform_libio_property_check(expected_properties, properties, "libio_latest_release"):
        check_float_property_value(properties, "libio_latest_release", lambda v: v >= 0.0)

    numeric_property_names = [
        "libio_dependents_projects",
        "libio_dependents_repos",
        "libio_total_releases"
    ]
    for numeric_property_name in numeric_property_names:
        if perform_libio_property_check(expected_properties, properties, numeric_property_name):
            check_libio_number_property_value(properties, "libio_dependents_projects",
                                              lambda v: v >= -1)


def test_github_related_properties(properties, expected_properties=False):
    """Check all properties related to GitHub."""
    integer_property_names = [
        "gh_contributors_count",
        "gh_forks",
        "gh_open_issues_count",
        "gh_issues_last_month_closed",
        "gh_issues_last_year_closed",
        "gh_prs_last_month_closed",
        "gh_prs_last_month_opened",
        "gh_prs_last_year_closed",
        "gh_prs_last_year_opened",
        "gh_stargazers",
        "gh_subscribers_count"
    ]
    for integer_property_name in integer_property_names:
        if expected_properties or integer_property_name in properties:
            check_integer_property_value(properties, integer_property_name, lambda cnt: cnt >= -1)


def test_vertex_label(properties, expected_value):
    """Check the property 'vertex_label'."""
    value = get_node_value(properties, "vertex_label")
    assert value is not None
    check_string_property_value(properties, "vertex_label", expected_value)


def test_cve_ids(properties, expected_property=False):
    """Check all CVE entries found for the package.

    The format for CVE is: CVE ID:score.
    """
    if expected_property or "cve_ids" in properties:
        cve_ids = check_and_get_attribute(properties, "cve_ids")
        for cve_id in cve_ids:
            cve = cve_id["value"]
            check_cve_value(cve, True)
