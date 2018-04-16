"""Unsorted utility functions used in integration tests."""
import os
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


def is_exe(fpath):
    """Check if the given file is executable."""
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def which(program):
    """Implement a basic form of 'which' utility."""
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def oc_login(url, username, password, tls_verify=True):
    """Wrap `oc login` command.

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
        e.cmd = [x.replace(password, '***') for x in e.cmd]
        raise e


def oc_delete_pods(selector, namespace=None):
    """Wrap `oc delete` command.

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


def oc_run_command(*args):
    """Run any command via the OpenShift Console.

    :return: The command output on success, raises `subprocess.CalledProcessError` on error
    """
    command = ['oc']
    command.extend(args)

    return subprocess.check_output(command)
