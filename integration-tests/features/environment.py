import json
import datetime
import subprocess
import os.path
import contextlib

from behave.log_capture import capture
import docker
import requests
import time

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_DIR = os.path.dirname(os.path.dirname(_THIS_DIR))

# The following API endpoint is used to check if the system is started
_API_ENDPOINT = 'api/v1'

# Ports used by various services
_FABRIC8_ANALYTICS_SERVER = 32000
_FABRIC8_ANALYTICS_JOBS = 34000
_ANITYA_SERVICE = 31005

# Endpoint for jobs debug API
_JOBS_DEBUG_API = _API_ENDPOINT + "/debug"

# Default timeout values for the stack analysis and component analysis endpoints
_DEFAULT_STACK_ANALYSIS_TIMEOUT = 600
_DEFAULT_COMPONENT_ANALYSIS_TIMEOUT = 600


def _make_compose_name(suffix='.yml'):
    return os.path.join(_REPO_DIR, 'docker-compose' + suffix)


def _set_default_compose_path(context):
    base_compose = _make_compose_name()
    test_specific_compose = _make_compose_name(".integration-tests.yml")
    # Extra containers are added as needed by integration setup commands
    context.docker_compose_path = [base_compose, test_specific_compose]

### make sure behave uses pytest improved asserts
# Behave runner uses behave.runner.exec_file function to read, compile
# and exec code of environment file and step files *in this order*.
# Therefore we provide a new implementation here, which uses pytest's
# _pytest.assertion.rewrite to rewrite the bytecode with pytest's
# improved asserts.
# This means that when behave tries to load steps, it will use our exec_file.
# => SUCCESS
# Don't ask how long it took me to figure this out.
import behave.runner


def exec_file(filename, globals=None, locals=None):
    if globals is None:
        globals = {}
    if locals is None:
        locals = globals
    locals['__file__'] = filename
    from py import path
    from _pytest import config
    from _pytest.assertion import rewrite
    f = path.local(filename)
    filename2 = os.path.relpath(filename, os.getcwd())
    config = config._prepareconfig([], [])
    _, code = rewrite._rewrite_test(config, f)
    exec(code, globals, locals)

behave.runner.exec_file = exec_file
### end this madness


def _make_compose_command(context, *args):
    cmd = ['docker-compose']
    for compose_file in context.docker_compose_path:
        cmd.append('-f')
        cmd.append(compose_file)
    cmd.extend(args)
    print(cmd)
    return cmd


def _start_system(context):
    if context.docker_compose_path:
        cmd = _make_compose_command(context, 'up', '--no-build', '-d')
    else:
        cmd = ['kubectl', 'create', '-f', context.kubernetes_dir_path]

    subprocess.check_output(cmd, stderr=subprocess.STDOUT)


def _make_compose_teardown_callback(context, services):
    cmds = []
    cmds.append(_make_compose_command(context, 'kill', *services))
    cmds.append(_make_compose_command(context, 'rm', '-fv', *services))

    def teardown_services():
        for cmd in cmds:
            subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    return teardown_services


def _run_command_in_service(context, service, command):
    """
    run command in specified service via `docker-compose run`; command is list of strs
    """
    if context.docker_compose_path:
        cmd = _make_compose_command(context, 'run', '--rm', '-d', service)
        cmd.extend(command)
    else:
        raise Exception("not implemented")

    try:
        # universal_newlines decodes output on Python 3.x
        output = subprocess.check_output(cmd, universal_newlines=True).strip()
        print(output)
        return output
    except subprocess.CalledProcessError as ex:
        print(ex.output)
        raise


def _exec_command_in_container(client, container, command):
    """
    equiv of `docker exec`, command is str
    """
    exec_id = client.exec_create(container, command)
    output = client.exec_start(exec_id).decode('utf-8')
    print(output)
    return output


def _get_k8s_volumes_to_delete():
    # universal_newlines decodes output on Python 3.x
    out = subprocess.check_output(['kubectl', 'get', 'pods', '-o', 'json'], universal_newlines=True)
    j = json.loads(out)
    volumes = []
    for pod in j['items']:
        pod_vols = pod['spec'].get('volumes', [])
        for pod_vol in pod_vols:
            if 'hostPath' in pod_vol:
                volumes.append(pod_vol['hostPath']['path'])
    return volumes


def _dump_server_logs(context, tail=None):
    if context.docker_compose_path:
        cmd = _make_compose_command(context, 'logs')
        if tail is not None:
            cmd.append('--tail={:d}'.format(tail))
        subprocess.check_call(cmd, stderr=subprocess.STDOUT)
    else:
        pass  # No current support for dumping logs under k8s


