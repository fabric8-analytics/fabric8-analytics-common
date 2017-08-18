from splinter import Browser
import time
import os
from urllib.parse import urljoin


SLEEP_BETWEEN_PAGES = 15
SLEEP_BEFORE_CLICK = 15


class Context:
    def __init__(self, server, username, password):
        self.browser = None
        self.space_name = None
        self.server = server
        self.username = username
        self.password = password


def check_env_variable(env_var_name):
    assert os.environ.get(env_var_name), \
        'The environment variable {v} should be set properly'.format(
            v=env_var_name)


def check_setup():
    check_env_variable('TARGET_SERVER')
    check_env_variable('OPENSHIFT_USERNAME')
    check_env_variable('OPENSHIFT_PASSWORD')


def front_page(context):
    '''Go to the Openshift.io front page and click the Login button.'''
    print("Front page")
    url = context.server
    context.browser.visit(url)
    time.sleep(SLEEP_BEFORE_CLICK)
    login_button = context.browser.find_by_css('button#login').first
    assert login_button.visible
    assert login_button.value == 'LOG IN'
    time.sleep(SLEEP_BEFORE_CLICK)
    login_button.click()
    time.sleep(SLEEP_BETWEEN_PAGES)


def login_page(context):
    '''Login into the Openshift.io using the provided username and
    password.'''
    print("Login page")
    username_input = context.browser.find_by_id('username').first
    password_input = context.browser.find_by_id('password').first
    assert username_input.visible
    assert password_input.visible
    context.browser.fill('username', context.username)
    context.browser.fill('password', context.password)
    login_button = context.browser.find_by_id('kc-login').first
    assert login_button.visible
    time.sleep(SLEEP_BEFORE_CLICK)
    login_button.click()
    time.sleep(SLEEP_BETWEEN_PAGES)


def get_all_existing_space_names(browser):
    '''Returns list of names of Spaces.'''
    spaces = browser.find_by_xpath("//div[@class='space-item']/h2/a")
    assert spaces is not None
    names = [space.value for space in spaces]
    print("Already created Spaces")
    print(" ".join(names))
    return names


def generate_space_prefix():
    localtime = time.localtime()
    return time.strftime("test%Y-%m-%d-")


def space_name(prefix, index):
    return "{p}{i}".format(p=prefix, i=index)


def is_space_name_unique(prefix, index, space_names):
    name = space_name(prefix, index)
    return name not in space_names


def generate_unique_space_name(space_names):
    '''Generate a name for a Space. The name is based on current date
    and is unique (by adding a small index to the date.'''
    prefix = generate_space_prefix()

    index = 1
    while not is_space_name_unique(prefix, index, space_names):
        index += 1
    return space_name(prefix, index)


def create_new_space_step_1(context):
    print('Create new Space: step 1')
    new_space_button = context.browser.find_by_text('New').first
    assert new_space_button is not None
    time.sleep(SLEEP_BEFORE_CLICK)
    new_space_button.click()
    name_input = context.browser.find_by_id('name').first
    assert name_input.visible
    context.browser.fill('name', context.space_name)
    create_space_button = context.browser.find_by_id('createSpaceButton').first
    assert create_space_button.visible
    time.sleep(SLEEP_BEFORE_CLICK)
    create_space_button.click()
    time.sleep(SLEEP_BETWEEN_PAGES)


def create_new_space_step_2(context):
    print('Create new Space: step 2')
    time.sleep(15)
    quick_start_button = context.browser.find_by_text('Quickstart').first
    assert quick_start_button is not None
    time.sleep(SLEEP_BEFORE_CLICK)
    quick_start_button.mouse_over()
    time.sleep(SLEEP_BEFORE_CLICK)
    quick_start_button.click()
    time.sleep(SLEEP_BETWEEN_PAGES)


def create_new_space_step_3(context):
    print('Create new Space: step 3')
    next_button = context.browser.find_by_id('forge-next-button').first
    assert next_button is not None
    print(next_button.text)
    time.sleep(SLEEP_BEFORE_CLICK)
    next_button.click()
    time.sleep(SLEEP_BETWEEN_PAGES)


def create_new_space_step_4(context):
    print('Create new Space: step 4')
    release_radio = context.browser.find_by_value('Release').first
    assert release_radio is not None
    time.sleep(SLEEP_BEFORE_CLICK)
    release_radio.click()
    next_button = context.browser.find_by_id('forge-next-button').first
    assert next_button is not None
    print(next_button.text)
    time.sleep(SLEEP_BEFORE_CLICK)
    next_button.click()
    time.sleep(SLEEP_BETWEEN_PAGES)


def create_new_space_step_5(context):
    print('Create new Space: step 5')
    next_button = context.browser.find_by_id('forge-next-button').first
    assert next_button is not None
    print(next_button.text)
    time.sleep(SLEEP_BEFORE_CLICK)
    next_button.click()
    time.sleep(SLEEP_BETWEEN_PAGES)


def create_new_space_step_6(context):
    print('Create new Space: step 6')
    finish_button = context.browser.find_by_id('forge-finish-button').first
    assert finish_button is not None
    print(finish_button.text)
    time.sleep(SLEEP_BEFORE_CLICK)
    finish_button.click()
    time.sleep(SLEEP_BETWEEN_PAGES)


def spaces_page(context):
    '''Go to the Spaces page with list of available Spaces.'''
    print("Spaces page")
    url = urljoin(context.server, context.username+"/_spaces")
    context.browser.visit(url)
    space_names = get_all_existing_space_names(context.browser)
    new_space_name = generate_unique_space_name(space_names)
    context.space_name = new_space_name
    print("Unique name for new Space\n    " + new_space_name)
    create_new_space_step_1(context)
    create_new_space_step_2(context)
    create_new_space_step_3(context)
    create_new_space_step_4(context)
    create_new_space_step_5(context)
    create_new_space_step_6(context)


def check_text_presence(context, text):
    tag = context.browser.find_by_text(text).first
    assert tag is not None
    print("    The text '{t}' is found on the page".format(t=text))


def stack_recommendation_on_space_page(context):
    url = urljoin(context.server, context.username+"/" + context.space_name)
    print("Going to the Space {s}".format(s=context.space_name))
    context.browser.visit(url)
    time.sleep(SLEEP_BEFORE_CLICK)

    recommendation1 = 'Recommendation: Change io.vertx:vertx-web : 3.4.1'
    check_text_presence(context, recommendation1)
    recommendation2 = 'Recommendation: Change io.vertx:vertx-core : 3.4.1'
    check_text_presence(context, recommendation2)

    time.sleep(SLEEP_BETWEEN_PAGES)



def run_tests(engine, server, username, password):
    context = Context(server, username, password)
    with Browser(engine) as browser:
        context.browser = browser
        front_page(context)
        login_page(context)
        spaces_page(context)


check_setup()
server = os.environ.get('TARGET_SERVER')
username = os.environ.get('OPENSHIFT_USERNAME')
password = os.environ.get('OPENSHIFT_PASSWORD')
engine = os.environ.get('BROWSER_ENGINE', 'chrome')

print("Using the following browser engine {e}".format(e=engine))

run_tests(engine, server, username, password)
