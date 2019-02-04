"""Implementation of common test steps."""

# vim: set fileencoding=utf-8

#
#  (C) Copyright 2019  Pavel Tisnovsky
#
#  All rights reserved. This program and the accompanying materials
#  are made available under the terms of the Eclipse Public License v1.0
#  which accompanies this distribution, and is available at
#  http://www.eclipse.org/legal/epl-v10.html
#
#  Contributors:
#      Pavel Tisnovsky
#

from behave import given, then, when
from time import sleep
from os import system
import subprocess


@given('The PyAutoGUI library is initialized')
def initial_initialize_autogui_library(context):
    """Initialize PyAutoGUI library and check display etc."""
    import pyautogui
    pyautogui.PAUSE = 1.0
    context.pyautogui = pyautogui


@given('The screen resolution is at least {width:d}x{height:d} pixels')
def check_screen_size(context, width, height):
    """Check the screen size, because the UI layout depends on it."""
    actual_width, actual_height = context.pyautogui.size()
    assert actual_width >= width, "Insuficient width {w}".format(w=actual_width)
    assert actual_height >= height, "Insuficient height {h}".format(h=actual_height)


@when('I start the Visual Studio Code')
def start_visual_studion_code(context):
    """Start the Visual Studio Code."""
    system("code")
    # time to breath
    sleep(2)


@then('I should find Visual Studio Code instance')
def visual_studio_code_instance(context):
    """Check that the Visual Studio Code has been started."""
    out = subprocess.Popen(['ps', '-e', '-o', 'command'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()

    assert stderr is None, "Error during 'ps'"
    assert stdout is not None, "No output from 'ps'"

    ps_output = stdout.decode('utf-8').split()
    for line in ps_output:
        if line.startswith("/usr/share/code"):
            return

    raise Exception("Visual Studio Code is not running")


@then('I should not find any Visual Studio Code instance')
def no_visual_studio_code_instance(context):
    """Check that the Visual Studio Code has not been started."""
    pass