def _teardown_system(context):
    cmds = []
    if context.docker_compose_path:
        cmds.append(_make_compose_command(context, 'kill'))
        cmds.append(_make_compose_command(context, 'rm', '-fv'))
        if hasattr(context, "container"):
            cmds.append(['docker', "kill", context.container])
            cmds.append(['docker', "rm", "-fv", "--rm-all", context.container])
        _set_default_compose_path(context)
    else:
        cmds.append(['kubectl', 'delete', '--ignore-not-found', '-f', context.kubernetes_dir_path])
        volumes = _get_k8s_volumes_to_delete()
        for volume in volumes:
            # TODO: the sudo thing is not very nice, but...
            cmds.append(['sudo', 'rm', '-rf', volume])
            cmds.append(['sudo', 'mkdir', volume])

    for cmd in cmds:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)


def _wait_for_system(context, wait_for_server=60):
    start = datetime.datetime.now()
    wait_till = start + datetime.timedelta(seconds=wait_for_server)
    # try to wait for server to start for some time
    while datetime.datetime.now() < wait_till:
        time.sleep(1)
        started_all = False
        if context.kubernetes_dir_path:
            res = json.loads(subprocess.check_output(['kubectl', 'get', 'pods', '-o', 'json']))
            for pod in res['items']:
                status = pod.get('status', {})
                conditions = status.get('conditions', [])
                phase = status.get('phase', '')
                if status == {}:
                    continue
                if phase != 'Running':
                    continue
                for condition in conditions:
                    if condition['type'] == 'Ready' and condition['status'] != 'True':
                        continue
                # if we got here, then everything is running
                started_all = True
                break
        else:
            if _is_running(context):
                started_all = True
                break
    if started_all:
        # let's give the whole system a while to breathe
        time.sleep(float(context.config.userdata.get('breath_time', 5)))
    else:
        raise Exception('Server failed to start in under {s} seconds'.
                        format(s=wait_for_server))


def _wait_for_api(context, wait_for_service, check_function):
    for _ in range(wait_for_service):
        if check_function(context):
            break
        time.sleep(1)
    else:
        raise Exception('Timeout waiting for the API service')


def _wait_for_jobs_debug_api_service(context, wait_for_service=60):
    _wait_for_api(context, wait_for_service, _is_jobs_debug_api_running)


def _wait_for_component_search_service(context, wait_for_service=60):
    _wait_for_api(context, wait_for_service, _is_component_search_service_running)


def _restart_system(context, wait_for_server=60):
    try:
        _teardown_system(context)
        _start_system(context)
        _wait_for_system(context, wait_for_server)
    except subprocess.CalledProcessError as e:
        raise Exception('Failed to restart system. Command "{c}" failed:\n{o}'.
                        format(c=' '.join(e.cmd), o=e.output))


def _is_api_running(url):
    try:
        res = requests.get(url)
        if res.status_code in {200, 401}:
            return True
    except requests.exceptions.ConnectionError:
        pass
    return False


def _is_running(context):
    return _is_api_running(context.coreapi_url + _API_ENDPOINT) and \
           _is_api_running(context.jobs_api_url + _API_ENDPOINT)


def _is_jobs_debug_api_running(context):
    return _is_api_running(context.jobs_api_url + _JOBS_DEBUG_API +
                           "/analyses-report?ecosystem=maven")


def _is_component_search_service_running(context):
    return _is_api_running(context.coreapi_url + _API_ENDPOINT +
                           "/component-search/any-component")


def _read_boolean_setting(context, setting_name):
    setting = context.config.userdata.get(setting_name, '').lower()
    if setting in ('1', 'yes', 'true', 'on'):
        return True
    if setting in ('', '0', 'no', 'false', 'off'):
        return False
    msg = '{!r} is not a valid option for boolean setting {!r}'
    raise ValueError(msg.format(setting, setting_name))


def _add_slash(url):
    if url and not url.endswith('/'):
        url += '/'
    return url


def _get_api_url(context, attribute, port):
    return _add_slash(context.config.userdata.get(attribute,
                      'http://localhost:{port}/'.format(port=port)))


def _send_json_file(endpoint, filename):
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    with open(filename) as json_data:
        response = requests.post(endpoint, data=json_data, headers=headers)
    return response


def _parse_int_env_var(env_var_name):
    val = os.environ.get(env_var_name)
    try:
        return int(val)
    except (TypeError, ValueError):
        return None


