"""Environment settings for VSCode visual tests."""

import os
import subprocess


def use_litava():
    """Check whether user specified the USE_LITAVA environment variable."""
    v = os.environ.get("USE_LITAVA", "").strip().lower()
    return v in {"yes", "1", "true", "y"}


def check_file_existence(filename):
    """Check whether the specified file exists."""
    assert filename is not None, "File to check is not specified"
    assert os.path.exists(filename), "The file {} does not exist".format(filename)


def check_litava_output(output, version, executable):
    """Check if Litava respond with expected output 'Litava version X.Y'."""
    assert output[0] == "Litava", "Unexpected output from '{}'".format(executable)
    assert output[1] == "version", "Unexpected output from '{}'".format(executable)
    assert output[2] == version, "Unexpected version '{}'".format(output[2])


def check_litava_version(executable, version):
    """Try to read Litava version."""
    out = subprocess.Popen([executable, "--version"],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    # interact with the process:
    # read data from stdout and stderr, until end-of-file is reached
    stdout, stderr = out.communicate()

    # basic checks
    assert stderr is None, "Error during '{}'".format(executable)
    assert stdout is not None, "No output from '{}'".format(executable)

    # try to decode the output and split it by lines
    output = stdout.decode('utf-8').split()
    assert output is not None

    check_litava_output(output, version, executable)


def before_all(context):
    """Perform basic setup."""
    context.time_for_analysis_to_finish = 5
    context.time_for_detailed_analysis_to_finish = 25
    context.time_for_text_editor_to_open = 2
    context.time_for_text_editor_to_close = 2
    context.time_for_vscode_to_close = 2
    context.time_for_context_menu = 2
    context.use_litava = use_litava()
    if context.use_litava:
        check_file_existence("./litava")
        check_litava_version("./litava", "1.0")


def after_all(context):
    """Perform basic cleanup."""
    pass
