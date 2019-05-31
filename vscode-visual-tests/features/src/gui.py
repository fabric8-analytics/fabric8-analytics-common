# vim: set fileencoding=utf-8

"""Common functions for GUI-related tests."""

from os import path


TYPING_INTERVAL = 0.25
DIRECTORY_WITH_REGIONS = "regions"
OUTPUT_DIRECTORY = "."


def perform_move_mouse_cursor(context, x=0, y=0):
    """Move mouse cursor to specifief coordinates."""
    assert context is not None, "Context must be provided by Behave"
    context.pyautogui.moveTo(x, y)


def check_location_existence(location):
    """Check if location exist and can be found on the screen."""
    assert location is not None, "Region can not be found"


def perform_click_on_the_region(context):
    """Click on region found by previous test step."""
    assert context is not None, "Context must be provided by Behave"

    # get the already found location
    location = context.location
    check_location_existence(location)

    # click on the center of location
    x, y = context.pyautogui.center(location)
    context.pyautogui.click(x, y)


def perform_type(context, what_to_type):
    """Type anything onto the screen."""
    context.pyautogui.typewrite(what_to_type, interval=TYPING_INTERVAL)


def region_filename_in_directory(directory, version, region):
    """Generate filename for region residing in specified directory."""
    # construct proper filename
    region = region.replace(" ", "_")
    filename = path.join(directory + "/" + version, region + ".png")
    return filename


def filename_for_region(context, region):
    """Proper filename for file containing pattern for region."""
    assert region is not None, "Name of region is required parameter"

    version = context.vs_code_version

    return region_filename_in_directory(DIRECTORY_WITH_REGIONS, version, region)


def save_screenshot(context, region):
    """Save screenshot with the filename the same as the region."""
    assert region is not None, "Name of region is required parameter"

    version = context.vs_code_version

    filename = region_filename_in_directory(OUTPUT_DIRECTORY, version, region)
    context.pyautogui.screenshot(filename)


def perform_find_the_region(context, region, alternate_region=None):
    """Try to find region on screen based on specified pattern."""
    assert region is not None, "Name of region is required parameter"
    context.location = None

    try:
        # first step - try to localize primary region
        filename = filename_for_region(context, region)
        location = context.pyautogui.locateOnScreen(filename)
        check_location_existence(location)
    except Exception:
        # the primary region can't be found: try the alternate region, if any
        if alternate_region is not None:
            try:
                filename = filename_for_region(context, alternate_region)
                location = context.pyautogui.locateOnScreen(filename)
                assert location is not None
            except Exception:
                save_screenshot(context, alternate_region)
                raise Exception("Alternate region '{r}' can not be found on the screen".format(
                                r=region))
        # first region can't be found and alternate region is not specified -> a problem
        else:
            save_screenshot(context, region)
            raise Exception("Primary region '{r}' can not be found on the screen".format(r=region))

    context.location = location
