import requests


class Api:

    _API_ENDPOINT = 'api/v1'

    def __init__(self, url):
        self.url = Api.add_slash(url)

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
