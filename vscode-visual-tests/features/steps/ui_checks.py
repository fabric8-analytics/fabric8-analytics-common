"""UI-based test steps not tied to any specific UI program."""

from behave import then, when


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
    location = context.location
    assert location is not None, "Region can not be found"
    x, y = context.pyautogui.center(location)
    context.pyautogui.click(x, y)


def filename_for_region(region):
    """Proper filename for file containing pattern for region."""
    region = region.replace(" ", "_")
    filename = "regions/" + region + ".png"
    return filename


@then('I should find the region with {region}')
def find_the_region(context, region):
    """Try to find region on screen based on specified pattern."""
    location = context.pyautogui.locateOnScreen(filename_for_region(region))
    assert location is not None, "Region can not be found"
    context.location = location
