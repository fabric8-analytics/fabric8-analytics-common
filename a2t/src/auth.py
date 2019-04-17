"""Retrieve temporary access token by using refresh/offline token.

Copyright (c) 2019 Red Hat Inc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from fastlog import log
from urllib.parse import urljoin
import requests

# The following endpoint is used to retrieve the access token from OSIO AUTH service
_AUTH_ENDPOINT = "/api/token/refresh"


def check_access_token_attribute(token_structure):
    """Additional check for the access_token attribute."""
    assert "access_token" in token_structure

    item = token_structure["access_token"]
    assert isinstance(item, str)

    # 200 chars is quite conservative
    assert len(token_structure["access_token"]) > 200

    # TODO: better check for token internal structure
    # 1) regexp-based
    # 2) decode it + check if it has all required fields (possibly)


def check_token_type_attribute(token_structure):
    """Additional check for the token_type attribute."""
    assert "token_type" in token_structure
    item = token_structure["token_type"]

    assert isinstance(item, str)
    # we don't know about any other token type
    assert item == "Bearer"


def check_expires_in_attribute(token_structure):
    """Additional check for the expires_in attribute."""
    assert "token_type" in token_structure
    item = token_structure["expires_in"]

    assert isinstance(item, int)
    assert item > 0


def check_refresh_expires_in_attribute(token_structure):
    """Additional check for the refresh_expires_in attribute."""
    assert "token_type" in token_structure
    item = token_structure["refresh_expires_in"]

    assert isinstance(item, int)
    assert item > 0


def check_not_before_policy_attribute(token_structure):
    """Additional check for the not-before-policy attribute."""
    assert "token_type" in token_structure
    item = token_structure["not-before-policy"]

    assert isinstance(item, int)
    assert item >= 0


def get_and_check_token_structure(data):
    """Get the token structure from returned data and check the basic format."""
    assert "token" in data
    token_structure = data["token"]

    assert "expires_in" in token_structure

    check_access_token_attribute(token_structure)
    check_token_type_attribute(token_structure)
    check_expires_in_attribute(token_structure)
    check_refresh_expires_in_attribute(token_structure)
    check_not_before_policy_attribute(token_structure)

    return token_structure


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
    token_structure = get_and_check_token_structure(data)

    log.info("Token seems to be correct")

    # seems like everything's ok, let's read the temporary access token
    return token_structure["access_token"]
