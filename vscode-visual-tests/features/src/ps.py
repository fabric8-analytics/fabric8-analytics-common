"""Implementation of process list command."""

import subprocess


def get_process_list():
    """Get list of all processes."""
    out = subprocess.Popen(['ps', '-e', '-o', 'command'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    # interact with the process:
    # read data from stdout and stderr, until end-of-file is reached
    stdout, stderr = out.communicate()

    assert stderr is None, "Error during 'ps'"
    assert stdout is not None, "No output from 'ps'"

    # try to decode the output and split it by lines
    ps_output = stdout.decode('utf-8').split()

    return ps_output
