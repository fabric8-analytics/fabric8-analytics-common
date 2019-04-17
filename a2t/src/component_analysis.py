"""Component analysis benchmarks.

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
import time
import datetime
import json
import os
from urllib.parse import urljoin

from api import Api


# directory where the API results needs to be dumped
API_RESULTS_DIRECTORY = "api_results"


class ComponentAnalysis(Api):
    """Implementation of component analysis."""

    def __init__(self, url, token, dump_json_responses):
        """Set the API endpoint and store the authorization token if provided."""
        super().__init__(url, token)
        self._dump_json_responses = dump_json_responses

    def analysis_url(self, ecosystem, component, version):
        """Construct URL for the component analyses REST API call."""
        return urljoin(self.url,
                       'api/v1/component-analyses/{e}/{c}/{v}'.format(e=ecosystem,
                                                                      c=component,
                                                                      v=version))

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

    def dump_analysis(self, ecosystem, component, version, json_response):
        """Dump the component analysis result into a file."""
        timestamp_str = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
        filename = API_RESULTS_DIRECTORY + "/"
        filename += "component_analysis_{e}_{c}_{v}_{t}.json".format(e=ecosystem,
                                                                     c=component,
                                                                     v=version,
                                                                     t=timestamp_str)
        with open(filename, 'w') as fout:
            json.dump(json_response, fout)

    def start(self, thread_id=None, i=0, ecosystem=None, component=None, version=None, queue=None):
        """Start the component analysis and check the status code."""
        url = self.analysis_url(ecosystem, component, version)
        response = requests.get(url, headers=self.authorization())

        if self._dump_json_responses:
            self.dump_analysis(ecosystem, component, version, response.json())

        status_code = response.status_code

        r = {"result": status_code,
             "json": response.json()}

        if queue is not None:
            queue.put(r)

        # return both component analysis status and debug data (durations) as well
        return r
