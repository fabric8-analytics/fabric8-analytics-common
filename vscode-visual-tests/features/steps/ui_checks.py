"""UI-based test steps that are not tied to any specific UI program."""

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

from behave import then, when
from src.gui import perform_click_on_the_region, perform_right_click_on_the_region
from src.gui import perform_find_the_region


@when('I press Enter')
def press_enter(context):
    """Press the Enter."""
    assert context is not None
    context.pyautogui.press('enter')


@when('I press Ctrl+W')
def press_ctrl_w(context):
    """Press the Ctrl+W."""
    assert context is not None
    context.pyautogui.hotkey('ctrl', 'w')


@when('I look at the whole screen')
def look_at_the_whole_screen(context):
    """Create the screenshot of the whole screen."""
    assert context is not None
    screenshot = context.pyautogui.screenshot()
    assert screenshot is not None, "Unable to create screenshot"
    context.screenshot = screenshot


@when('I click on the region')
@when('I click on that region')
def click_on_the_region(context):
    """Click on region found by previous test step."""
    assert context is not None
    perform_click_on_the_region(context)


@when('I right click on the region')
@when('I right click on that region')
def right_click_on_the_region(context):
    """Click on region found by previous test step."""
    assert context is not None
    perform_right_click_on_the_region(context)


@then('I should find the region with {region}')
def find_the_region(context, region):
    """Try to find region on screen based on specified pattern."""
    assert context is not None
    assert region is not None
    perform_find_the_region(context, region)
