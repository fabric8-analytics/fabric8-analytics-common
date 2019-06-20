"""REST API calls implementation."""

import requests
import json


def authorization(token):
    """Construct header with authorization token for the server API calls.

    Returned dict can be added to the 'request' object.
    """
    return {'Authorization': 'Bearer {token}'.format(token=token)}


def content_type(content_type="application/json"):
    """Construct header with content type declaration for the server API calls.

    Returned dict can be added to the 'request' object.
    """
    return {'Content-type': content_type}


def send_payload(url, payload, access_token):
    """Send payload to the REST API endpoint using POST HTTP method."""
    json_payload = json.dumps(payload)
    headers = content_type()
    if access_token:
        headers.update(authorization(access_token))
    response = requests.post(url, data=json_payload, headers=headers)
    return response
