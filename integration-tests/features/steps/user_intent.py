"""Basic checks for the server API."""
from behave import when

import requests

from src.authorization_tokens import authorization


def post_data_to_user_intent_endpoint(context, payload=None):
    """Post data into the REST API endpoint for user-intent."""
    url = "/api/v1/user-intent"

    if payload is not None:
        context.response = requests.post(context.coreapi_url + url,
                                         headers=authorization(context),
                                         json=payload)
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


@when('I call user-intent endpoint with incorrect payload')
def check_user_intent_with_incorrect_payload(context):
    """Post incorrect into the REST API endpoint for user-intent."""
    payload = {"foo": "bar"}
    post_data_to_user_intent_endpoint(context, payload)


@when('I call user-intent endpoint with payload that contains only manual_tagging attribute')
def check_user_intent_with_manual_tagging_attribute_in_payload(context):
    """Post incomplete payload into the REST API endpoint for user-intent."""
    payload = {"manual_tagging": "true"}
    post_data_to_user_intent_endpoint(context, payload)


@when('I call user-intent endpoint with payload that contains only manual_tagging and user '
      'attributes')
def check_user_intent_with_manual_tagging_user_attributes_in_payload(context):
    """Post incomplete payload into the REST API endpoint for user-intent."""
    payload = {"manual_tagging": "true",
               "user": "User name"}
    post_data_to_user_intent_endpoint(context, payload)


@when('I call user-intent endpoint with payload that contains only ecosystem attribute')
def check_user_intent_with_ecosystem_in_payload(context):
    """Post incomplete payload into the REST API endpoint for user-intent."""
    payload = {"ecosystem": "npm"}
    post_data_to_user_intent_endpoint(context, payload)
