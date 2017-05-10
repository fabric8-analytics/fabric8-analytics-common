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


def _set_default_compose_path(context):
    base_compose = os.path.join(_REPO_DIR, 'docker-compose.yml')
    # Extra containers are added as needed by integration setup commands
    context.docker_compose_path = [base_compose]

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
    if context.docker_compose:
        cmd = _make_compose_command(context, 'up', '--no-build', '-d')
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)


def _make_compose_teardown_callback(context, services):
    cmds = [
        _make_compose_command(context, 'kill', *services),
        _make_compose_command(context, 'rm', '-fv', *services)
    ]

    def teardown_services():
        for cmd in cmds:
            subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    return teardown_services


def _run_command_in_service(context, service, command):
    """
    run command in specified service via `docker-compose run`; command is list of strs
    """
    if context.docker_compose:
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


def _dump_server_logs(context, tail=None):
    if context.docker_compose:
        cmd = _make_compose_command(context, 'logs')
        if tail is not None:
            cmd.append('--tail={:d}'.format(tail))
        subprocess.check_call(cmd, stderr=subprocess.STDOUT)
    else:
        pass  # No current support for dumping logs under k8s


def _teardown_system(context):
    if context.docker_compose:
        cmds = [
            _make_compose_command(context, 'kill'),
            _make_compose_command(context, 'rm', '-fv')
        ]
        if hasattr(context, "container"):
            cmds.append(['docker', "kill", context.container])
            cmds.append(['docker', "rm", "-fv", "--rm-all", context.container])
        _set_default_compose_path(context)

        for cmd in cmds:
            subprocess.check_output(cmd, stderr=subprocess.STDOUT)


def _wait_for_system(context, wait_for_server=120):
    start = datetime.datetime.now()
    wait_till = start + datetime.timedelta(seconds=wait_for_server)
    # try to wait for server to start for some time
    started_all = False
    while datetime.datetime.now() < wait_till:
        time.sleep(1)
        if _is_running(context):
            started_all = True
            break
    if started_all:
        # let's give the whole system a while to breathe
        time.sleep(float(context.config.userdata.get('breath_time', 10)))
    else:
        raise Exception('Server failed to start in under {s} seconds'.
                        format(s=wait_for_server))


def _restart_system(context, wait_for_server=120):
    try:
        _teardown_system(context)
        _start_system(context)
        _wait_for_system(context, wait_for_server)
    except subprocess.CalledProcessError as e:
        raise Exception('Failed to restart system. Command "{c}" failed:\n{o}'.
                        format(c=' '.join(e.cmd), o=e.output))


def _is_running(context):
    coreapi = False
    anitya = False
    try:
        res = requests.get(context.coreapi_url + 'api/v1/readiness')
        if res.status_code == 200:
            coreapi = True
        res = requests.get(context.anitya_url + 'api/version')
        if res.status_code == 200:
            anitya = True
    except requests.exceptions.ConnectionError:
        pass
    return coreapi and anitya


def _read_boolean_setting(context, setting_name):
    setting = context.config.userdata.get(setting_name, '').lower()
    if setting in ('1', 'yes', 'true', 'on'):
        return True
    if setting in ('', '0', 'no', 'false', 'off'):
        return False
    msg = '{!r} is not a valid option for boolean setting {!r}'
    raise ValueError(msg.format(setting, setting_name))


def _add_slash(url):
    if not url.endswith('/'):
        url += '/'
    return url


def before_all(context):
    context.config.setup_logging()
    context.start_system = _start_system
    context.teardown_system = _teardown_system
    context.restart_system = _restart_system
    context.run_command_in_service = _run_command_in_service
    context.exec_command_in_container = _exec_command_in_container
    context.is_running = _is_running

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

    host = context.config.userdata.get('coreapi_host', 'localhost')
    port = context.config.userdata.get('coreapi_port', '32000')
    context.coreapi_url = "http://{host}:{port}/".format(host=host, port=port)

    host = context.config.userdata.get('anitya_host', 'localhost')
    port = context.config.userdata.get('anitya_port', '31005')
    context.anitya_url = "http://{host}:{port}/".format(host=host, port=port)

    # Configure system under test
    context.docker_compose = not context.config.userdata.get('openshift', False)
    if context.docker_compose:
        # If we're not running OpenShift, use the local Docker Compose setup
        _set_default_compose_path(context)

        # we just assume we know what compose file looks like (what services need what images)
        context.images = {
            'bayesian/bayesian-api': context.config.userdata.get(
                                        'coreapi_server_image',
                                        'docker-registry.usersys.redhat.com/bayesian/bayesian-api'),
            'bayesian/cucos-worker': context.config.userdata.get(
                                        'coreapi_worker_image',
                                        'docker-registry.usersys.redhat.com/bayesian/cucos-worker')
        }

        context.client = docker.AutoVersionClient()
        for desired, actual in context.images.items():
            desired = 'docker-registry.usersys.redhat.com/' + desired
            if desired != actual:
                context.client.tag(actual, desired, force=True)
    else:
        context.docker_compose_path = None

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
    try:
        _teardown_system(context)
    except subprocess.CalledProcessError as e:
        raise Exception('Failed to teardown system. Command "{c}" failed:\n{o}'.
                        format(c=' '.join(e.cmd), o=e.output))
