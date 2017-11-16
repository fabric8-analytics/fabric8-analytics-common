"""Module with class representing jobs API."""
from api import *
import time
import datetime
import json
import botocore
from botocore.exceptions import ClientError
from componentgenerator import *


class JobsApi(Api):
    """Class representing jobs API."""

    def __init__(self, url, token):
        """Set the API endpoint and store the authorization token if provided."""
        super().__init__(url, token)
        self.componentGeneratorForPypi = ComponentGenerator.generator_for_ecosystem('pypi')
        self._dump_json_responses = False

    @property
    def dump_json_responses(self):
        """Getter to retrieve the flag if JSON responses dumps are enabled."""
        return self._dump_json_responses

    @dump_json_responses.setter
    def dump_json_responses(self, settings):
        self._dump_json_responses = settings

    def authorization(self):
        """Return a HTTP header with authorization token."""
        return {'auth-token': '{token}'.format(token=self.token)}

    def send_json_file(self, endpoint, filename):
        """Send the content of file to the selected API endpoint as JSON."""
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}

        headers.update(self.authorization())
        with open(filename) as json_data:
            response = requests.post(endpoint, data=json_data, headers=headers)
        return response

    def send_data_as_json(self, endpoint, data):
        """Send the JSON data to the selected API endpoint.

        Data (any Python structure) is converted to JSON first.
        """
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}

        headers.update(self.authorization())
        json_data = json.dumps(data)
        print(json_data)
        response = requests.post(endpoint, data=json_data, headers=headers)
        return response

    def check_auth_token_validity(self):
        """Check that the authorization token is valid by calling the API and check HTTP code."""
        endpoint = self.url + 'api/v1/jobs'
        response = requests.get(endpoint, headers=self.authorization())
        if response.status_code != 200:
            self.print_error_response(response, "detail")
        return response.status_code == 200

    def prepare_jobs_data(self, ecosystem, package, version):
        """Prepare data structure that specify new job attributes."""
        return \
            {
                "flow_arguments": [
                    {
                        "ecosystem": ecosystem,
                        "name": package,
                        "version": version,
                        "force": True,
                        "force_graph_sync": True,
                        "recursive_limit": 0
                    }
                ],
                "flow_name": "bayesianApiFlow"
            }

    @staticmethod
    def dump_job_data(s3, bucket, key):
        """Dump the job data read from the S3 database to a file."""
        data = s3.read_object(bucket, key)
        timestamp_str = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
        filename = "s3_data_{e}_{c}_{v}_{t}.json".format(e=ecosystem,
                                                         c=component,
                                                         v=version,
                                                         t=timestamp_str)
        with open(filename, 'w') as fout:
            json.dump(data, fout)

    def start_component_analysis(self, ecosystem, package, version, thread_id):
        """Start the component analysis."""
        jobs_data = self.prepare_jobs_data(ecosystem, package, version)
        endpoint = "{jobs_api_url}api/v1/jobs/flow-scheduling?state=running".\
            format(jobs_api_url=self.url)
        print(endpoint)
        print(thread_id)
        response = self.send_data_as_json(endpoint, jobs_data)
        assert response.status_code == 201
        print(response)
        print(response.json())

    def wait_for_component_analysis(self, s3, ecosystem, package, version, thread_id=""):
        """Wait for the component analysis by looking at metadata stored in the S3 database."""
        timeout = 300 * 60
        sleep_amount = 10

        bucket = "bayesian-core-data"

        key = s3.component_key(ecosystem, package, version)
        print(key)

        start_time = datetime.datetime.now(datetime.timezone.utc)

        for _ in range(timeout // sleep_amount):
            current_date = datetime.datetime.now(datetime.timezone.utc)
            try:
                last_modified = s3.read_object_metadata(bucket, key, "LastModified")
                delta = current_date - last_modified
                print(thread_id, "  ", "   ", key, "   ", current_date, "   ", last_modified,
                      "   ", delta, "   ", delta.seconds,
                      "    ", current_date - start_time)
                if delta.days == 0 and delta.seconds < sleep_amount * 2:
                    print("done!", thread_id, "   ", key)
                    if self._dump_json_responses:
                        JobsApi.dump_job_data(s3, bucket, key)
                    return True
            except ClientError as e:
                print("No analyses yet (waiting for {t})".format(t=current_date - start_time))
            time.sleep(sleep_amount)

        # raise Exception('Timeout waiting for the job metadata in S3!')

        print('Timeout waiting for the job metadata in S3!\n'
              '(timetout is se to {s} seconds)'.format(s=timeout))
        return False

    def component_analysis(self, i, s3, thread_id=None,
                           ecosystem=None, component=None, version=None):
        """Start the component analysis and wait for its finish."""
        if ecosystem is None or component is None or version is None:
            ecosystem, component, version = next(self.componentGeneratorForPypi)
        s3.connect()
        self.start_component_analysis(ecosystem, component, version, thread_id)
        return self.wait_for_component_analysis(s3, ecosystem, component, version, thread_id)
