import requests
import os


class Api:

    _API_ENDPOINT = 'api/v1'

    def __init__(self, url, token=None):
        self.url = Api.add_slash(url)
        self.token = token

    def is_api_running(self):
        try:
            res = requests.get(self.url)
            if res.status_code in {200, 401}:
                return True
        except requests.exceptions.ConnectionError:
            pass
        return False

    def add_slash(url):
        if url and not url.endswith('/'):
            url += '/'
        return url

    def get(self):
        return requests.get(self.url)

    def print_error_response(self, response, message_key):
        print("    Server returned HTTP code {c}".format(c=response.status_code))
        try:
            error_message = response.json().get(message_key, "Server does not sent error message")
            print("    Error message: {m}".format(m=error_message))
        except Exception:
            pass   # no error message
