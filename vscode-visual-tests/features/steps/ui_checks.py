"""UI-based test steps not tied to any specific UI program."""

from behave import then, when
from src.gui import perform_click_on_the_region, perform_find_the_region


@when('I look at the whole screen')
def look_at_the_whole_screen(context):
    """Create the screenshot of the whole screen."""
    screenshot = context.pyautogui.screenshot()
    assert screenshot is not None, "Unable to create screenshot"
    context.screenshot = screenshot


@when('I click on the region')
@when('I click on that region')
def click_on_the_region(context):
    """Click on region found by previous test step."""
    perform_click_on_the_region(context)


@then('I should find the region with {region}')
def find_the_region(context, region):
    """Try to find region on screen based on specified pattern."""
    assert region is not None
    perform_find_the_region(context, region)
