# vim: set fileencoding=utf-8

"""Interface to the Litava tool."""

import subprocess


def get_int_metrics(line):
    """Retrieve the integer metrics."""
    return int(line.split(" ")[1])


def get_string_metrics(line):
    """Retrieve the string metrics."""
    return line.split(" ")[1].strip()


def parse_litava_output(output):
    """Parse output from the Litava tool."""
    x = None
    y = None
    w = None
    h = None
    result = None

    for line in output:
        if line.startswith("x:"):
            x = get_int_metrics(line)
        elif line.startswith("y:"):
            y = get_int_metrics(line)
        elif line.startswith("w:"):
            w = get_int_metrics(line)
        elif line.startswith("h:"):
            h = get_int_metrics(line)
        elif line.startswith("Result: "):
            result = get_string_metrics(line)

    return x, y, w, h, result


def check_location(x, y):
    """Check location of a pattern."""
    assert x is not None, "x coordinate of a pattern must be set"
    assert x >= 0, "x coordinate must be positive number"
    assert y is not None, "y coordinate of a pattern must be set"
    assert y >= 0, "x coordinate must be positive number"


def check_size(w, h):
    """Check size of a pattern."""
    assert w is not None, "width of a pattern must be set"
    assert w > 0, "width must be greater than zero"
    assert h is not None, "height of a pattern must be set"
    assert h > 0, "height must be greater than zero"


def check_result(result):
    """Check the status/result produced y Litava."""
    assert result is not None, "result needs to be provided"
    assert result == "found", "pattern should be found in an image"


def decode_litava_output(output):
    """Decode and check output from the Litava tool."""
    x, y, w, h, result = parse_litava_output(output)
    check_location(x, y)
    check_size(w, h)
    check_result(result)

    # this is expected output - a tuple of (x, y, width, height)
    return (x, y, w, h)


def locate_on_screen_using_litava(screenshot, pattern):
    """Try to locate pattern on screen using the Litava tool."""
    out = subprocess.Popen(['./litava', screenshot, pattern, "output.bmp"],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    # interact with the process:
    # read data from stdout and stderr, until end-of-file is reached
    stdout, stderr = out.communicate()

    # basic checks
    assert stderr is None, "Error during check"
    assert stdout is not None, "No output from litava"

    assert out.returncode == 0 or out.returncode == 1

    output = stdout.decode('utf-8').split("\n")
    assert output is not None
    return decode_litava_output(output)
