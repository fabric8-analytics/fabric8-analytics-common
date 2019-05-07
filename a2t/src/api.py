"""Module with class representing common API.

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

import requests
from fastlog import log


class Api:
    """Class representing common API."""

    # Prefix for all API endpoints
    # please note that we use version1 of API
    _API_ENDPOINT = 'api/v1'

    def __init__(self, url, token=None, user_key=None):
        """Set the API endpoint and store the authorization token if provided."""
        self.url = Api.add_slash(url)
        # optional on devcluster, but used on stage and on production as well
        self.token = token
        self.user_key = user_key

    def is_api_running(self):
        """Check if the API is available for calls."""
        try:
            res = requests.get(self.url)
            if res.status_code in {200, 401, 403}:
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
        """Print error message into the log if anything goes wrong."""
        log.error("Server returned HTTP code {c}".format(c=response.status_code))
        error_message = None
        try:
            error_message = response.json().get(message_key, "Server did not sent error message")
        except Exception:
            pass   # no error message

        if error_message:
            log.error("Error message: {m}".format(m=error_message))
