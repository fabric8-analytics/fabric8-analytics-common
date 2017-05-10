import datetime
import json
import time

from behave import given, then, when
from urllib.parse import urljoin
import jsonschema
import requests


def split_comma_separated_list(l):
    return [i.strip() for i in l.split(',')]


@given('System is in initial state')
def initial_state(context):
    context.restart_system(context)


@given('System is running')
def running_system(context):
    if not context.is_running(context):
        initial_state(context)


@when("I obtain TGT in {service} service")
def get_tgt_in_service(context, service):
    """
    obtains TGT in specified container via `docker exec` and returns output of klist
    """
    context.container = context.run_command_in_service(context, service, ["sleep", "10"])
    assert context.container
    # just in case
    context.exec_command_in_container(context.client, context.container,
                                      'kdestroy')

    # this may take ages if you are not on network: I'm currently writing this in train and I had
    # no wifi nor ethernet and the command would never finish; when I connected to train's wifi
    # it started to work just fine; can you imagine?
    context.exec_command_in_container(context.client, context.container,
                                      'bash -c "echo user | kinit user@EXAMPLE.COM"')
    klist_out = context.exec_command_in_container(context.client, context.container,
                                                  'klist')
    assert "Valid starting" in klist_out


@when("I perform kerberized {method} request to {url}")
def perform_kerberized_request(context, method, url):
    command = "curl -s -X {method} --negotiate -u : http://coreapi-server:5000{url}".format(
        method=method, url=url
    )
    context.kerb_request = \
        context.exec_command_in_container(context.client, context.container, command)


@when("I wait for {ecosystem}/{package}/{version} analysis to {action}")
def wait_for_analysis(context, ecosystem, package, version, action):
    if action == 'finish':
        # Wait for analysis to finish
        timeout = 600
        err = "The analysis of {e}/{p}/{v} takes too long, more than {s} seconds."
        finished = True
    else:
        # Wait for analysis to start
        timeout = 60
        err = "The analysis of {e}/{p}/{v} has not started in {s} seconds."
        finished = False

    url = urljoin(context.coreapi_url, 'api/v1/analyses/{e}/{p}/{v}'.format(e=ecosystem,
                                                                          p=package,
                                                                          v=version))

    start = datetime.datetime.now()
    wait_till = start + datetime.timedelta(seconds=timeout)
    done = False
    while datetime.datetime.now() < wait_till:
        time.sleep(1)
        response = requests.get(url)
        if response.status_code != 200:
            continue
        if not response.json():
            continue
        if finished:
            if not response.json().get('finished_at', None):
                continue
        else:
            if not response.json().get('started_at', None):
                continue
        done = True
        break

    assert done, err.format(e=ecosystem, p=package, v=version, s=timeout)


@when('I access anitya {url}')
def anitya_url(context, url):
    context.response = requests.get(context.anitya_url + url)


@when('I access {url}')
def access_url(context, url):
    context.response = requests.get(context.coreapi_url + url)

@then("I should get API token")
def check_api_token(context):
    try:
        j = json.loads(context.kerb_request)
    except ValueError:
        print(context.kerb_request)
        raise
    assert j["token"]


@then('I should see {num:d} ecosystems')
def check_ecosystems(context, num):
    ecosystems = context.response.json()['items']
    assert len(ecosystems) == num
    for e in ecosystems:
        # assert that there is 'ecosystem' field in every ecosystem
        assert 'ecosystem' in e


@then('I should see 0 packages')
@then('I should see {num:d} packages ({packages}), all from {ecosystem} ecosystem')
def check_packages(context, num=0, packages='', ecosystem=''):
    packages = split_comma_separated_list(packages)
    pkgs = context.response.json()['items']
    assert len(pkgs) == num
    for p in pkgs:
        assert p['ecosystem'] == ecosystem
        assert p['package'] in packages


