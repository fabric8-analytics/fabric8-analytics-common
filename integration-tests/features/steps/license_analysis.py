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
