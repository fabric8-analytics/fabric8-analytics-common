"""Tests for API endpoints that performs v2 component analysis."""
import requests

import time

from behave import then, when
from urllib.parse import urljoin

from src.parsing import parse_token_clause


def component_analysis_v2_url(context, ecosystem, component, version):
    """Construct URL for the component analyses REST API call."""
    return urljoin(context.core_v2_api_url,
                   '/api/v2/component-analyses/{e}/{c}/{v}'.format(e=ecosystem,
                                                                   c=component,
                                                                   v=version))


def perform_v2_component_analysis(context, ecosystem, package, version, use_user_key, rate):
    """Call API endpoint to v2 analysis for component."""
    context.duration = None
    start_time = time.time()
    url = component_analysis_v2_url(context, ecosystem, package, version)
    if use_user_key:
        for _ in range(rate):
            context.response = requests.get(
                url, params={'user_key': context.three_scale_preview_user_key})
            # break the loop if rate limit exceeded
            if context.response.status_code == 429:
                break
    else:
        context.response = requests.get(url)
    end_time = time.time()
    # compute the duration
    # plase note that duration==None in case of any errors (which is to be expected)
    context.duration = end_time - start_time


@when("I start v2 component analyses {ecosystem}/{package}/{version} {user_key} user_key")
@when("I start v2 component analyses {ecosystem}/{package}/{version} {rate:d} "
      "times in a minute {user_key} user_key")
def start_v2_component_analysis(context, ecosystem, package, version, user_key, rate=1):
    """Analyse the given component."""
    use_user_key = parse_token_clause(user_key)
    perform_v2_component_analysis(context, ecosystem, package, version, use_user_key, rate)


@then('I should find no recommendation')
def check_recommendation_in_result(context):
    """Check if no recommendation comes."""
    json_data = context.response.json()
    result = json_data["recommendation"]
    assert result == {}


@then('I should find recommended version {version} in the component analysis')
def check_recommended_versions_result(context, version):
    """Check for the recommended version."""
    json_data = context.response.json()
    result = json_data["recommended_versions"]
    assert result == version, "different version found {} != {}".format(version, result)


@then('I should find snyk registration link in the result')
def check_snyk_link(context):
    """Check for snyk link in result."""
    json_data = context.response.json()
    print(json_data['registration_link'])
    assert "registration_link" in json_data, "No snyk link found in the result"


@then('I should find one or more vulnerabilities in result with valid attributes')
def check_vulnerability_in_result(context):
    """Find the vulnerabilities report."""
    json_data = context.response.json()

    if "component_analyses" in json_data:
        vulnerabilities = json_data['component_analyses']['vulnerability']
        for vulnerability in vulnerabilities:
            assert "cvss" in vulnerability
            assert "is_private" in vulnerability
            assert "vendor_cve_ids" in vulnerability


@when('I try to access snyk link i should get {status:d} status code')
def check_snyk_link_is_valid(context, status):
    """Check if snyk link works."""
    json_data = context.response.json()
    url = json_data['registration_link']
    response = requests.get(url)
    assert response.status_code == status, "Unable to access the snyk login url"


@then('I should find essential fields present in the result')
def look_for_other_attributes(context):
    """Check for all attributes."""
    json_data = context.response.json()
    assert "recommended_versions" in json_data, "No recommended version found"
    assert "registration_link" in json_data, "No snyk registration link found"
    assert "component_analyses" in json_data, "No component analyses data found"
    assert "message" in json_data, "No message found"
    assert "severity" in json_data, "No severity found"
    assert "known_security_vulnerability_count" in json_data
    assert "security_advisory_count" in json_data


@then('I should get no result or recommendation with report')
def check_for_recommendation_result_report(context):
    """Check for result if recommedation or not."""
    json_data = context.response.json()
    if "recommendation" in json_data:
        check_recommendation_in_result(context)
    else:
        look_for_other_attributes(context)
        check_vulnerability_in_result(context)


@then('I should find CVE report {cve} with score {score} in the component v2 analysis')
def check_report_cve_score(context, cve, score):
    """Check the cve report for specific cve id and score."""
    json_data = context.response.json()

    if "component_analyses" in json_data:
        vulnerabilities = json_data['component_analyses']['vulnerability']
        for v in vulnerabilities:
            assert "cvss" in v
            assert "is_private" in v
            assert "vendor_cve_ids" in v
            if v["vendor_cve_ids"] == cve and str(v["cvss"]) == score:
                return
    raise Exception("Can not find CVE {} with score {}".format(cve, score))


@then('I should find a private vulnerability in v2 component analysis')
def check_for_private_vul(context):
    """Check for a private vulnerability in report."""
    json_data = context.response.json()

    if "component_analyses" in json_data:
        vulnerabilities = json_data['component_analyses']['vulnerability']
        for v in vulnerabilities:
            if v["is_private"]:
                return
    raise Exception("No private vulnerability found")


@then('I should find no private vulnerability in v2 component analysis')
def check_for_no_privates(context):
    """Check for no private vulnerablities in report."""
    json_data = context.response.json()

    if "component_analyses" in json_data:
        vulnerabilities = json_data['component_analyses']['vulnerability']
        for v in vulnerabilities:
            assert "cvss" in v
            assert "is_private" in v
            assert "vendor_cve_ids" in v
            if v["is_private"]:
                raise Exception("Private vulnerability found")


@then('I should see no registered user fields are exposed in result')
def check_for_exposed(context):
    """Exposed fields for free user check."""
    json_data = context.response.json()
    if "exploitable_vulnerabilities_count" in json_data:
        raise Exception("Field exploitable_vulnerabilities_count Exposed in"
                        " Free user result")
    if "vendor_package_link" in json_data:
        raise Exception("Field vendor_package_link has been exposed for free user")


@then('I should not have any recommended version')
def check_for_no_version_recommended(context):
    """Check for no recommended version if private vuln."""
    json_data = context.response.json()
    assert "recommended_versions" in json_data
    assert json_data["recommended_versions"] == ""
