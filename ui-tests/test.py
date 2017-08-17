from splinter import Browser
import time
import os
from urllib.parse import urljoin


SLEEP_BETWEEN_PAGES = 15
SLEEP_BEFORE_CLICK = 15


def check_env_variable(env_var_name):
    assert os.environ.get(env_var_name), \
        'The environment variable {v} should be set properly'.format(
            v=env_var_name)


def check_setup():
    check_env_variable('TARGET_SERVER')
    check_env_variable('OPENSHIFT_USERNAME')
    check_env_variable('OPENSHIFT_PASSWORD')


def front_page(browser, server):
    '''Go to the Openshift.io front page and click the Login button.'''
    print("Front page")
    url = server
    browser.visit(url)
    time.sleep(SLEEP_BEFORE_CLICK)
    login_button = browser.find_by_css('button#login').first
    assert login_button.visible
    assert login_button.value == 'LOG IN'
    time.sleep(SLEEP_BEFORE_CLICK)
    login_button.click()
    time.sleep(SLEEP_BETWEEN_PAGES)


def login_page(browser, server, username, password):
    '''Login into the Openshift.io using the provided username and
    password.'''
    print("Login page")
    username_input = browser.find_by_id('username').first
    password_input = browser.find_by_id('password').first
    assert username_input.visible
    assert password_input.visible
    browser.fill('username', username)
    browser.fill('password', password)
    login_button = browser.find_by_id('kc-login').first
    assert login_button.visible
    time.sleep(SLEEP_BEFORE_CLICK)
    login_button.click()
    time.sleep(SLEEP_BETWEEN_PAGES)


def run_tests(engine, server, username, password):
    with Browser(engine) as browser:
        front_page(browser, server)
        login_page(browser, server, username, password)


check_setup()
server = os.environ.get('TARGET_SERVER')
username = os.environ.get('OPENSHIFT_USERNAME')
password = os.environ.get('OPENSHIFT_PASSWORD')
engine = os.environ.get('BROWSER_ENGINE', 'chrome')

print("Using the following browser engine {e}".format(e=engine))

run_tests(engine, server, username, password)
