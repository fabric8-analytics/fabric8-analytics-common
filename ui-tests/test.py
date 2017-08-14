from splinter import Browser
import time
import os
from urllib.parse import urljoin


def check_env_variable(env_var_name):
    assert os.environ.get(env_var_name), \
        'The environment variable {v} should be set properly'.format(
            v=env_var_name)


def check_setup():
    check_env_variable('TARGET_SERVER')
    check_env_variable('OPENSHIFT_USERNAME')
    check_env_variable('OPENSHIFT_PASSWORD')


def front_page(browser, server):
    url = server
    browser.visit(url)
    login_button = browser.find_by_css('button#login').first
    assert login_button.visible
    assert login_button.value == 'LOG IN'
    login_button.click()


def run_tests(engine, server, username, password):
    with Browser(engine) as browser:
        front_page(browser, server)


check_setup()
server = os.environ.get('TARGET_SERVER')
username = os.environ.get('OPENSHIFT_USERNAME')
password = os.environ.get('OPENSHIFT_PASSWORD')
engine = os.environ.get('BROWSER_ENGINE', 'chrome')

print("Using the following browser engine {e}".format(e=engine))

run_tests(engine, server, username, password)
