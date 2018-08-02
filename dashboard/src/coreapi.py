"""Module with class representing core (server) API."""
import requests

from api import Api


class CoreApi(Api):
    """Class representing core (server) API."""

    def __init__(self, url, token):
        """Set the API endpoint and store the authorization token if provided."""
        super().__init__(url, token)

    def authorization(self):
        """Return a HTTP header with authorization token."""
        return {'Authorization': 'Bearer {token}'.format(token=self.token)}

    def check_auth_token_validity(self):
        """Check that the authorization token is valid by calling the API and check HTTP code."""
        endpoint = self.url + 'api/v1/component-search/foobar'
        response = requests.get(endpoint, headers=self.authorization())
        if response.status_code != 200:
            self.print_error_response(response, "error")
        return response.status_code == 200