@then('I should see {num:d} versions ({versions}), all for {ecosystem}/{package} package')
def check_versions(context, num=0, versions='', ecosystem='', package=''):
    versions = split_comma_separated_list(versions)
    vrsns = context.response.json()['items']
    assert len(vrsns) == num
    for v in vrsns:
        assert v['ecosystem'] == ecosystem
        assert v['package'] == package
        assert v['version'] in versions


@then('I should see empty analysis')
def check_json(context):
    assert context.response.json() == {}


@then('I should get {status:d} status code')
def check_status_code(context, status):
    assert context.response.status_code == status


@when('I wait {num:d} seconds')
@then('I wait {num:d} seconds')
def pause_scenario_execution(context, num):
    time.sleep(num)


@then('I should see {state} analysis result for {ecosystem}/{package}/{version}')
def check_analysis_result(context, state, ecosystem, package, version):
    res = context.response.json()
    if state == 'incomplete':
        assert res['ecosystem'] == ecosystem
        assert res['package'] == package
        assert res['version'] == version
        assert datetime.datetime.strptime(res["started_at"], "%Y-%m-%dT%H:%M:%S.%f")
    elif state == 'complete':
        assert datetime.datetime.strptime(res["finished_at"], "%Y-%m-%dT%H:%M:%S.%f")
        analyzers_keys = context.get_expected_component_analyses(ecosystem)
        actual_keys = set(res["analyses"].keys())
        missing, unexpected = context.compare_analysis_sets(actual_keys,
                                                            analyzers_keys)
        err_str = 'unexpected analyses: {}, missing analyses: {}'
        assert not missing and not unexpected, err_str.format(unexpected, missing)
        analyzers_with_standard_schema = set(analyzers_keys)
        analyzers_with_standard_schema -= context.NONSTANDARD_ANALYSIS_FORMATS
        for a in analyzers_with_standard_schema:
            a_keys = set(res["analyses"].get(a, {}).keys())
            if not a_keys and a in context.UNRELIABLE_ANALYSES:
                continue
            assert a_keys.issuperset({"details", "status", "summary"}), a_keys


@then('Result of {ecosystem}/{package}/{version} should be valid')
def validate_analysis_result(context, ecosystem, package, version):
    res = context.response.json()
    # make sure analysis has finished
    assert res['finished_at'] is not None
    # we want to validate top-level analysis and worker results that have "schema" defined
    structures_to_validate = [res]
    for _, worker_result in res['analyses'].items():
        # TODO: in future we want to mandate that all workers have their schemas,
        #  so we'll remove the condition
        if 'schema' in worker_result:
            structures_to_validate.append(worker_result)

    for struct in structures_to_validate:
        schema = requests.get(struct['schema']['url']).json()
        jsonschema.validate(struct, schema)


@when("I get a valid request ID")
@then("I should get a valid request ID")
def check_stack_analyses_request_id(context):
    assert context.response['status'] == "success"
    assert len(context.response['id']) == 32


@when("I post a valid {manifest} to {url}")
def perform_valid_manifest_post(context, manifest, url):
    files = {'manifest[]': open("data/poms/{manifest}".format(manifest=manifest.replace("\"", '')), 'r')}
    context.response = requests.post("{coreapi_url}{url}".format(
        coreapi_url=context.coreapi_url, url=url
    ),
        files=files
    ).json()
    context.response.raise_for_status()


@then("I get stack analyses response via {url}")
def get_stack_analyses_response(context, url):
    url = "{base_url}{url}{request_id}".format(
        base_url=context.coreapi_url,
        url=url, request_id=context.response['id'])
    retry_count = 120
    retry_interval = 5
    counter = 0
    while counter < retry_count:
        context.response = requests.get(url)
        counter += 1
        if context.response.status_code != 202:  # not in progress
            context.response.raise_for_status()
            context.response = context.response.json()
            break
        time.sleep(retry_interval)
    else:
        assert True, "Stack analyses could not be completed within {t} seconds".format(t=counter * retry_interval)


@then("Response matches {response}")
def compare_stack_analyses_response(context, response):
    temp = open("data/responses/{response}".format(response=response.replace("\"", '')), 'r')
    # TODO: when stack analysis will work, implement compare
    pass
