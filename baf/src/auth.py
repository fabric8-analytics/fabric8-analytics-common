"""Retrieve temporary access token by using refresh/offline token."""

from fastlog import log
from urllib.parse import urljoin
import requests

# The following endpoint is used to retrieve the access token from OSIO AUTH service
_AUTH_ENDPOINT = "/api/token/refresh"


def retrieve_access_token(refresh_token, auth_service_url):
    """Retrieve temporary access token by using refresh/offline token."""
    log.info("Trying to retrieve access token")
    if refresh_token is None:
        log.error("aborting: RECOMMENDER_REFRESH_TOKEN environment variable is not set")
        return None
    if auth_service_url is None:
        log.error("aborting: OSIO_AUTH_SERVICE environment variable is not set")
        return None

    payload = {'refresh_token': refresh_token}
    url = urljoin(auth_service_url, _AUTH_ENDPOINT)
    response = requests.post(url, json=payload)

    assert response is not None and response.ok, "Error communicating with the OSIO AUTH service"
    data = response.json()

    # check the basic structure of the response
    assert "token" in data
    token_structure = data["token"]

    assert "access_token" in token_structure
    assert "token_type" in token_structure
    assert "expires_in" in token_structure

    log.info("Token seems to be correct")

    # seems like everything's ok, let's read the temporary access token
    return token_structure["access_token"]
