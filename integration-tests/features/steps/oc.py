"""Test steps that access OC client."""

from behave import given, then, when

from src.utils import *
from src.attribute_checks import *

from subprocess import CalledProcessError
import json
import re


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
    except (CalledProcessError, FileNotFoundError) as e:
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
    regexp = r"[A-Za-z0-9]+"
    name = lines[0].decode("utf-8")
    assert re.fullmatch(regexp, name)


@when(u'I ask for statuses of all deployments')
def check_status_of_all_deployments(context):
    """Run the 'oc' command to retrieve statuses of all deployments."""
    try:
        result = oc_run_command("get", "dc", "--output", "json")
        context.oc_result = json.loads(result)
    except (CalledProcessError, FileNotFoundError) as e:
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
    except (CalledProcessError, FileNotFoundError) as e:
        # nothing we can do ATM
        raise


@then(u'I should find that the service {service_name} exists')
def oc_service_exist(context, service_name):
    """Check the existence of service."""
    metadata = check_and_get_attribute(context.oc_result, "metadata")
    name = check_and_get_attribute(metadata, "name")
    assert name == service_name, "Returned service has wrong name {name}".format(name=name)


@when(u'I delete all pods for the service {service_name}')
def oc_delete_selected_pods(context, service_name):
    """Delete selected pods."""
    oc_delete_pods(service=service_name)
