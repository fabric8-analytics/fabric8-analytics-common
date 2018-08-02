"""Test steps that are related to authorization tokens for the server API and jobs API."""
import os
import datetime

import jwt
from jwt.contrib.algorithms.pycrypto import RSAAlgorithm

DEFAULT_AUTHORIZATION_TOKEN_FILENAME = "private_key.pem"

jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))


@then('I should get the proper authorization token')
def is_proper_authorization_token_for_server_api(context):
    """Check if the test has any authorization token for server API."""
    assert context.token is not None


@then('I should get the proper job API authorization token')
def is_proper_authorization_token_for_jobs_api(context):
    """Check if the test has any authorization token for the Jobs API."""
    assert context.jobs_api_token is not None


@when('I acquire the authorization token')
def acquire_authorization_token(context):
    """Acquire the authorization token.

    The token is read from the environment variable or is to be generated from
    the given .pem file (private key).

    Alternatively the REFRESH_TOKEN (offline token) can be used to get
    the temporary access token - it should be done just once in environment.py.
    """
    recommender_token = os.environ.get("RECOMMENDER_API_TOKEN")
    # log.info ("TOKEN: {}\n\n".format(recommender_token))

    # if access_token has been acquired via refresh/offline token, let's use it
    # (and don't call AUTH API several times - it is not encouraged)
    if context.access_token is not None:
        context.token = context.access_token
    elif recommender_token is not None:
        context.token = recommender_token
    else:
        generate_authorization_token(context, DEFAULT_AUTHORIZATION_TOKEN_FILENAME)


@when('I generate authorization token from the private key {private_key}')
def generate_authorization_token(context, private_key):
    """Generate authorization token from the private key."""
    expiry = datetime.datetime.utcnow() + datetime.timedelta(days=90)
    userid = "testuser"

    path_to_private_key = 'data/{private_key}'.format(private_key=private_key)
    # initial value
    context.token = None

    with open(path_to_private_key) as fin:
        private_key = fin.read()

        payload = {
            'exp': expiry,
            'iat': datetime.datetime.utcnow(),
            'sub': userid
        }
        token = jwt.encode(payload, key=private_key, algorithm='RS256')
        decoded = token.decode('utf-8')
        # print(decoded)
        context.token = decoded


@then("I should get API token")
def check_api_token(context):
    """Check the API token existence."""
    try:
        j = json.loads(context.kerb_request)
    except ValueError:
        print(context.kerb_request)
        raise
    assert j["token"]
