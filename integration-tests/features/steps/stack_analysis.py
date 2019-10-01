"""Tests for API endpoints that performs stack analysis."""
import requests
import time
import os
import json
from behave import then, when
from urllib.parse import urljoin
import jsonschema
import random
from src.attribute_checks import check_attribute_presence, check_cve_value
from src.parsing import parse_token_clause
from src.utils import split_comma_separated_list
from src.json_utils import check_id_value_in_json_response
from src.json_utils import get_value_using_path
from src.authorization_tokens import authorization, authorization_with_eco_origin
from src.stack_analysis_common import contains_alternate_node, stack_analysis_endpoint
from src.stack_analysis_common import check_frequency_count, get_json_data
from src.stack_analysis_common import get_components_with_cve


STACK_ANALYSIS_CONSTANT_FILE_URL = "https://raw.githubusercontent.com/" \
    "fabric8-analytics/fabric8-analytics-stack-analysis/master/" \
    "analytics_platform/kronos/pgm/src/pgm_constants.py"

STACK_ANALYSIS_OUTLIER_PROBABILITY_CONSTANT_NAME = \
    "KRONOS_OUTLIER_PROBABILITY_THRESHOLD_VALUE"


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
    context.duration = None
    start_time = time.time()

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
    end_time = time.time()
    # compute the duration
    # plase note that duration==None in case of any errors (which is to be expected)
    context.duration = end_time - start_time


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


def send_manifest_to_stack_analysis(context, manifest, name, endpoint, use_token, **kwargs):
    """Send the selected manifest file to stack analysis."""
    filename = 'data/{manifest}'.format(manifest=manifest)
    manifest_file_dir = os.path.dirname(filename)
    path_to_manifest_file = os.path.abspath(manifest_file_dir)
    context.manifest = manifest

    # please note that the trick with (None, path_to_manifest_file) has to be
    # used here so the REST API call would work properly. It is similar to use
    # curl -F 'manifest[]=@filename' -F 'filePath[]=PATH_TO_FILE'
    files = {'manifest[]': (name, open(filename, 'rb')),
             'filePath[]': (None, path_to_manifest_file)}
    if use_token:
        response = requests.post(endpoint, files=files,
                                 headers=authorization_with_eco_origin(
                                     context,
                                     ecosystem=kwargs.get('ecosystem', None),
                                     origin=kwargs.get('origin', None)))
    else:
        response = requests.post(endpoint, files=files)
    context.response = response


def test_stack_analyses_with_deps_file(context, ecosystem, manifest, origin, endpoint):
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
    context.response = requests.post(endpoint, files=files,
                                     headers=authorization_with_eco_origin(
                                         context, ecosystem, origin))


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
                                    endpoint, use_token, ecosystem='npm', origin='vscode')


@when("I send Python package manifest {manifest} to stack analysis")
@when("I send Python package manifest {manifest} to stack analysis {token} authorization token")
@when("I send Python package manifest {manifest} to stack analysis version {version:d}")
@when("I send Python package manifest {manifest} to stack analysis version {version:d} {token} "
      "authorization token")
def python_manifest_stack_analysis(context, manifest, version=3, token="without"):
    """Send the Python package manifest file to the stack analysis."""
    endpoint = stack_analysis_endpoint(context, version)
    use_token = parse_token_clause(token)
    send_manifest_to_stack_analysis(context, manifest, 'pylist.json',
                                    endpoint, use_token, ecosystem='pypi', origin='vscode')


@when("I test {ecosystem} dependencies file {manifest} for stack analysis from {origin}")
def process_deps_file_from_origin(context, ecosystem, manifest, origin, version=3):
    """Test stack analyses of an ecosystem specific dependencies file from an integration point."""
    endpoint = stack_analysis_endpoint(context, version)
    test_stack_analyses_with_deps_file(context, ecosystem.lower(), manifest, origin, endpoint)


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
                                    endpoint, use_token, ecosystem='maven', origin='vscode')


@when("I send new Maven package manifest {manifest} to stack analysis version {version:d} {token} "
      "authorization token")
def maven_new_manifest_stack_analysis(context, manifest, version=3, token="without"):
    """Send the Maven package manifest file to the stack analysis."""
    endpoint = stack_analysis_endpoint(context, version)
    use_token = parse_token_clause(token)
    send_manifest_to_stack_analysis(context, manifest, 'dependencies.txt',
                                    endpoint, use_token, ecosystem='maven', origin='vscode')


def check_result_node(resp):
    """Check result node in stack analysis response."""
    assert resp is not None
    assert len(resp["results"]) >= 1


def check_stack_analysis_status(resp_json, err):
    """Ensure that the stack analyses result has been asserted in the loop."""
    assert resp_json.get("status") == "success", err


