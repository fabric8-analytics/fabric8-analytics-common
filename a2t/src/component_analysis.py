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

import datetime
from time import time
import json
import re
from urllib.parse import urljoin

from api import Api


# directory where the API results needs to be dumped
API_RESULTS_DIRECTORY = "api_results"


class ComponentAnalysis(Api):
    """Implementation of component analysis."""

    def __init__(self, url, token, user_key, dump_json_responses):
        """Set the API endpoint and store the authorization token if provided."""
        super().__init__(url, token, user_key)
        self._dump_json_responses = dump_json_responses

    def analysis_url(self, ecosystem, component, version):
        """Construct URL for the component analyses REST API call."""
        return urljoin(self.url,
                       'api/v1/component-analyses/{e}/{c}/{v}'.format(e=ecosystem,
                                                                      c=component,
                                                                      v=version))

    def check_auth_token_validity(self):
        """Check that the authorization token is valid by calling the API and check HTTP code."""
        endpoint = self.url + 'api/v1/readiness'
        response = self.perform_get_request(endpoint)

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

    def check_analysis(self, analysis, ecosystem, package, version):
        """Check the results of component analysis."""
        try:
            assert analysis is not None, "Analysis not available"
            assert "result" in analysis, "Can not find the 'result' node."
            result = analysis["result"]
            self.check_recommendation_part(result)
            self.check_data_part(result, ecosystem, package, version)
            return "OK"
        except Exception as e:
            return "Failed: " + str(e)

    def start(self, thread_id=None, ecosystem=None, component=None, version=None, queue=None):
        """Start the component analysis and check the status code."""
        start_time = time()
        endpoint = self.analysis_url(ecosystem, component, version)
        response = self.perform_get_request(endpoint)

        if self._dump_json_responses:
            try:
                self.dump_analysis(ecosystem, component, version, response.json())
            except Exception:
                self.print_error_response(response, "error")

        status_code = response.status_code
        end_time = time()
        duration = end_time - start_time

        json_response = ""
        check = "N/A"

        try:
            json_response = response.json()
            if status_code == 200:
                check = self.check_analysis(json_response, ecosystem, component, version)
            else:
                check = "N/A, analysis in progress"
        except Exception:
            pass

        r = {"name": "component_analysis",
             "method": "GET",
             "ecosystem": ecosystem,
             "package": component,
             "version": version,
             "thread_id": thread_id,
             "status_code": status_code,
             "json": json_response,
             "started": start_time,
             "finished": end_time,
             "duration": duration,
             "analysis": check,
             "manifest": "N/A"
             }

        if queue is not None:
            queue.put(r)

        # return both component analysis status and debug data (durations) as well
        return r
