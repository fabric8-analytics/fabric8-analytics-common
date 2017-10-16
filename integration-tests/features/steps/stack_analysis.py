"""Tests for API endpoints that performs stack analysis."""
import requests
import os

from behave import given, then, when
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


@when("I wait for stack analysis to finish")
@when("I wait for stack analysis to finish {token} authorization token")
@when("I wait for stack analysis version {version} to finish {token} authorization token")
def wait_for_stack_analysis_completion(context, version="2", token="without"):
    """Try to wait for the stack analysis to be finished.

    This step assumes that stack analysis has been started previously and
    thus that the job ID is known

    Current API implementation returns just three HTTP codes:
    200 OK : analysis is already finished
    202 Accepted: analysis is started or is in progress (or other state!)
    401 UNAUTHORIZED : missing or inproper authorization token
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
    # please note that the stack analysis v2 now becames the only available endpoint
    endpoint = {"1": "/api/v1/stack-analyses-v1/",
                "2": "/api/v1/stack-analyses/"}.get(version)
    if endpoint is None:
        raise Exception("Wrong version specified: {v}".format(v=version))
    return urljoin(context.coreapi_url, endpoint)


@when("I send NPM package manifest {manifest} to stack analysis")
@when("I send NPM package manifest {manifest} to stack analysis {token} authorization token")
@when("I send NPM package manifest {manifest} to stack analysis version {version} {token} "
      "authorization token")
def npm_manifest_stack_analysis(context, manifest, version="2", token="without"):
    """Send the NPM package manifest file to the stack analysis."""
    endpoint = stack_analysis_endpoint(context, version)
    use_token = parse_token_clause(token)
    send_manifest_to_stack_analysis(context, manifest, 'package.json',
                                    endpoint, use_token)


@when("I send Python package manifest {manifest} to stack analysis")
@when("I send Python package manifest {manifest} to stack analysis {token} authorization token")
@when("I send Python package manifest {manifest} to stack analysis version {version} {token} "
      "authorization token")
def python_manifest_stack_analysis(context, manifest, version="2", token="without"):
    """Send the Python package manifest file to the stack analysis."""
    endpoint = stack_analysis_endpoint(context, version)
    use_token = parse_token_clause(token)
    send_manifest_to_stack_analysis(context, manifest, 'requirements.txt',
                                    endpoint, use_token)


@when("I send Maven package manifest {manifest} to stack analysis")
@when("I send Maven package manifest {manifest} to stack analysis {token} authorization token")
@when("I send Maven package manifest {manifest} to stack analysis version {version} {token} "
      "authorization token")
def maven_manifest_stack_analysis(context, manifest, version="2", token="without"):
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


@when('I download and parse outlier probability threshold value')
def download_and_parse_outlier_probability_threshold_value(context):
    """Download and parse outlier probability threshold value.

    This Special step that is needed to get the stack analysis outlier
    probability threshold.
    """
    content = download_file_from_url(STACK_ANALYSIS_CONSTANT_FILE_URL)
    context.outlier_probability_threshold = parse_float_value_from_text_stream(
        content, STACK_ANALYSIS_OUTLIER_PROBABILITY_CONSTANT_NAME)


@then('I should have outlier probability threshold value between {min:f} and {max:f}')
def check_outlier_probability_threshold_value(context, min, max):
    """Check that the outlier probability falls between selected range."""
    v = context.outlier_probability_threshold
    assert v is not None
    assert v >= min
    assert v <= max


def check_outlier_probability(usage_outliers, package_name, threshold_value):
    """Check the outlier probability.

    Try to find outlier probability for given package is found and that
    its probability is within permitted range.
    """
    # NOTE: there's a typo in the attribute name (issue #73)
    # the following line should be updated after the issue ^^^ will be fixed
    outlier_probability_attribute = "outlier_prbability"

    for usage_outlier in usage_outliers:
        if usage_outlier["package_name"] == package_name:
            assert outlier_probability_attribute in usage_outlier, \
                "'%s' attribute is expected in the node, " \
                "found: %s attributes " % (outlier_probability_attribute,
                                           ", ".join(usage_outlier.keys()))
            probability = usage_outlier[outlier_probability_attribute]
            assert probability is not None
            v = float(probability)
            assert v >= threshold_value and v <= 1.0, \
                "outlier_prbability value should fall within %f..1.0 range, "\
                "found %f value instead" % (threshold_value, v)
            return
    raise Exception("Can not find usage outlier for the package {p}".format(p=package_name))


@then('I should find the proper outlier record for the {component} component')
def stack_analysis_check_outliers(context, component):
    """Check the outlier record in the stack analysis."""
    json_data = context.response.json()
    threshold = context.outlier_probability_threshold
    # log.info('Usage outlier threshold: %r' % threshold)
    path = "result/0/recommendation/usage_outliers"
    usage_outliers = get_value_using_path(json_data, path)
    check_outlier_probability(usage_outliers, component, threshold)


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


def check_licenses(node, expected_licenses):
    """Check that the expected license can be found in the list of licenses."""
    for item in node:
        licenses = item["licenses"]
        assert licenses is not None
        for license in licenses:
            if license not in expected_licenses:
                raise Exception("Unexpected license found: {license}".format(
                                license=license))


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
    path = "result/0/user_stack_info/analyzed_dependencies"
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
    path = "result/0/user_stack_info/analyzed_dependencies"
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


def check_cve_value(cve):
    """Check CVE values in CVE records."""
    pattern = "CVE-([0-9]{4})-[0-9]{4,}"

    match = re.fullmatch(pattern, cve)
    assert match is not None, "Improper CVE number %s" % cve

    year = int(re.fullmatch(pattern, cve).group(1))
    current_year = datetime.datetime.now().year

    # well the lower limit is a bit arbitrary
    # (according to SRT guys it should be 1999)
    assert year >= 1999 and year <= current_year


def check_cvss_value(cvss):
    """Check CVSS values in CVE records."""
    score = float(cvss)
    # TODO: check the specificaion how to calculate the maximum possible value
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
    check_security_node(context, "result/0/user_stack_info/dependencies")


@then('I should find the security node for all alternate components')
def stack_analysis_check_security_node_for_alternate_components(context):
    """Check security node presense for all alternate components."""
    check_security_node(context, "result/0/recommendation/alternate")


@then('I should find the {cve} security issue for the dependency {package}')
def check_security_issue_existence(context, cve, package):
    """Check if the security issue CVE-yyyy-xxxx can be found for the given analyzed package."""
    json_data = context.response.json()
    assert json_data is not None

    path = "result/0/user_stack_info/dependencies"
    components = get_value_using_path(json_data, path)
    assert components is not None

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