@then("stack analyses response is available via {url}")
def check_stack_analyses_response(context, url):
    """Check the stack analyses response available on the given URL."""
    response = context.response
    resp = response.json()

    check_result_node(resp)
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
    check_stack_analysis_status(resp_json, err)

    # ensure that the response is in accordance to the Stack Analyses schema
    schema = requests.get(resp_json["schema"]["url"]).json()
    jsonschema.validate(resp_json, schema)


@then('I should find the proper outlier record for the {component} component')
def stack_analysis_check_outliers(context, component):
    """Check the outlier record in the stack analysis."""
    json_data = get_json_data(context)
    path = "result/0/recommendation/usage_outliers"
    usage_outliers = get_value_using_path(json_data, path)
    check_frequency_count(usage_outliers, component)


@then('I should find that total {count} outliers are reported')
def check_outlier_count(context, count=2):
    """Check the number of outliers in the stack analysis."""
    json_data = get_json_data(context)
    path = "result/0/recommendation/usage_outliers"
    usage_outliers = get_value_using_path(json_data, path)
    assert len(usage_outliers) == int(count)


@then('I should find that valid outliers are reported')
def check_outlier_validity(context):
    """Check the outlier validity in the stack analysis."""
    json_data = get_json_data(context)
    path = "result/0/recommendation/usage_outliers"
    usage_outliers = get_value_using_path(json_data, path)
    for usage_outlier in usage_outliers:
        # log.info("PACKAGE: {}".format(usage_outlier["package_name"]))
        check_frequency_count(usage_outliers, usage_outlier["package_name"])


@then('I should find that greater than {min_count} companions are reported')
def check_companion_count(context, min_count=0):
    """Check that we have more than min_count companions."""
    json_data = get_json_data(context)
    path = "result/0/recommendation/companion"
    companions = get_value_using_path(json_data, path)
    assert len(companions) > int(min_count)


def check_for_unexpected_licenses(licenses, expected_licenses):
    """Check that none unexpected licenses can be found."""
    for license in licenses:
        if license not in expected_licenses:
            raise Exception("Unexpected license found: {license}".format(
                            license=license))


def check_for_expected_licenses(licenses, expected_licenses):
    """Check that all licenses are also included in expected licenses."""
    for expected_license in expected_licenses:
        if expected_license not in licenses:
            raise Exception("Required license could not be found: {license}".format(
                            license=expected_license))


def check_licenses(licenses, expected_licenses):
    """Compare list of read licenses with list of expected licenses.

    Check that all expected licenses and only such licenses can be found in the list of licenses.
    """
    assert licenses is not None
    check_for_unexpected_licenses(licenses, expected_licenses)
    check_for_expected_licenses(licenses, expected_licenses)


@then('I should find the following licenses ({licenses}) under the path {path}')
def stack_analysis_check_licenses(context, licenses, path):
    """Check the license(s) in the stack analysis."""
    licenses = split_comma_separated_list(licenses)
    json_data = get_json_data(context)
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
    json_data = get_json_data(context)

    # those two lists should have no element in common
    analyzed_packages = get_analyzed_packages(json_data)
    companion_packages = get_companion_packages(json_data)

    for companion_package in companion_packages:
        assert companion_package not in analyzed_packages, \
            "The analyzed package '%s' is found in companion packages as well" \
            % companion_package


@then('I should get {field_name} field in stack report')
def verify_stack_level_field_presence_in_stack_report(context, field_name):
    """Check that the given field can be found in the stack report."""
    json_data = get_json_data(context)
    path = 'result/0/user_stack_info'
    user_stack_info = get_value_using_path(json_data, path)
    assert user_stack_info.get(field_name, None) is not None


@then('I should find {field_name} field in recommendation')
def verify_stack_level_field_presence_in_recommendation(context, field_name):
    """Check that the given field can be found in the recommendation."""
    json_data = get_json_data(context)
    path = 'result/0/recommendation'
    recommendation = get_value_using_path(json_data, path)
    assert recommendation.get(field_name, None) is not None


def replaces_component(replacement, component, version):
    """Check the component replacement info in the stack analysis."""
    check_attribute_presence(replacement, "replaces")
    replaces = replacement["replaces"]
    for replace in replaces:
        check_attribute_presence(replace, "name")
        check_attribute_presence(replace, "version")
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
def stack_analysis_check_replaces(context, component, version, replaced_by, replacement_version):
    """Check that the component is replaced by the given package and version."""
    json_data = get_json_data(context)
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
def stack_analysis_check_replaces_count(context, component, version, expected_replacements=1):
    """Check that the component is replaced only once in the alternate analysis."""
    json_data = get_json_data(context)
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
    json_data = get_json_data(context)
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
    json_data = get_json_data(context)

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
    json_data = get_json_data(context)

    path = "result/0/user_stack_info/analyzed_dependencies"
    components = get_value_using_path(json_data, path)
    assert components is not None

    return components


