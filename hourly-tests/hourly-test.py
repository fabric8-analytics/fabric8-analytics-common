# Copyright © 2020 Red Hat Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Meer Sawood <msawood@redhat.com>
#
"""Hourly tests for Stack Analyses V2 API endpoints."""
import requests
import os
import time

API_URL = os.environ.get('F8A_API_URL', None)
THREE_SCALE_TOKEN = os.environ.get('THREE_SCALE_PROD_USER_KEY', None)

ECOSYSTEM_TO_MANIFEST_NAME_MAP = {
    'pypi': 'pylist.json',
    'npm': 'npmlist.json',
    'maven': 'dependencies.txt',
    'golang': 'golist.json'
}


def make_sa_post_req(manifest, ecosystem):
    """SA hourly post request."""
    params = {'user_key': THREE_SCALE_TOKEN}
    url = API_URL + "/api/v2/stack-analyses"
    files = {}
    data = {'show_transitive': False}
    if ecosystem != 'None':
        data['ecosystem'] = ecosystem
    if manifest != 'None':
        filename = 'data/{}'.format(manifest)
        files['manifest'] = (ECOSYSTEM_TO_MANIFEST_NAME_MAP.get(ecosystem,
                             'invalid_name.json'),
                             open(filename, 'rb'))
        data['file_path'] = os.path.abspath(os.path.dirname(filename))
    response = requests.request("POST", url, files=files,
                                data=data, params=params)
    time.sleep(10)
    if response.status_code == 200:
        data = response.json()
        stack_id = data['id']
        get_response = make_sa_get_request(stack_id)
        status_code = get_response.status_code
        if status_code == 200:
            check_for_feilds(get_response.json())
            return
        elif status_code == 202:
            check_for_feilds(get_response.json())
            return
        else:
            raise Exception("Error status code {c}".format(c=status_code))
        print(get_response.json())
    else:
        raise Exception("Error status code {c}".format(
                        c=response.status_code))


def check_for_feilds(data):
    """Check is analyzed deps present in data."""
    print(data)
    assert 'analyzed_dependencies' in data, "Response Invalid"


def make_sa_get_request(s_id):
    """Make Stack Analysis get request."""
    params = {'user_key': THREE_SCALE_TOKEN}
    url = API_URL + "/api/v2/stack-analyses/{}".format(s_id)
    response = requests.get(url, params=params)
    return response


if __name__ == "__main__":
    """Main Driver Code."""
    make_sa_post_req(manifest="pylist.json", ecosystem="pypi")
