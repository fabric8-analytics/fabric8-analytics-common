"""REST API calls implementation."""

import requests
from fastlog import log


def authorization(token):
    """Construct header with authorization token for the server API calls.

    Returned dict can be added to the 'request' object.
    """
    return {'Authorization': 'Bearer {token}'.format(token=token)}


def send_payload(url, payload, access_token):
    """Send payload to the REST API endpoint using POST HTTP method."""
    if access_token:
        response = requests.post(url, data=payload, headers=authorization(access_token))
    else:
        response = requests.post(url, data=payload)
    return response