def cve_found(cve_items, cve):
    """Look for CVE in security node."""
    for cve_item in cve_items:
        check_attribute_presence(cve_item, "CVE")
        if cve_item["CVE"] == cve:
            return True
    return False


@then('I should find the {cve} security issue for the dependency {package}')
def check_security_issue_existence(context, cve, package):
    """Check if the security issue CVE-yyyy-xxxx can be found for the given analyzed package."""
    components = get_analyzed_components(context)

    for component in components:
        if component["name"] == package:
            check_attribute_presence(component, "security")
            cve_items = component["security"]
            if cve_found(cve_items, cve):
                # CVE for the component has been found - > let's finish this check
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


def test_dependency_for_package_version(dependencies, package, version):
    """Test if the dependency attribute contains a given package + version pair."""
    for dependency in dependencies:
        if dependency["package"] == package \
           and dependency["version"] == version:
            break
    else:
        raise Exception('Package {package} with version {version} not found'.
                        format(package=package, version=version))


def test_analyzed_dependency_for_package_version(analyzed_dependencies, package, version):
    """Test if the analyzed_dependency attribute contains a given name + version pair."""
    for analyzed_dependency in analyzed_dependencies:
        if analyzed_dependency["name"] == package \
           and analyzed_dependency["version"] == version:
            break
    else:
        raise Exception('Package {package} with version {version} not found'.
                        format(package=package, version=version))


@then('I should find dependency named {package} with version {version} in the stack '
      'analysis')
def check_dependency(context, package, version):
    """Check for the existence of dependency for given package."""
    json_data = get_json_data(context)
    path = "result/0/user_stack_info/dependencies"
    dependencies = get_value_using_path(json_data, path)

    assert dependencies is not None, \
        "Empty or missing attribute user_stack_info/dependencies"

    test_dependency_for_package_version(dependencies, package, version)


@then('I should find analyzed dependency named {package} with version {version} in the stack '
      'analysis')
def check_analyzed_dependency(context, package, version):
    """Check for the existence of analyzed dependency for given package."""
    json_data = get_json_data(context)
    path = "result/0/user_stack_info/analyzed_dependencies"
    analyzed_dependencies = get_value_using_path(json_data, path)

    assert analyzed_dependencies is not None, \
        "Empty or missing attribute user_stack_info/analyzed_dependencies"

    test_analyzed_dependency_for_package_version(analyzed_dependencies, package, version)


@then('I should find the following dependencies ({packages}) in the stack analysis')
def check_all_dependencies(context, packages):
    """Check all dependencies in the stack analysis."""
    json_data = get_json_data(context)
    packages = split_comma_separated_list(packages)
    path = "result/0/user_stack_info/dependencies"
    analyzed_dependencies = get_value_using_path(json_data, path)
    assert analyzed_dependencies is not None
    dependencies = get_attribute_values(analyzed_dependencies, "package")
    for package in packages:
        if package not in dependencies:
            raise Exception('Package {package} not found'.format(package=package))


@then('I should find the following analyzed dependencies ({packages}) in the stack analysis')
def check_all_analyzed_dependencies(context, packages):
    """Check all analyzed dependencies in the stack analysis."""
    json_data = get_json_data(context)
    packages = split_comma_separated_list(packages)
    path = "result/0/user_stack_info/analyzed_dependencies"
    analyzed_dependencies = get_value_using_path(json_data, path)
    assert analyzed_dependencies is not None
    dependencies = get_attribute_values(analyzed_dependencies, "name")
    for package in packages:
        if package not in dependencies:
            raise Exception('Package {package} not found'.format(package=package))


@then("I should find at least one dependency")
@then("I should find at least {expected:n} dependencies")
def check_dependencies_count(context, expected=1):
    """Check number of dependencies."""
    json_data = get_json_data(context)
    path = "result/0/user_stack_info/dependencies"
    dependencies_count = len(get_value_using_path(json_data, path))
    assert dependencies_count >= expected, \
        "Found only {} dependencies, but at least {} is expected".format(
            dependencies_count, expected)


@then("I should find at least one analyzed dependency")
@then("I should find at least {expected:n} analyzed dependencies")
def check_analyzed_dependencies_count(context, expected=1):
    """Check number of analyzed dependencies."""
    json_data = get_json_data(context)
    path = "result/0/user_stack_info/analyzed_dependencies_count"
    analyzed_dependencies_count = get_value_using_path(json_data, path)
    assert analyzed_dependencies_count >= expected, \
        "Found only {} analyzed dependencies, but at least {} is expected".format(
            analyzed_dependencies_count, expected)


