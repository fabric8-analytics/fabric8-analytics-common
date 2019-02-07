"""Common functions for GUI-related tests."""

TYPING_INTERVAL = 0.25


def perform_click_on_the_region(context):
    """Click on region found by previous test step."""
    assert context is not None, "Context must be provided by Behave"

    # get the already found location
    location = context.location
    assert location is not None, "Region can not be found"

    # click on the center of location
    x, y = context.pyautogui.center(location)
    context.pyautogui.click(x, y)


def perform_type(context, what_to_type):
    """Type anything onto the screen."""
    context.pyautogui.typewrite(what_to_type, interval=TYPING_INTERVAL)


def filename_for_region(region):
    """Proper filename for file containing pattern for region."""
    assert region is not None, "Name of region is required parameter"

    region = region.replace(" ", "_")
    filename = "regions/" + region + ".png"
    return filename


def save_screenshot(context, region):
    """Save screenshot with the filename the same as the region."""
    assert region is not None, "Name of region is required parameter"

    context.pyautogui.screenshot(region.replace(" ", "_") + ".png")


def perform_find_the_region(context, region, alternate_region=None):
    """Try to find region on screen based on specified pattern."""
    try:
        # first step - try to localize primary region
        location = context.pyautogui.locateOnScreen(filename_for_region(region))
    except Exception:
        # the primary region can't be found: try the alternate region, if any
        if alternate_region is not None:
            try:
                location = context.pyautogui.locateOnScreen(filename_for_region(alternate_region))
            except Exception:
                save_screenshot(context, alternate_region)
                raise Exception("Alternate region '{r}' can not be found".format(r=region))
        # first region can't be found and alternate region is not specified -> a problem
        else:
            save_screenshot(context, region)
            raise Exception("Primary region '{r}' can not be found".format(r=region))

    context.location = location
