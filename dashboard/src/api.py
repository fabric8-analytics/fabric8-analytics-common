"""Module with class representing common API."""
import requests
import os


class Api:
    """Class representing common API."""

    _API_ENDPOINT = 'api/v1'

    def __init__(self, url, token=None):
        """Set the API endpoint and store the authorization token if provided."""
        self.url = Api.add_slash(url)
        self.token = token

    def is_api_running(self):
        """Check if the API is available for calls."""
        try:
            res = requests.get(self.url)
            if res.status_code in {200, 401}:
                return True
        except requests.exceptions.ConnectionError:
            pass
        return False

    @staticmethod
    def add_slash(url):
        """Add a slash at end of URL, if the slash is not provided."""
        if url and not url.endswith('/'):
            url += '/'
        return url

    def get(self):
        """Use GET method to access API."""
        return requests.get(self.url)

    def print_error_response(self, response, message_key):
        """Print error message if anything goes wrong."""
        print("    Server returned HTTP code {c}".format(c=response.status_code))
        print("    Error message: {m}".format(m=error_message))
