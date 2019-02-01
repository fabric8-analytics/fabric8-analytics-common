"""Basic checks for the server API."""
from behave import then, when
from urllib.parse import urljoin

import requests

from src.authorization_tokens import authorization
from src.parsing import parse_token_clause


def post_data_to_user_intent_endpoint(context, payload=None):
    """Post data into the REST API endpoint for user-intent."""
    url = "/api/v1/user-intent"

    if payload is not None:
        context.response = requests.post(context.coreapi_url + url,
                                         headers=authorization(context),
                                         data=payload)
    else:
        context.response = requests.post(context.coreapi_url + url,
                                         headers=authorization(context))


@when('I call user-intent endpoint without any payload')
def check_user_intent_without_payload(context):
    """Post no payload into the REST API endpoint for user-intent."""
    post_data_to_user_intent_endpoint(context)


@when('I call user-intent endpoint with empty payload')
def check_user_intent_with_empty_payload(context):
    """Post empty into the REST API endpoint for user-intent."""
    payload = {}
    post_data_to_user_intent_endpoint(context, payload)
