"""Tests for license analysis service."""
import requests

from behave import given, then, when
from urllib.parse import urljoin

from src.parsing import *
from src.utils import *
from src.authorization_tokens import *


@when("I access the license analysis service")
def access_license_service(context):
    """Access the licence analysis service."""
    context.response = requests.get(context.license_service_url)


@when("I access the license analysis service with authorization token")
def access_license_service(context):
    """Access the licence analysis service using the authorization token."""
    context.response = requests.get(context.license_service_url,
                                    headers=authorization(context))


def send_payload_to_license_analysis(context, filename, use_token):
    """Send the selected file to the license analysis service to be processed."""
    filename = 'data/license_analysis/{filename}'.format(filename=filename)
    path_to_file = os.path.abspath(filename)

    endpoint = context.license_service_url + "/api/v1/license-recommender"

    with open(path_to_file) as json_data:
        if use_token:
            response = requests.post(endpoint, data=json_data,
                                     headers=authorization(context))
        else:
            response = requests.post(endpoint, data=json_data)

    context.response = response


@when("I send the file {filename} to the license analysis service")
@when("I send the file {filename} to the license analysis service {token} authorization token")
def send_the_file_for_license_analysis(context, filename, token="without"):
    """Test step to send the selected file to the license analysis service."""
    use_token = parse_token_clause(token)
    send_payload_to_license_analysis(context, filename, use_token)
