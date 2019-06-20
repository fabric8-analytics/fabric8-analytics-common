"""Visual Studio Code-related test steps."""

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

from time import sleep
from behave import then, when
from src.gui import perform_click_on_the_region, perform_find_the_region, perform_type
from src.gui import perform_move_mouse_cursor

SLEEP_AMOUNT = 2


@when('I click on the File menu')
def click_on_the_file_menu(context):
    """Click on the File menu."""
    assert context is not None
    perform_find_the_region(context, "file menu header")
    perform_click_on_the_region(context)


@when('I move mouse cursor to the top left corner')
def move_mouse_cursor(context):
    """Move mouse cursor to the top left corner."""
    assert context is not None
    # don't use [0, 0] as it is special area for the PyAutoGUI library
    perform_move_mouse_cursor(context, 10, 10)


@when('I click on the Exit menu entry')
def click_on_the_exit_menu_entry(context):
    """Click on the Exit menu entry in File menu."""
    assert context is not None
    perform_find_the_region(context, "file menu exit")
    perform_click_on_the_region(context)


@then('I should find the activity bar')
def look_for_activity_bar(context):
    """Try to find the activity bar."""
    assert context is not None
    perform_find_the_region(context, "activity bar", "activity bar 2")


@then('I should find the extension icon on the activity bar')
def look_for_extension_icon_on_activity_bar(context):
    """Try to find the extension icon on activity bar."""
    assert context is not None
    perform_find_the_region(context, "extensions icon")


@then('I should find the Search extension in Marketplace input box')
def look_for_search_extension_in_marketplace(context):
    """Try to find the Marketplace input box."""
    assert context is not None
    perform_find_the_region(context, "search extension in marketplace")


@then('I should find the Dependency Analytics info region')
def look_for_dependency_analytics_info_region(context):
    """Try to find the Dependency Analytics info region."""
    assert context is not None
    perform_find_the_region(context, "dependency analytics info region")
    perform_find_the_region(context, "dependency analytics info region 0 12")


@then('I should find the OpenShift logo')
def look_for_openshift_logo(context):
    """Try to find the OpenShift logo."""
    assert context is not None
    perform_find_the_region(context, "openshift logo", "openshift logo 2")


@then('I should find Analytics page with {header} header')
def look_for_analytics_page_with_specified_header(context, header):
    """Try to find specified header on the Analytics page."""
    assert context is not None
    assert header is not None
    region = "analysis_security_{}_header".format(header.lower())
    perform_find_the_region(context, region)


@then('I should find the Dependency Analytics header')
def look_for_dependency_analytics_header(context):
    """Try to find the Dependency Analytics header."""
    assert context is not None
    perform_find_the_region(context, "dependency analytics header")


@then('I should find the Dependency Analytics title')
def look_for_dependency_analytics_title(context):
    """Try to find the Dependency Analytics title."""
    assert context is not None
    perform_find_the_region(context, "dependency analytics title")


@then('I should find the Plugin install button')
def look_for_plugin_install_button(context):
    """Try to find the Install button for a selected plugin."""
    assert context is not None
    perform_find_the_region(context, "plugin install button", "plugin install button 2")


@then(u'I should find the Plugin uninstall button')
def look_for_plugin_uninstall_button(context):
    """Try to find the Unistall button for a selected plugin."""
    assert context is not None
    perform_find_the_region(context, "plugin uninstall button", "plugin uninstall button 2")


@then('I should find the Uninstalled label')
def look_for_uninstalled_label(context):
    """Try to find the Uninstalled label."""
    assert context is not None
    perform_find_the_region(context, "uninstalled label")


@then('I should find the Reload and Uninstall buttons')
def look_for_plugin_reload_and_uninstall_button(context):
    """Try to find the Reload and Unistall buttons for a selected plugin."""
    assert context is not None
    perform_find_the_region(context, "reload uninstall buttons")


@then('I should find the Reload button and Gear icon')
def look_for_plugin_reload_button_and_gear_icon(context):
    """Try to find the Reload button with Gear icon for a selected plugin."""
    assert context is not None
    perform_find_the_region(context, "reload gear")


@then('I should find the Installed icon and Gear button')
def look_for_plugin_installed_icon_and_gear_button(context):
    """Try to find the Install icon and a Gear icon for a selected plugin."""
    assert context is not None
    perform_find_the_region(context, "installed icon and gear button")


@then('I should find the Installed icon and Uninstall button')
def look_for_plugin_install_icon_and_uninstall_button(context):
    """Try to find the Install icon and a Uninstall icon for a selected plugin."""
    assert context is not None
    perform_find_the_region(context, "installed icon and uninstall button")


@then('I should find the Dependency Analysis Report menu entry in context menu')
def look_for_dependency_analysis_report_menu_entry_context_menu(context):
    """Try to find the Dependency Analysis Report menu entry in context menu."""
    assert context is not None
    perform_find_the_region(context, "context menu dependency analytics entry")


@then('I should find the empty window or Welcome tab')
def look_for_empty_window_or_welcome_tab(context):
    """Try to find the Welcome tab displayed after all editor tabs are closed."""
    assert context is not None
    perform_find_the_region(context, "welcome tab", "empty window")


@then('I should find the icon with info about zero problems in the status bar')
def look_for_icon_with_info_about_zero_problems(context):
    """Try to find the icon that informed users about zero problems."""
    assert context is not None
    perform_find_the_region(context, "zero problems")


@then('I should find the icon with info about one problem found in the status bar')
def look_for_icon_with_info_about_one_problem(context):
    """Try to find the icon that informed users about one problem."""
    assert context is not None
    perform_find_the_region(context, "one problem")


@then('I should find the icon with info about {number} problems found in the status bar')
def look_for_icon_with_info_about_more_problems(context, number):
    """Try to find the icon that informed users about more problems."""
    assert context is not None
    perform_find_the_region(context, number + " problems")


@when('I type in {what}')
def type_in_text(context, what):
    """Type anything onto the screen."""
    assert context is not None
    perform_type(context, what)


@when('I click on the extension icon on the activity bar')
def click_on_the_extension_icon_on_the_activity_bar(context):
    """Try to click on the extensino icon on the activity bar."""
    assert context is not None
    look_for_activity_bar(context)
    look_for_extension_icon_on_activity_bar(context)
    perform_click_on_the_region(context)
    click_on_the_extension_icon_on_the_activity_bar
    sleep(SLEEP_AMOUNT)


@when('I close the Visual Studio Code')
def close_visual_studio_code(context):
    """Try close the Visual Studio Code."""
    assert context is not None
    click_on_the_file_menu(context)
    click_on_the_exit_menu_entry(context)
    sleep(SLEEP_AMOUNT)


@when('I search for {plugin} plugin')
def search_for_plugin(context, plugin):
    """Search for plugin."""
    assert context is not None
    look_for_search_extension_in_marketplace(context)
    type_in_text(context, plugin)
    sleep(SLEEP_AMOUNT)
    look_for_dependency_analytics_info_region(context)


@when('I select the plugin')
def select_plugin(context):
    """Select the plugin to install."""
    assert context is not None
    perform_click_on_the_region(context)
    # time to find the plugin
    sleep(SLEEP_AMOUNT)
    look_for_plugin_install_button(context)


@when('I start the installation by clicking on the Plugin install button')
def start_extension_installation(context):
    """Start the VS code extension installation."""
    assert context is not None
    perform_click_on_the_region(context)
    perform_move_mouse_cursor(context, 10, 10)
    sleep(SLEEP_AMOUNT)
