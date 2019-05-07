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
from time import time, sleep
import json
from fastlog import log
from urllib.parse import urljoin
import os

from api import Api


# directory where the API results needs to be dumped
API_RESULTS_DIRECTORY = "api_results"

# TODO: make timeout configurable
DEFAULT_TIMEOUT = 10 * 60

DEFAULT_SLEEP_AMOUNT = 15


class StackAnalysis(Api):
    """Implementation of stack analysis."""

    def __init__(self, url, token, user_key, dump_json_responses):
        """Set the API endpoint and store the authorization token if provided."""
        super().__init__(url, token, user_key)
        self._dump_json_responses = dump_json_responses

    def analysis_url(self):
        """Construct URL for the component analyses REST API call."""
        return urljoin(self.url,
                       'api/v1/stack-analyses')

    def check_auth_token_validity(self):
        """Check that the authorization token is valid by calling the API and check HTTP code."""
        endpoint = self.url + 'api/v1/readiness'
        response = self.perform_get_request(endpoint)

        if response.status_code != 200:
            self.print_error_response(response, "error")
        return response.status_code == 200

    def dump_analysis(self, ecosystem, manifest, json_response):
        """Dump the stack analysis result into a file."""
        timestamp_str = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
        filename = API_RESULTS_DIRECTORY + "/"
        filename += "stack_analysis_{t}_{e}_{m}.json".format(t=timestamp_str,
                                                             e=ecosystem,
                                                             m=manifest)
        with open(filename, 'w') as fout:
            json.dump(json_response, fout)

    @staticmethod
    def get_manifest_name(filename):
        """Get the standard manifest name for the given filename."""
        manifests = {
            ".txt": "requirements.txt",
            ".xml": "pom.xml",
            ".json": "package.json"}
        for extension, manifest in manifests.items():
            if filename.endswith(extension):
                return manifest
        raise Exception("Unknown extension in filename: {f}".format(f=filename))

    @staticmethod
    def prepare_manifest_files(filename):
        """Send the selected manifest file to stack analysis."""
        # default variable substitutions
        filename = filename or 'requirements_click_6_star.txt'
        manifest_name = StackAnalysis.get_manifest_name(filename)

        log.info("filename with manifest data: {f}".format(f=filename))
        log.info("standard manifest name: {n}".format(n=manifest_name))

        filename = 'data/{filename}'.format(filename=filename)
        manifest_file_dir = os.path.dirname(filename)
        path_to_manifest_file = os.path.abspath(manifest_file_dir)

        files = {'manifest[]': (manifest_name, open(filename, 'rb')),
                 'filePath[]': (None, path_to_manifest_file)}
        return files

    def wait_for_stack_analysis(self, ecosystem, manifest, job_id, thread_id=""):
        """Wait for the stack analysis to finish."""
        endpoint = self.analysis_url() + "/" + job_id

        timeout = DEFAULT_TIMEOUT
        sleep_amount = DEFAULT_SLEEP_AMOUNT
        too_many_requests_cnt = 0

        for _ in range(timeout // sleep_amount):
            response = self.perform_get_request(endpoint)
            status_code = response.status_code
            log.info("thread# {t}  job# {j}  status code: {s}".format(
                t=thread_id, j=job_id, s=status_code))

            if status_code == 200:
                if self._dump_json_responses:
                    json_resp = response.json()
                    self.dump_analysis(ecosystem, manifest, json_resp)
                return response
            # 401 code should be checked later
            elif status_code == 401:
                log.info("WARNING: got 401")
                return response
            elif status_code == 500 or status_code == 504:
                log.info("WARNING: got {c}".format(c=status_code))
            elif status_code == 429:
                too_many_requests_cnt += 1
                log.info("Additional sleep...")
                sleep(sleep_amount)
                if too_many_requests_cnt > 10:
                    raise Exception('429 Too Many Requests')
            elif status_code != 202:
                # print("warning, got wrong status code {c}".format(c=status_code))
                raise Exception('Bad HTTP status code {c}'.format(c=status_code))
            sleep(sleep_amount)
        else:
            raise Exception('Timeout waiting for the stack analysis results')

    def start(self, thread_id=None, ecosystem=None, manifest=None, queue=None):
        """Start the component analysis and check the status code."""
        start_time = time()
        endpoint = self.analysis_url()
        files = StackAnalysis.prepare_manifest_files(manifest)

        response = self.perform_post_request(endpoint, files)

        response.raise_for_status()

        post_time = time()
        post_duration = post_time - start_time

        # log.info(response.json())
        job_id = response.json().get("id")
        log.info("job ID: " + job_id)

        try:
            self.wait_for_stack_analysis(ecosystem, manifest, job_id, thread_id)
            status_code = response.status_code
        except Exception as e:
            status_code = str(e)

        end_time = time()
        duration = end_time - post_time

        r1 = {"name": "stack_analysis",
              "method": "POST",
              "ecosystem": ecosystem,
              "package": "N/A",
              "version": "N/A",
              "thread_id": thread_id,
              "status_code": status_code,
              "json": response.json(),
              "started": start_time,
              "finished": post_time,
              "duration": post_duration,
              "manifest": manifest
              }

        r2 = {"name": "stack_analysis",
              "method": "GET",
              "ecosystem": ecosystem,
              "package": "N/A",
              "version": "N/A",
              "thread_id": thread_id,
              "status_code": status_code,
              "json": response.json(),
              "started": post_time,
              "finished": end_time,
              "duration": duration,
              "manifest": manifest
              }

        if queue is not None:
            queue.put(r1)
            queue.put(r2)

        # return both component analysis status and debug data (durations) as well
        return r1, r2
