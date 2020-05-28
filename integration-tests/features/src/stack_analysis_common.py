"""Common functions used to test stack analysis API."""

from urllib.parse import urljoin


def get_json_data(context):
    """Retrieve JSON data."""
    json_data = context.response.json()
    assert json_data is not None, \
        "JSON response from the previous request does not exist"
    return json_data


def get_result_from_payload(json_resp):
    """Try to get result node from the payload."""
    assert json_resp is not None
    assert 'result' in json_resp
    # read the actual result
    return json_resp.get('result')


def contains_alternate_node(json_resp):
    """Check for the existence of alternate node in the stack analysis."""
    # read the actual result
    result = get_result_from_payload(json_resp)
    return bool(result) and isinstance(result, list) \
        and (result[0].get('recommendation', {}) or {}).get('alternate', None) is not None


def stack_analysis_endpoint(context, version):
    """Return endpoint for the stack analysis of selected version."""
    # Two available endpoints for stack analysis are /stack-analyses and /analyse
    # /analyse endpoint was developed to meet the performance norms at production
    endpoints = ["/api/v1/stack-analyses-v1",
                 "/api/v1/analyse",
                 "/api/v1/stack-analyses/"]

    if version < 1 or version > len(endpoints):
        raise Exception("Wrong version specified: {v}".format(v=version))

    endpoint = endpoints[version - 1]

    return urljoin(context.coreapi_url, endpoint)


def check_frequency_count_attribute(usage_outlier, package_name):
    """Check one frequency count attribute."""
    frequency_count_attribute = "frequency_count"
    assert frequency_count_attribute in usage_outlier, \
        "'%s' attribute is expected in the node, " \
        "found: %s attributes " % (frequency_count_attribute,
                                   ", ".join(usage_outlier.keys()))
    value = usage_outlier[frequency_count_attribute]
    assert value is not None, \
        "Value of '%s' attribute should be set, but it is null" % frequency_count_attribute
    try:
        v = int(value)
        # check if the value represents non-negative integer
        assert v >= 0, \
            "frequency_count must represent non-negative integer" \
            "found %f value instead" % (v)
    except ValueError:
        raise Exception("Invalid value {v} found in {a} attribute for the package {p}".
                        format(v=value, a=frequency_count_attribute, p=package_name))


def check_frequency_count(usage_outliers, package_name):
    """Check the frequency count attribute.

    Try to find frequency count value for given package and check that
    the value is within permitted range.
    """
    for usage_outlier in usage_outliers:
        if usage_outlier["package_name"] == package_name:
            check_frequency_count_attribute(usage_outlier, package_name)
            return
    raise Exception("Can not find usage outlier for the package {p}".format(p=package_name))


def get_components_with_cve(components):
    """Get all components with CVE record(s)."""
    result = []

    for component in components:
        assert "security" in component
        cve_items = component["security"]
        for cve_item in cve_items:
            if "CVE" in cve_item:
                result.append(component)

    return result
