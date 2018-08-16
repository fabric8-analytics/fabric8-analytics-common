"""Tests for API endpoints that performs stack analysis."""
import requests
import time
import os

from behave import then, when
from urllib.parse import urljoin
import jsonschema

from src.attribute_checks import *
from src.parsing import *
from src.utils import *
from src.json_utils import *
from src.authorization_tokens import *


STACK_ANALYSIS_CONSTANT_FILE_URL = "https://raw.githubusercontent.com/" \
    "fabric8-analytics/fabric8-analytics-stack-analysis/master/" \
    "analytics_platform/kronos/pgm/src/pgm_constants.py"

STACK_ANALYSIS_OUTLIER_PROBABILITY_CONSTANT_NAME = \
    "KRONOS_OUTLIER_PROBABILITY_THRESHOLD_VALUE"


def contains_alternate_node(json_resp):
    """Check for the existence of alternate node in the stack analysis."""
    result = json_resp.get('result')
    return bool(result) and isinstance(result, list) \
        and (result[0].get('recommendation', {}) or {}).get('alternate', None) is not None


@when("I wait for stack analysis to finish")
@when("I wait for stack analysis to finish {token} authorization token")
@when("I wait for stack analysis version {version:d} to finish {token} authorization token")
def wait_for_stack_analysis_completion(context, version=3, token="without"):
    """Try to wait for the stack analysis to be finished.

    This step assumes that stack analysis has been started previously and
    thus that the job ID is known

    Current API implementation returns just three HTTP codes:
    200 OK : analysis is already finished
    202 Accepted: analysis is started or is in progress (or other state!)
    401 UNAUTHORIZED : missing or improper authorization token
    """
    timeout = context.stack_analysis_timeout  # in seconds
    sleep_amount = 10  # we don't have to overload the API with too many calls
    use_token = parse_token_clause(token)

    id = context.response.json().get("id")
    context.stack_analysis_id = id
    # log.info("REQUEST ID: {}\n\n".format(context.stack_analysis_id))
    url = urljoin(stack_analysis_endpoint(context, version), id)
    # log.info("RECOMMENDER API URL: {}\n\n".format(url))

    for _ in range(timeout // sleep_amount):
        if use_token:
            context.response = requests.get(url, headers=authorization(context))
        else:
            context.response = requests.get(url)
        status_code = context.response.status_code
        # log.info("%r" % context.response.json())
        if status_code == 200:
            json_resp = context.response.json()
            if contains_alternate_node(json_resp):
                # log.info('Recommendation found')
                break
        # 401 code should be checked later
        elif status_code == 401:
            break
        elif status_code != 202:
            raise Exception('Bad HTTP status code {c}'.format(c=status_code))
        time.sleep(sleep_amount)
    else:
        raise Exception('Timeout waiting for the stack analysis results')


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

    # please note that the trick with (None, path_to_manifest_file) has to be
    # used here so the REST API call would work properly. It is similar to use
    # curl -F 'manifest[]=@filename' -F 'filePath[]=PATH_TO_FILE'
    files = {'manifest[]': (name, open(filename, 'rb')),
             'filePath[]': (None, path_to_manifest_file)}
    if use_token:
        response = requests.post(endpoint, files=files,
                                 headers=authorization(context))
    else:
        response = requests.post(endpoint, files=files)
    context.response = response


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


@when("I send NPM package manifest {manifest} to stack analysis")
@when("I send NPM package manifest {manifest} to stack analysis {token} authorization token")
@when("I send NPM package manifest {manifest} to stack analysis version {version:d}")
@when("I send NPM package manifest {manifest} to stack analysis version {version:d} {token} "
      "authorization token")
def npm_manifest_stack_analysis(context, manifest, version=3, token="without"):
    """Send the NPM package manifest file to the stack analysis."""
    endpoint = stack_analysis_endpoint(context, version)
    use_token = parse_token_clause(token)
    send_manifest_to_stack_analysis(context, manifest, 'package.json',
                                    endpoint, use_token)


@when("I send Python package manifest {manifest} to stack analysis")
@when("I send Python package manifest {manifest} to stack analysis {token} authorization token")
@when("I send Python package manifest {manifest} to stack analysis version {version:d}")
@when("I send Python package manifest {manifest} to stack analysis version {version:d} {token} "
      "authorization token")
def python_manifest_stack_analysis(context, manifest, version=3, token="without"):
    """Send the Python package manifest file to the stack analysis."""
    endpoint = stack_analysis_endpoint(context, version)
    use_token = parse_token_clause(token)
    send_manifest_to_stack_analysis(context, manifest, 'requirements.txt',
                                    endpoint, use_token)


@when("I send Maven package manifest {manifest} to stack analysis")
@when("I send Maven package manifest {manifest} to stack analysis {token} authorization token")
@when("I send Maven package manifest {manifest} to stack analysis version {version:d}")
@when("I send Maven package manifest {manifest} to stack analysis version {version:d} {token} "
      "authorization token")
def maven_manifest_stack_analysis(context, manifest, version=3, token="without"):
    """Send the Maven package manifest file to the stack analysis."""
    endpoint = stack_analysis_endpoint(context, version)
    use_token = parse_token_clause(token)
    send_manifest_to_stack_analysis(context, manifest, 'pom.xml',
                                    endpoint, use_token)


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
        # Allowing enough retries for stack analyses to complete
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
        err = "Stack analyses could not be completed within {t} seconds".format(
            t=iter * retry_interval)

    resp_json = get_resp.json()

    # ensure that the stack analyses result has been asserted in the loop
    assert resp_json.get("status") == "success", err

    # ensure that the response is in accordance to the Stack Analyses schema
    schema = requests.get(resp_json["schema"]["url"]).json()
    jsonschema.validate(resp_json, schema)


def check_frequency_count(usage_outliers, package_name):
    """Check the frequency count attribute.

    Try to find frequency count value for given package and check that
    the value is within permitted range.
    """
    frequency_count_attribute = "frequency_count"

    for usage_outlier in usage_outliers:
        if usage_outlier["package_name"] == package_name:
            assert frequency_count_attribute in usage_outlier, \
                "'%s' attribute is expected in the node, " \
                "found: %s attributes " % (frequency_count_attribute,
                                           ", ".join(usage_outlier.keys()))
            value = usage_outlier[frequency_count_attribute]
            assert value is not None
            v = float(probability)
            assert v >= 0, \
                "frequency_count value should be greater than or equal to zero, "\
                "found %f value instead" % (v)
            return
    raise Exception("Can not find usage outlier for the package {p}".format(p=package_name))


@then('I should find the proper outlier record for the {component} component')
def stack_analysis_check_outliers(context, component):
    """Check the outlier record in the stack analysis."""
    json_data = context.response.json()
    # log.info('Usage outlier threshold: %r' % threshold)
    path = "result/0/recommendation/usage_outliers"
    usage_outliers = get_value_using_path(json_data, path)
    check_frequency_count(usage_outliers, component)


@then('I should find that total {count} outliers are reported')
def check_outlier_count(context, count=2):
    """Check the number of outliers in the stack analysis."""
    json_data = context.response.json()
    path = "result/0/recommendation/usage_outliers"
    usage_outliers = get_value_using_path(json_data, path)
    assert len(usage_outliers) == int(count)


@then('I should find that valid outliers are reported')
def check_outlier_validity(context):
    """Check the outlier validity in the stack analysis."""
    json_data = context.response.json()
    threshold = 0.9
    path = "result/0/recommendation/usage_outliers"
    usage_outliers = get_value_using_path(json_data, path)
    for usage_outlier in usage_outliers:
        # log.info("PACKAGE: {}".format(usage_outlier["package_name"]))
        check_outlier_probability(usage_outliers, usage_outlier["package_name"], threshold)


@then('I should find that greater than {min_count} companions are reported')
def check_companion_count(context, min_count=0):
    """Check that we have more than min_count companions."""
    json_data = context.response.json()
    path = "result/0/recommendation/companion"
    companions = get_value_using_path(json_data, path)
    assert len(companions) > int(min_count)


def check_licenses(licenses, expected_licenses):
    """Compare list of read licenses with list of expected licenses.

    Check that all expected licenses and only such licenses can be found in the list of licenses.
    """
    assert licenses is not None
    for license in licenses:
        if license not in expected_licenses:
            raise Exception("Unexpected license found: {license}".format(
                            license=license))
    for expected_license in expected_licenses:
        if expected_license not in licenses:
            raise Exception("Required license could not be found: {license}".format(
                            license=expected_license))


@then('I should find the following licenses ({licenses}) under the path {path}')
def stack_analysis_check_licenses(context, licenses, path):
    """Check the license(s) in the stack analysis."""
    licenses = split_comma_separated_list(licenses)
    json_data = context.response.json()
    node = get_value_using_path(json_data, path)
    assert node is not None
    check_licenses(node, licenses)


def get_attribute_values(list, attribute_name):
    """Return attribute values as a sequence."""
    return [item[attribute_name] for item in list]


def get_analyzed_packages(json_data):
    """Get names of all analyzed packages."""
    path = "result/0/user_stack_info/dependencies"
    analyzed_packages = get_value_using_path(json_data, path)
    return get_attribute_values(analyzed_packages, "package")


def get_companion_packages(json_data):
    """Get names of all packages in companion list."""
    path = "result/0/recommendation/companion"
    companion = get_value_using_path(json_data, path)
    return get_attribute_values(companion, "name")


@then('I should find that none analyzed package can be found in companion packages as well')
def stack_analysis_check_companion_packages(context):
    """Check that the analyze packages and companion packages has no common item(s)."""
    json_data = context.response.json()

    # those two lists should have no element in common
    analyzed_packages = get_analyzed_packages(json_data)
    companion_packages = get_companion_packages(json_data)

    for companion_package in companion_packages:
        assert companion_package not in analyzed_packages, \
            "The analyzed package '%s' is found in companion packages as well" \
            % companion_package


@then('I should get {field_name} field in stack report')
def verify_stack_level_field_presence(context, field_name):
    """Check that the given field can be found in the stack report."""
    json_data = context.response.json()
    path = 'result/0/user_stack_info'
    user_stack_info = get_value_using_path(json_data, path)
    assert user_stack_info.get(field_name, None) is not None


@then('I should find {field_name} field in recommendation')
def verify_stack_level_field_presence(context, field_name):
    """Check that the given field can be found in the recommendation."""
    json_data = context.response.json()
    path = 'result/0/recommendation'
    recommendation = get_value_using_path(json_data, path)
    assert recommendation.get(field_name, None) is not None


def replaces_component(replacement, component, version):
    """Check the component replacement info in the stack analysis."""
    assert "replaces" in replacement
    replaces = replacement["replaces"]
    for replace in replaces:
        assert "name" in replace
        assert "version" in replace
        if replace["name"] == component and replace["version"] == version:
            return True
    return False


def find_replacements(alternates, component, version):
    """Find the component replacement(s)."""
    return [replacement
            for replacement in alternates
            if replaces_component(replacement, component, version)]


@then('I should find that the component {component} version {version} can be replaced by '
      'component {replaced_by} version {replacement_version}')
def stack_analysis_check_replaces(json_data, component, version, replaced_by, replacement_version):
    """Check that the component is replaced by the given package and version."""
    json_data = context.response.json()
    path = "result/0/recommendation/alternate"
    alternates = get_value_using_path(json_data, path)
    replacements = find_replacements(alternates, component, version)

    for replacement in replacements:
        if replacement["name"] == replaced_by and \
           replacement["version"] == replacement_version:
            break
    else:
        raise Exception("Can not found expected replacement for the component"
                        " {component} {version}".format(component=component,
                                                        version=version))


@then('I should find that the component {component} version {version} has only one replacement')
@then('I should find that the component {component} version {version} has '
      '{expected_replacements:d} replacements')
def stack_analysis_check_replaces_count(json_data, component, version, expected_replacements=1):
    """Check that the component is replaced only once in the alternate analysis."""
    json_data = context.response.json()
    path = "result/0/recommendation/alternate"
    alternates = get_value_using_path(json_data, path)
    replacements = find_replacements(alternates, component, version)
    replacements_count = len(replacements)

    assert replacements_count == expected_replacements, \
        "there must be just %d replacement(s), " \
        "but %d replacements have been found" % (expected_replacements, replacements_count)


def get_user_components(json_data):
    """Get user components from the stack analysis."""
    path = "result/0/user_stack_info/dependencies"
    return get_value_using_path(json_data, path)


def get_alternate_components(json_data):
    """Get alternate components from the stack analysis."""
    path = "result/0/recommendation/alternate"
    return get_value_using_path(json_data, path)


def perform_alternate_components_validation(json_data):
    """Check the user components and alternate components."""
    user_components = get_user_components(json_data)

    # in order to use the 'in' operator later we need to have a sequence
    # of dictionaries with 'name' and 'version' keys
    user_components = [{"name": c["package"],
                        "version": c["version"]} for c in user_components]
    alternate_components = get_alternate_components(json_data)

    for alternate_component in alternate_components:

        check_attribute_presence(alternate_component, "name")

        check_attribute_presence(alternate_component, "replaces")
        replaces = alternate_component["replaces"]

        for replace in replaces:
            check_attribute_presence(replace, "name")
            r_name = replace["name"]

            check_attribute_presence(replace, "version")
            r_version = replace["version"]

            assert replace in user_components,  \
                "The component %s version %s does not replace any user " \
                "component" % (r_name, r_version)


@then('I should find that alternate components replace user components')
def stack_analysis_validate_alternate_components(context):
    """Check that all alternate components replace user components."""
    json_data = context.response.json()
    assert json_data is not None, \
        "JSON response from the previous request does not exist"
    perform_alternate_components_validation(json_data)


def check_cvss_value(cvss):
    """Check CVSS values in CVE records."""
    score = float(cvss)
    # TODO: check the specification how to calculate the maximum possible value
    # https://www.first.org/cvss/specification-document
    assert score >= 0.0, "CVSS score must be >= 0.0"
    assert score <= 10.0, "CVSS score must be <= 10.0"


def check_security_node(context, path):
    """Check the content of security node."""
    json_data = context.response.json()
    assert json_data is not None

    components = get_value_using_path(json_data, path)
    assert components is not None

    for component in components:
        check_attribute_presence(component, "security")
        cve_items = component["security"]
        for cve_item in cve_items:
            check_attribute_presence(cve_item, "CVE")
            check_attribute_presence(cve_item, "CVSS")
            cve = cve_item["CVE"]
            cvss = cve_item["CVSS"]
            check_cve_value(cve)
            check_cvss_value(cvss)


@then('I should find the security node for all dependencies')
def stack_analysis_check_security_node_for_dependencies(context):
    """Check security node presense for all user dependencies."""
    check_security_node(context, "result/0/user_stack_info/analyzed_dependencies")


@then('I should find the security node for all alternate components')
def stack_analysis_check_security_node_for_alternate_components(context):
    """Check security node presense for all alternate components."""
    check_security_node(context, "result/0/recommendation/alternate")


def get_analyzed_components(context):
    """Return all analyzed components from the deserialized JSON file."""
    json_data = context.response.json()
    assert json_data is not None

    path = "result/0/user_stack_info/analyzed_dependencies"
    components = get_value_using_path(json_data, path)
    assert components is not None

    return components


@then('I should find the {cve} security issue for the dependency {package}')
def check_security_issue_existence(context, cve, package):
    """Check if the security issue CVE-yyyy-xxxx can be found for the given analyzed package."""
    components = get_analyzed_components(context)

    for component in components:
        if component["name"] == package:
            check_attribute_presence(component, "security")
            cve_items = component["security"]
            for cve_item in cve_items:
                check_attribute_presence(cve_item, "CVE")
                if cve_item["CVE"] == cve:
                    return
            else:
                raise Exception('Could not find the CVE {c} for the '
                                'package {p}'.format(c=cve, p=package))
    else:
        raise Exception('Could not find the analyzed package {p}'
                        .format(p=package))


@then('I should not find any security issue for the dependency {package}')
def check_security_issue_nonexistence(context, package):
    """Check than none security issue can be found for the given analyzed package."""
    components = get_analyzed_components(context)

    for component in components:
        if component["name"] == package:
            check_attribute_presence(component, "security")
            cve_items = component["security"]
            if cve_items:
                raise Exception('Found security issue(s) for the package {p}'.format(p=package))
            break
    else:
        raise Exception('Could not find the analyzed package {p}'
                        .format(p=package))


@then('I should find dependency named {package} with version {version} in the stack '
      'analysis')
def check_dependency(context, package, version):
    """Check for the existence of dependency for given package."""
    jsondata = context.response.json()
    assert jsondata is not None
    path = "result/0/user_stack_info/dependencies"
    dependencies = get_value_using_path(jsondata, path)
    assert dependencies is not None
    for dependency in dependencies:
        if dependency["package"] == package \
           and dependency["version"] == version:
            break
    else:
        raise Exception('Package {package} with version {version} not found'.
                        format(package=package, version=version))


@then('I should find analyzed dependency named {package} with version {version} in the stack '
      'analysis')
def check_analyzed_dependency(context, package, version):
    """Check for the existence of analyzed dependency for given package."""
    jsondata = context.response.json()
    assert jsondata is not None
    path = "result/0/user_stack_info/analyzed_dependencies"
    analyzed_dependencies = get_value_using_path(jsondata, path)
    assert analyzed_dependencies is not None
    for analyzed_dependency in analyzed_dependencies:
        if analyzed_dependency["name"] == package \
           and analyzed_dependency["version"] == version:
            break
    else:
        raise Exception('Package {package} with version {version} not found'.
                        format(package=package, version=version))


@then('I should find the following analyzed dependencies ({packages}) in the stack analysis')
def check_all_analyzed_dependency(context, packages):
    """Check all analyzed dependencies in the stack analysis."""
    packages = split_comma_separated_list(packages)
    jsondata = context.response.json()
    assert jsondata is not None
    path = "result/0/user_stack_info/analyzed_dependencies"
    analyzed_dependencies = get_value_using_path(jsondata, path)
    assert analyzed_dependencies is not None
    dependencies = get_attribute_values(analyzed_dependencies, "name")
    for package in packages:
        if package not in dependencies:
            raise Exception('Package {package} not found'.format(package=package))


@then("I should get a valid request ID")
def check_stack_analyses_request_id(context):
    """Check the ID attribute in the JSON response.

    Check if ID is in a format like: '477e85660c504b698beae2b5f2a28b4e'
    ie. it is a string with 32 characters containing 32 hexadecimal digits
    """
    check_id_value_in_json_response(context, "request_id")


@then("I should find the status attribute set to success")
def check_stack_analyses_request_id(context):
    """Check if the status is set to success in the JSON response."""
    response = context.response
    json_data = response.json()

    check_attribute_presence(json_data, 'status')

    assert json_data['status'] == "success"


@then('I should find the attribute request_id equals to id returned by stack analysis request')
def check_stack_analysis_id(context):
    """Check the ID of stack analysis."""
    previous_id = context.stack_analysis_id

    json_data = context.response.json()
    assert json_data is not None

    check_attribute_presence(json_data, "request_id")
    request_id = json_data["request_id"]

    assert previous_id is not None
    assert request_id is not None
    assert previous_id == request_id


@then('I should find matching topic lists for all {key} components')
def validate_topic_list(context, key):
    """Verify topics' list for stack dependencies with the input stack topics."""
    json_data = context.response.json()
    path = "result"
    manifest_results = get_value_using_path(json_data, path)

    # loop through results for each of the manifest files
    for result in manifest_results:
        path = "recommendation/input_stack_topics"
        input_stack_topics = get_value_using_path(result, path)

        deps = get_value_using_path(result, key)

        for dep in deps:
            assert len(dep['topic_list']) == len(input_stack_topics[dep['name']])
            assert sorted(dep['topic_list']) == sorted(input_stack_topics[dep['name']])