@then("I should find exactly one really unknown dependency")
@then("I should find exactly {expected:n} really unknown dependencies")
def check_unknown_dependencies_count_exact_check(context, expected=1):
    """Check number of really unknown dependencies (for specific manifests)."""
    json_data = get_json_data(context)
    path = "result/0/user_stack_info/unkwnown_dependencies_count"
    unknown_dependencies_count = get_value_using_path(json_data, path)
    assert unknown_dependencies_count == expected, \
        "Found {} unknown dependencies, but {} is expected".format(
            unknown_dependencies_count, expected)


@then("I should find no more than {expected:n} unknown dependencies")
def check_unknown_dependencies_count(context, expected):
    """Check number of unknown dependencies."""
    json_data = get_json_data(context)
    path = "result/0/user_stack_info/unknown_dependencies_count"
    unknown_dependencies_count = get_value_using_path(json_data, path)
    assert unknown_dependencies_count <= expected, \
        "Found {} unknown dependencies, but at most {} is expected".format(
            unknown_dependencies_count, expected)


@then("I should get a valid request ID")
def check_stack_analyses_request_id(context):
    """Check the ID attribute in the JSON response.

    Check if ID is in a format like: '477e85660c504b698beae2b5f2a28b4e'
    ie. it is a string with 32 characters containing 32 hexadecimal digits
    """
    check_id_value_in_json_response(context, "request_id")


@then("I should find the status attribute set to success")
def check_stack_analyses_request_status_attribute(context):
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


@when('I look at recent stack analysis')
def look_at_recent_stack_analysis(context):
    """Just dummy step to make test scenarios more readable."""
    assert context is not None
    json_data = context.response.json()
    assert json_data is not None


@when('I look at the stack analysis duration')
def look_at_stack_analysis_duration(context):
    """Just dummy step to make test scenarios more readable."""
    assert context is not None
    assert context.duration is not None


@then('I should see that the duration is less than {duration:d} second')
@then('I should see that the duration is less than {duration:d} seconds')
def check_stack_analysis_duration_in_seconds(context, duration):
    """Check the stack analysis duration when the duration is specified in seconds."""
    # with very low probability, leap second might occur
    assert context.duration > 0, \
        "Duration is negative, it means that the leap second occured during stack analysis"

    # check if the measured duration is less than maximum expected threshold
    assert context.duration < duration, \
        "Stack analysis duration is too long: {} seconds instead of {}".format(
            duration, context.duration)


@then('I should see that the duration is less than {duration:d} minute')
@then('I should see that the duration is less than {duration:d} minutes')
def check_stack_analysis_duration_in_minutes(context, duration):
    """Check the stack analysis duration when the duration is specified in minutes."""
    # just use the existing code, with different units
    check_stack_analysis_duration_in_seconds(context, duration * 60)


@then('I should find a recommended version when a CVE is found')
def check_recommended_version_for_cve(context):
    """Check that all E/P/V with CVE detected also have recommended versions."""
    # retrieve all components
    components = get_analyzed_components(context)

    # retrieve components with CVE record(s)
    components_with_cve = get_components_with_cve(components)

    # check if at least one recommendation is found for a component with CVE
    for component_with_cve in components_with_cve:
        check_attribute_presence(component_with_cve, "recommended_latest_version")
        recommended = component_with_cve["recommended_latest_version"]
        assert len(recommended) >= 1


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


@when('I tried to fetch dynamic manifests from s3')
def dynamic_manifest_file(context):
    """Integration for dynamically generated manifests files."""
    response, status = context.s3interface.get_object_from_s3()
    assert status == 200, response


@then('I should be able to validate them')
def validate_dynamic_manifest_file(context):
    """Generate valid manifest files out of Multiple Stacks file from S3."""
    file_save_path = os.path.join(
        os.path.abspath(os.curdir), "data", "valid_manifests/")
    if not os.path.exists(file_save_path):
        os.makedirs(file_save_path)

    files_to_validate = [
        ('npmlist.json', validate_file_npm),
        ('dependencies.json', validate_file_maven),
        ('pylist.json', validate_file_pypi)
    ]
    for file, func in files_to_validate:
        with open('dynamic_manifests/' + file) as fp:
            contents = json.load(fp)
        contents = random.sample(contents, 1)
        func(contents[0], file, file_save_path)


def validate_file_npm(contents, file_name, file_save_path):
    """Generate file for npm."""
    data = {'dependencies': {}}
    with open(file_save_path + file_name, 'w') as manifest:
        data['dependencies'] = contents.pop('dependencies')
        json.dump(data, manifest)


def validate_file_pypi(contents, file_name, file_save_path):
    """Generate file for pypi."""
    with open(file_save_path + file_name, 'w') as manifest:
        json.dump(contents[0], manifest)


def validate_file_maven(contents, file_name, file_save_path):
    """Generate file for maven."""
    with open(file_save_path + 'dependencies.txt', 'w') as manifest:
        manifest.write(contents['content'])