def before_all(context):
    context.config.setup_logging()
    context.start_system = _start_system
    context.teardown_system = _teardown_system
    context.restart_system = _restart_system
    context.run_command_in_service = _run_command_in_service
    context.exec_command_in_container = _exec_command_in_container
    context.is_running = _is_running
    context.is_jobs_debug_api_running = _is_jobs_debug_api_running
    context.is_component_search_service_running = _is_component_search_service_running
    context.send_json_file = _send_json_file
    context.wait_for_jobs_debug_api_service = _wait_for_jobs_debug_api_service
    context.wait_for_component_search_service = _wait_for_component_search_service

    # Configure container logging
    context.dump_logs = _read_boolean_setting(context, 'dump_logs')
    tail_logs = int(context.config.userdata.get('tail_logs', 0))
    dump_errors = _read_boolean_setting(context, 'dump_errors')
    if tail_logs:
        dump_errors = True
    else:
        tail_logs = 50
    context.dump_errors = dump_errors
    context.tail_logs = tail_logs

    # Configure system under test
    context.kubernetes_dir_path = context.config.userdata.get('kubernetes_dir', None)
    if context.kubernetes_dir_path is not None:
        context.docker_compose_path = None
    else:
        # If we're not running Kubernetes, use the local Docker Compose setup
        _set_default_compose_path(context)
    # for now, we just assume we know what compose file looks like (what services need what images)
    context.images = {}
    context.images['bayesian/bayesian-api'] = context.config.userdata.get(
        'coreapi_server_image',
        'registry.devshift.net/bayesian/bayesian-api')
    context.images['bayesian/cucos-worker'] = context.config.userdata.get(
        'coreapi_worker_image',
        'registry.devshift.net/bayesian/cucos-worker')

    coreapi_url = _add_slash(os.environ.get('F8A_API_URL', None))
    jobs_api_url = _add_slash(os.environ.get('F8A_JOB_API_URL', None))
    anitya_url = _add_slash(os.environ.get('F8A_ANITYA_API_URL', None))

    context.running_locally = not (coreapi_url and jobs_api_url and anitya_url)

    context.coreapi_url = coreapi_url or _get_api_url(context, 'coreapi_url', _FABRIC8_ANALYTICS_SERVER)
    context.jobs_api_url = jobs_api_url or _get_api_url(context, 'jobs_api_url', _FABRIC8_ANALYTICS_JOBS)
    context.anitya_url = anitya_url or _get_api_url(context, 'anitya_url', _ANITYA_SERVICE)

    context.client = None

    # timeout values can be overwritten by environment variables
    stack_analysis_timeout = _parse_int_env_var('F8A_STACK_ANALYSIS_TIMEOUT')
    component_analysis_timeout = _parse_int_env_var('F8A_COMPONENT_ANALYSIS_TIMEOUT')

    context.stack_analysis_timeout = stack_analysis_timeout or _DEFAULT_STACK_ANALYSIS_TIMEOUT
    context.component_analysis_timeout = component_analysis_timeout or _DEFAULT_COMPONENT_ANALYSIS_TIMEOUT

    if context.running_locally:
        context.client = docker.AutoVersionClient()

        for desired, actual in context.images.items():
            desired = 'registry.devshift.net/' + desired
            if desired != actual:
                context.client.tag(actual, desired, force=True)

    # Specify the analyses checked for when looking for "complete" results
    def _get_expected_component_analyses(ecosystem):
        common = context.EXPECTED_COMPONENT_ANALYSES
        specific = context.ECOSYSTEM_DEPENDENT_ANALYSES.get(ecosystem, set())
        return common | specific
    context.get_expected_component_analyses = _get_expected_component_analyses

    def _compare_analysis_sets(actual, expected):
        unreliable = context.UNRELIABLE_ANALYSES
        missing = expected - actual - unreliable
        unexpected = actual - expected - unreliable
        return missing, unexpected
    context.compare_analysis_sets = _compare_analysis_sets

    context.EXPECTED_COMPONENT_ANALYSES = {
        'metadata', 'source_licenses',
        'digests', 'redhat_downstream',
        'dependency_snapshot', 'code_metrics'
        # The follower workers are currently disabled by default:
        # 'static_analysis', 'binary_data', 'languages', 'crypto_algorithms'
    }
    # Analyses that are only executed for particular language ecosystems
    context.ECOSYSTEM_DEPENDENT_ANALYSES = {
        "maven": {'blackduck'},
        "npm": {'blackduck'},
    }
    # Results that use a nonstandard format, so we don't check for the
    # standard "status", "summary", and "details" keys
    context.NONSTANDARD_ANALYSIS_FORMATS = set()
    # Analyses that are just plain unreliable and so need to be excluded from
    # consideration when determining whether or not an analysis is complete
    context.UNRELIABLE_ANALYSES = {
        'blackduck',
        'github_details',  # if no github api token provided
        'security_issues'  # needs Snyk vulndb in S3
    }


@capture
def before_scenario(context, scenario):
    context.resource_manager = contextlib.ExitStack()


@capture
def after_scenario(context, scenario):
    if context.running_locally:
        if context.dump_logs or context.dump_errors and scenario.status == "failed":
            try:
                _dump_server_logs(context, int(context.tail_logs))
            except subprocess.CalledProcessError as e:
                raise Exception('Failed to dump server logs. Command "{c}" failed:\n{o}'.
                                format(c=' '.join(e.cmd), o=e.output))

        # Clean up resources (which may destroy some container logs)
        context.resource_manager.close()


@capture
def after_all(context):
    if context.running_locally:
        try:
            _teardown_system(context)
        except subprocess.CalledProcessError as e:
            raise Exception('Failed to teardown system. Command "{c}" failed:\n{o}'.
                            format(c=' '.join(e.cmd), o=e.output))
