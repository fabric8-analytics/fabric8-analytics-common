"""Test steps that access OC client."""

from behave import given, then, when

from src.utils import which, oc_run_command, oc_delete_pods
from src.attribute_checks import check_and_get_attribute

from subprocess import CalledProcessError
import json
import re
import time


@given(u'The OpenShift Client is installed')
def check_oc_command(context):
    """Check if 'oc' command is available for the current user."""
    assert which("oc"), "The 'oc' command is not found. " +\
        "Have you installed the OpenShift Console tool?"


@when(u'I run OC command to show information about the current session')
def oc_show_status(context):
    """Run the 'oc whoami' and check the exit code."""
    try:
        context.oc_result = oc_run_command("whoami")
    except (CalledProcessError, FileNotFoundError):
        # nothing we can do ATM
        raise


@then(u'I should get the user name')
def oc_got_user_name_p(context):
    """Check if the command 'oc whoami' returned (possibly valid) user name."""
    # check if at least any result exists
    assert context.oc_result, "'oc' command did not return any result"

    # check if we got one line output only
    lines = context.oc_result.split()
    assert len(lines) == 1, "Expected one line output"

    # check the user name
    regexp = r"[A-Za-z0-9:-]+"
    name = lines[0].decode("utf-8")
    assert re.fullmatch(regexp, name)


@when(u'I ask for states of all deployments')
def check_status_of_all_deployments(context):
    """Run the 'oc' command to retrieve states of all deployments."""
    try:
        result = oc_run_command("get", "deploymentconfigs", "--output", "json")
        context.oc_result = json.loads(result)
    except (CalledProcessError, FileNotFoundError):
        # nothing we can do ATM
        raise


@then(u'I should find that the deployment {deployment_name} exists')
def oc_deployment_exist(context, deployment_name):
    """Check if the given deployment exists and is visible for logged in user."""
    deployments = check_and_get_attribute(context.oc_result, "items")
    for deployment in deployments:
        metadata = check_and_get_attribute(deployment, "metadata")
        name = check_and_get_attribute(metadata, "name")
        if name == deployment_name:
            return
    raise Exception("Deployment {d} could not be found".format(d=deployment_name))


@when(u'I ask for status of the {service} service')
def check_status_of_service(context, service):
    """Run the 'oc' command to retrieve status of selected service."""
    try:
        result = oc_run_command("get", "service", service, "--output", "json")
        context.oc_result = json.loads(result)
    except (CalledProcessError, FileNotFoundError):
        # nothing we can do ATM
        raise


@then(u'I should find that the service {service_name} exists')
def oc_service_exist(context, service_name):
    """Check the existence of service."""
    metadata = check_and_get_attribute(context.oc_result, "metadata")
    name = check_and_get_attribute(metadata, "name")
    assert name == service_name, "Returned service has wrong name {name}".format(name=name)


def selector_for_service(service_name):
    """Construct selector for a service (or any other label)."""
    return "service={service_name}".format(service_name=service_name)


@when(u'I delete all pods for the service {service_name}')
def oc_delete_selected_pods(context, service_name):
    """Delete selected pods."""
    selector = selector_for_service(service_name)
    oc_delete_pods(selector, force=True)


@when(u'I get all pods for the {service_name} service')
def oc_get_pods_for_service(context, service_name):
    """Get all pods for the service."""
    selector = selector_for_service(service_name)
    try:
        result = oc_run_command("get", "pods", "--selector", selector, "--output", "json")
        context.oc_result = json.loads(result)
    except (CalledProcessError, FileNotFoundError):
        # nothing we can do ATM
        raise


@then(u'I should find at least {num:n} pod')
@then(u'I should find at least {num:n} pods')
def oc_number_of_pods(context, num):
    """Check if at least specified number of pods exists for the given service."""
    pods = check_and_get_attribute(context.oc_result, "items")
    cnt = len(pods)
    assert cnt >= num, "Wrong number of pods ({cnt}) has been found".format(cnt=cnt)


def get_pod_phase(pod):
    """Get the current phase of pod from JSON data returned by OpenShift client."""
    status = check_and_get_attribute(pod, "status")
    return check_and_get_attribute(status, "phase")


def is_pod(pod):
    """Check whether the data describes Pod or something else."""
    kind = check_and_get_attribute(pod, "kind")
    return kind == "Pod"


def get_pod_states(context):
    """Get states for all pods."""
    states = {}
    pods = check_and_get_attribute(context.oc_result, "items")
    for pod in pods:
        if is_pod(pod):
            metadata = check_and_get_attribute(pod, "metadata")
            name = check_and_get_attribute(metadata, "name")
            phase = get_pod_phase(pod)
            states[name] = phase
    return states


@then(u'I should find that all pods are in the {expected} state')
def oc_pods_in_state(context, expected):
    """Check state for all pods for the given service."""
    states = get_pod_states(context)
    for pod_name, pod_state in states.items():
        assert pod_state == expected, ("Pod {name} should be in state {expected}, but it is in " +
                                       "state {pod_state} instead.").format(name=pod_name,
                                                                            expected=expected,
                                                                            pod_state=pod_state)


@then(u'I should find that none of pods are in the {state} state')
def oc_pods_in_state_negative(context, state):
    """Check state for all pods for the given service."""
    states = get_pod_states(context)
    for pod_name, pod_state in states.items():
        assert pod_state != state, "Pod {name} is in wrong state {state}".format(name=pod_name,
                                                                                 state=pod_state)


@when(u'I wait for the service {service_name} to restart with timeout set to {timeout:d} minutes')
def oc_wait_for_service_restart(context, service_name, timeout):
    """Try to wait for the service to be restarted."""
    timeout *= 60  # minutes
    sleep_amount = 2
    for _ in range(timeout // sleep_amount):
        oc_get_pods_for_service(context, service_name)
        states = get_pod_states(context)
        for pod_name, status in states.items():
            if status == "Running":
                # pod has been started
                return
        time.sleep(sleep_amount)
    else:
        raise Exception("Timeout waiting for service {service} to restart".format(
            service=service_name))
