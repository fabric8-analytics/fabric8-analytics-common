"""Unsorted utility functions used in integration tests."""
import requests
import subprocess


def download_file_from_url(url):
    """Download file from the given URL and do basic check of response."""
    assert url
    response = requests.get(url)
    assert response.status_code == 200
    assert response.text is not None
    return response.text


def split_comma_separated_list(l):
    """Split the list into elements separated by commas."""
    return [i.strip() for i in l.split(',')]


def oc_login(url, username, password, tls_verify=True):
    """Wrapper around `oc login`.

    :param url: str, OpenShift URL
    :param username: str, username
    :param password: str, password
    :param tls_verify: bool, verify server's certificate?; default: True
    :return: None on success, raises `subprocess.CalledProcessError` on error
    """
    command = ['oc', 'login', url, '--username', username, '--password', password]
    if not tls_verify:
        command.extend(['--insecure-skip-tls-verify=true'])

    try:
        subprocess.check_call(command)
    except subprocess.CalledProcessError as e:
        # replace password with '***' so somebody will not accidentally leak it in CI logs
        e.cmd = [x if x != password else '***' for x in e.cmd]
        raise e


def oc_delete_pods(selector, namespace=None):
    """Wrapper around `oc delete`.

    Selector determines which pods will be deleted.
    More on selectors:
    https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors

    Note k8s/OpenShift will immediately restart deleted pods,
    to match desired number of replicas for given deployment.

    The expectation is that the user is already logged in
    and has permissions to delete pods.

    Example usage:
    oc_delete_pods('service=bayesian-pgbouncer'

    :param selector: str, selector identifying pods that will be deleted
    :param namespace: str, namespace in which `oc delete` command should be executed,
           default: currently selected namespace
    :return: None on success, raises `subprocess.CalledProcessError` on error
    """
    command = ['oc', 'delete', 'pods', '--selector=', selector]
    if namespace:
        command.extend(['--namespace', namespace])

    subprocess.check_call(command)
