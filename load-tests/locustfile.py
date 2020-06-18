"""LOAD TESTING FOR V2 API."""
from locust import HttpUser, task, between
import os


def _add_slash(url):
    if url and not url.endswith('/'):
        url += '/'
    return url


def _read_url_from_env_var(env_var_name):
    return _add_slash(os.environ.get(env_var_name, None))


core_v2_api_url = _read_url_from_env_var('F8A_API_V2_URL')
user_key = os.environ.get('THREE_SCALE_PREVIEW_USER_KEY', None)

if core_v2_api_url is None or core_v2_api_url == "":
    print("No API URL FOUND EXITING")
    os._exit(0)
elif user_key is None or user_key == "":
    print("No API USER KEY FOUND EXITING")
    os._exit(0)

fp = open('data/pylist.json')
fp1 = fp.read()


class QuickstartUser(HttpUser):
    """Class that handles the locusts load test."""

    wait_time = between(0, 2)
    params = {'user_key': user_key}

    @task
    def CA_V2(self):
        """Component analysis load tests."""
        response = self.client.get(core_v2_api_url + "api/v2/component-analyses/npm/marked/0.3.5",
                                   params=self.params)
        print(response.json())

    @task
    def SA_V2(self):
        """Stack analysis load tests."""
        response = self.client.post(core_v2_api_url + "api/v2/stack-analyses/",
                                    files={'manifest': ('pylist.json', fp1)},
                                    data={'file_path': '/home/JohnDoe', 'ecosystem': 'pypi'},
                                    params=self.params)
        print(response.json())
