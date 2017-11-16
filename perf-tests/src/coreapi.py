"""Module with class representing core (server) API."""
from urllib.parse import urljoin

from api import *
import time
import datetime
import json


class CoreApi(Api):
    """Class representing core (server) API."""

    def __init__(self, url, token):
        """Set the API endpoint and store the authorization token if provided."""
        super().__init__(url, token)
        self._stack_analysis_manifest = None
        self._dump_json_responses = False

    @property
    def stack_analysis_manifest(self):
        """Getter to retrieve the stack analysis manifest name."""
        return self._stack_analysis_manifest

    @stack_analysis_manifest.setter
    def stack_analysis_manifest(self, filename):
        self._stack_analysis_manifest = filename

    @property
    def dump_json_responses(self):
        """Getter to retrieve the flag if JSON responses dumps are enabled."""
        return self._dump_json_responses

    @dump_json_responses.setter
    def dump_json_responses(self, settings):
        self._dump_json_responses = settings

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

    @staticmethod
    def contains_alternate_node(json_resp):
        """Check for the existence of alternate node in the stack analysis."""
        result = json_resp.get('result')
        return bool(result) and isinstance(result, list) \
            and (result[0].get('recommendation', {}) or {}).get('alternate', None) is not None

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
        raise "Unknown extension in filename: {f}".format(f=filename)

    @staticmethod
    def prepare_manifest_files(filename):
        """Send the selected manifest file to stack analysis."""
        # default variable substitutions
        filename = filename or 'requirements_click_6_star.txt'
        manifest_name = CoreApi.get_manifest_name(filename)

        print("filename with manifest data: {f}".format(f=filename))
        print("standard manifest name: {n}".format(n=manifest_name))

        filename = 'data/{filename}'.format(filename=filename)
        manifest_file_dir = os.path.dirname(filename)
        path_to_manifest_file = os.path.abspath(manifest_file_dir)

        files = {'manifest[]': (manifest_name, open(filename, 'rb')),
                 'filePath[]': (None, path_to_manifest_file)}
        return files

    @staticmethod
    def dump_stack_analysis(job_id, json_response):
        """Dump the stack analysis result into a file."""
        filename = "stack_analysis_{j}.json".format(j=job_id)
        with open(filename, 'w') as fout:
            json.dump(json_response, fout)

    @staticmethod
    def dump_component_analysis(ecosystem, component, version, json_response):
        """Dump the component analysis result into a file."""
        timestamp_str = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
        filename = "component_analysis_{e}_{c}_{v}_{t}.json".format(e=ecosystem,
                                                                    c=component,
                                                                    v=version,
                                                                    t=timestamp_str)
        with open(filename, 'w') as fout:
            json.dump(json_response, fout)

    def start_stack_analysis(self):
        """Start the stack analysis, sending the manifest file."""
        files = CoreApi.prepare_manifest_files(self._stack_analysis_manifest)
        endpoint = self.url + 'api/v1/stack-analyses'
        response = requests.post(endpoint, files=files, headers=self.authorization())
        response.raise_for_status()
        print(response.json())
        job_id = response.json().get("id")
        print("job ID: " + job_id)
        return job_id

    def wait_for_stack_analysis(self, job_id, thread_id="", i=0):
        """Wait for the stack analysis to finish."""
        endpoint = self.url + 'api/v1/stack-analyses/' + job_id
        timeout = 5000
        sleep_amount = 5

        for _ in range(timeout // sleep_amount):
            response = requests.get(endpoint, headers=self.authorization())
            status_code = response.status_code
            print("        thread# {t}  run# {r}  job# {j}  status code: {s}".format(
                t=thread_id, r=i, j=job_id,
                s=status_code))
            if status_code == 200:
                json_resp = response.json()
                if CoreApi.contains_alternate_node(json_resp):
                    if self._dump_json_responses:
                        CoreApi.dump_stack_analysis(job_id, json_resp)
                    return response
            # 401 code should be checked later
            elif status_code == 401:
                print("WARNING: got 401")
                return response
            elif status_code == 500 or status_code == 504:
                print("WARNING: got {c}".format(c=status_code))
            elif status_code != 202:
                # print("warning, got wrong status code {c}".format(c=status_code))
                raise Exception('Bad HTTP status code {c}'.format(c=status_code))
            time.sleep(sleep_amount)
        else:
            raise Exception('Timeout waiting for the stack analysis results')

    def read_stack_analysis_debug_data(self, job_id, thread_id="", i=0):
        """Read the stack analysis debug data via API."""
        endpoint = self.url + 'api/v1/stack-analyses/' + job_id + "/_debug"
        response = requests.get(endpoint, headers=self.authorization())
        status_code = response.status_code
        if status_code == 200:
            return response
        else:
            raise Exception('Bad HTTP status code {s} returned by the call {c}'.format(
                s=status_code, c=endpoint))

    def stack_analysis(self, thread_id=None, i=0):
        """Start the stack analysis and wait for its finish."""
        job_id = self.start_stack_analysis()
        result = self.wait_for_stack_analysis(job_id, thread_id, i)
        debug = self.read_stack_analysis_debug_data(job_id, thread_id, i)
        # return both stack analysis results and debug data (durations) as well
        return {"result": result,
                "debug": debug}

    def component_analysis_url(self, ecosystem, component, version):
        """Construct URL for the component analyses REST API call."""
        return urljoin(self.url,
                       'api/v1/component-analyses/{e}/{c}/{v}'.format(e=ecosystem,
                                                                      c=component,
                                                                      v=version))

    def component_analysis(self, thread_id=None, i=0,
                           ecosystem=None, component=None, version=None):
        """Start the component analysis and check the status code."""
        url = self.component_analysis_url(ecosystem, component, version)
        response = requests.get(url, headers=self.authorization())
        if self._dump_json_responses:
            CoreApi.dump_component_analysis(ecosystem, component, version, response.json())
        status_code = response.status_code
        return {"result": status_code}
