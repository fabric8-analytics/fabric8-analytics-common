"""Tests for API endpoints that performs v2 Vunerablity analysis route."""
import requests
import time
import logging
from behave import then, when
from urllib.parse import urljoin
from src.parsing import parse_token_clause
from component_analysis_v2_batchcall import get_packages_from_json
logger = logging.getLogger()

def vulnerability_analysis_batch_call_url(context):
    """Construct url for call."""
    return urljoin(context.core_v2_api_url,
                   '/api/v2/vulnerability-analysis')

def perform_Vuln_batch_call(context, use_user_key, packages_file):
    """Perform Batch Call for vulnerability-analysis."""
    context.duration = None
    start_time = time.time()

    url = vulnerability_analysis_batch_call_url(context)
    parms = {'user_key': context.three_scale_preview_user_key}

    data = get_packages_from_json(packages_file)

    if use_user_key:
        context.response = requests.post(url, params=parms, json=data)
        if context.response.status_code == 429:
            raise Exception("429 Limit excceded")
    else:
        context.response = requests.post(url, json=data)
    end_time = time.time()
    context.duration = end_time - start_time

def validate_vuln_feilds(vul):
    """Validate feilds present in vulnerability."""
    for vuln in vul:
        assert "id" in vuln
        assert "severity" in vuln
        assert "title" in vuln
        assert "url" in vuln
        assert "fixed_in" in vuln

def validate_vuln_basic_feilds(single_item):
    """Validate Basic Vulnerabity feilds."""
    if single_item['vulnerabilities'] != []:
        assert "name" in single_item, "No package Found!"
        assert "version" in single_item, "No Version Found!"
        validate_vuln_feilds(single_item['vulnerabilities'])
    else:
        assert "name" in single_item
        assert "version" in single_item
        assert single_item['vulnerabilities'] == []

def validate_all_feilds(json_data):
    """Validate all the feilds that are present in result."""
    for single_item in json_data:
        validate_vuln_basic_feilds(single_item)

def match_key_value_pair(k, key, val, id, match_down):
    """Validate one step further."""
    if match_down and k['id'] == id:
        assert k[key] == val, "Invalid {key} and {val}".format(key, val)
        assert False

def match_pkg_ver_key_val(item, pkg, ver, key, val, synk_id, match):
    """Validate the package and version"""
    try:
        if item['name'] == pkg and item['version'] == ver:
            for i in item['vulnerabilities']:
                match_key_value_pair(k=i, key=key, val=val, id=synk_id, match_down=match)         
    except KeyError:
        pass

def match_fixed_in(item, pkg, ver, value_to_match, synk_id):
    """Match value preset in fixed in"""
    try:
        if item['name'] == pkg and item['version'] == ver:
            count = 1
            vuln_len = len(item['vulnerabilities'])
            for i in item['vulnerabilities']:
                if i['id'] == synk_id:
                    assert value_to_match in i['fixed_in'], 'The Specified version doesnt exist'
                elif count >= vuln_len:
                    print(item)
                    assert False, 'Id not Found'
                else:
                    count = count + 1
    except KeyError:
        pass

def match_data_in(item, pkg, ver, value_to_match, synk_id, key):
    """Match value preset in fixed in"""
    try:
        if item['name'] == pkg and item['version'] == ver:
            count = 1
            vuln_len = len(item['vulnerabilities'])
            for i in item['vulnerabilities']:
                if i['id'] == synk_id:
                    assert value_to_match == i[key], 'The Specified value {} doesnt exist'.format(value_to_match)
                elif count >= vuln_len:
                    print(item)
                    assert False, 'Id not Found'
                else:
                    count = count + 1
    except KeyError:
        pass

@when("I start vulnerablity analysis for {file} {user_key} user_key")
def start_batch_call(context, file, user_key):
    """Start vulnerablity analysis Batch call."""
    use_user_key = parse_token_clause(user_key)
    perform_Vuln_batch_call(context, use_user_key, file)

@then('I should be able to find all feilds in the result')
def find_vulnerablities(context):
    """I should be able to find some Vulnerablities."""
    json_data = context.response.json()
    validate_all_feilds(json_data)

@then('I should find no vulnerablities in Result for package {name} and version {ver}')
def no_vulns(context, name, ver):
    """I should not find any vulnerablities for pkg and version."""
    json_data = context.response.json()
    count = 1
    vuln_len = len(json_data)
    for single_item in json_data:
        if single_item['name'] == name and single_item['version'] == ver:
            logger.info(single_item)
            assert single_item['vulnerabilities'] == [], "Package has vulneraabilities"
        elif count >= vuln_len:
            assert False, 'Specified Package Version doesnt exist'
        else:
            count = count + 1

@then('I should find pkg {package} and version {version} with vulnerablity id {id} and {key} {value} in Result')
def match_package_version_id(context, package, version, id, key=None, value=None):
    """Match the package and version provided."""
    json_data = context.response.json()

    for single_item in json_data:
        match_data_in(item=single_item,pkg=package, ver=version,value_to_match=value, synk_id=id, key=key)

@then('I should find pkg {package} and version {version} with id {id} and a fixed in {fix}')
def match_fixed_in_result(context, package, version, id, fix):
    """Match a Fixed in version in Result."""
    json_data = context.response.json()
    for single_item in json_data:
        match_fixed_in(single_item, pkg=package, ver=version,value_to_match=fix, synk_id=id)

@then('I should not find any vulnerabilities in the Result')
def no_vulns(context):
    """Result should not have any vulnerabilities."""
    json_data = context.response.json()
    for single_item in json_data:
        assert single_item['vulnerabilities'] == [], 'Vulnerabilities exists!'


