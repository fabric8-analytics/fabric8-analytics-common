"""Visual Studio Code-related test steps."""

from time import sleep
from behave import given, then, when
from src.gui import perform_click_on_the_region, perform_find_the_region, perform_type
from src.gui import perform_move_mouse_cursor


@when('I click on the File menu')
def click_on_the_file_menu(context):
    """Click on the File menu."""
    perform_find_the_region(context, "file menu header")
    perform_click_on_the_region(context)


@when('I move mouse cursor to the top left corner')
def move_mouse_cursor(context):
    """Move mouse cursor to the top left corner."""
    perform_move_mouse_cursor(context, 10, 10)


@when('I click on the Exit menu entry')
def click_on_the_exit_menu_entry(context):
    """Click on the Exit menu entry in File menu."""
    perform_find_the_region(context, "file menu exit")
    perform_click_on_the_region(context)


@then('I should find the activity bar')
def look_for_activity_bar(context):
    """Try to find the activity bar."""
    perform_find_the_region(context, "activity bar", "activity bar 2")


@then('I should find the extension icon on the activity bar')
def look_for_extension_icon_on_activity_bar(context):
    """Try to find the extension icon on activity bar."""
    perform_find_the_region(context, "extensions icon")


@then('I should find the Search extension in Marketplace input box')
def look_for_search_extension_in_marketplace(context):
    """Try to find the Marketplace input box."""
    perform_find_the_region(context, "search extension in marketplace")


@then('I should find the Dependency Analytics info region')
def look_for_dependency_analytics_info_region(context):
    """Try to find the Dependency Analytics info region."""
    perform_find_the_region(context, "dependency analytics info region 0 11")


@then('I should find the OpenShift logo')
def look_for_openshift_logo(context):
    """Try to find the OpenShift logo."""
    perform_find_the_region(context, "openshift logo")


@then('I should find the Dependency Analytics header')
def look_for_dependency_analytics_header(context):
    """Try to find the Dependency Analytics header."""
    perform_find_the_region(context, "dependency analytics header")


@then('I should find the Dependency Analytics title')
def look_for_dependency_analytics_title(context):
    """Try to find the Dependency Analytics title."""
    perform_find_the_region(context, "dependency analytics title")


@then('I should find the Plugin install button')
def look_for_plugin_install_button(context):
    """Try to find the Install button for a selected plugin."""
    perform_find_the_region(context, "plugin install button")


@then('I should find the Reload and Uninstall buttons')
def look_for_plugin_reload_and_uninstall_button(context):
    """Try to find the Reload and Unistall buttons for a selected plugin."""
    perform_find_the_region(context, "reload uninstall buttons")


@then('I should find the Reload button and Gear icon')
def look_for_plugin_reload_button_and_gear_icon(context):
    """Try to find the Reload button with Gear icon for a selected plugin."""
    perform_find_the_region(context, "reload gear")


@when('I type in {what}')
def type_in_text(context, what):
    """Type anything onto the screen."""
    perform_type(context, what)


@when('I click on the extension icon on the activity bar')
def click_on_the_extension_icon_on_the_activity_bar(context):
    """Try to click on the extensino icon on the activity bar."""
    look_for_activity_bar(context)
    look_for_extension_icon_on_activity_bar(context)
    perform_click_on_the_region(context)
    click_on_the_extension_icon_on_the_activity_bar
    sleep(2)


@when('I close the Visual Studio Code')
def close_visual_studio_code(context):
    """Try close the Visual Studio Code."""
    click_on_the_file_menu(context)
    click_on_the_exit_menu_entry(context)
    sleep(2)


@when('I search for {plugin} plugin')
def search_for_plugin(context, plugin):
    """Search for plugin."""
    look_for_search_extension_in_marketplace(context)
    type_in_text(context, plugin)
    sleep(2)
    look_for_dependency_analytics_info_region(context)


@when('I select the plugin')
def select_plugin(context):
    """Select the plugin to install."""
    perform_click_on_the_region(context)
    # time to find the plugin
    sleep(2)
    look_for_plugin_install_button(context)


@when('I start the installation by clicking on the Plugin install button')
def start_extension_installation(context):
    """Start the VS code extension installation."""
    perform_click_on_the_region(context)
    perform_move_mouse_cursor(context, 10, 10)
    sleep(2)
