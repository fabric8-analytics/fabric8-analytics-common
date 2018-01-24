"""Basic checks for the server API."""
from behave import given, then, when
import requests

from src.utils import *
from src.authorization_tokens import *


@when('I access {url:S}')
def access_url(context, url):
    """Access the service API using the HTTP GET method."""
    context.response = requests.get(context.coreapi_url + url)


@when('I access {url:S} with authorization token')
def access_url_with_authorization_token(context, url):
    """Access the service API using the HTTP GET method."""
    context.response = requests.get(context.coreapi_url + url,
                                    headers=authorization(context))


@then('I should see {num:d} ecosystems')
def check_ecosystems(context, num):
    """Check if the API call returns correct number of ecosystems."""
    ecosystems = context.response.json()['items']
    assert len(ecosystems) == num
    for e in ecosystems:
        # assert that there is 'ecosystem' field in every ecosystem
        assert 'ecosystem' in e


@then('I should see {num:d} versions ({versions}), all for {ecosystem}/{package} package')
def check_versions(context, num=0, versions='', ecosystem='', package=''):
    """Check the versions for the selected ecosystems and package."""
    versions = split_comma_separated_list(versions)
    vrsns = context.response.json()['items']
    assert len(vrsns) == num
    for v in vrsns:
        assert v['ecosystem'] == ecosystem
        assert v['package'] == package
        assert v['version'] in versions
