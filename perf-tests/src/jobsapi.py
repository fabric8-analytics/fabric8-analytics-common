from api import *
import time
import datetime
from componentgenerator import *


class JobsApi(Api):

    def __init__(self, url, token):
        super().__init__(url, token)
        self.componentGeneratorForPypi = ComponentGenerator.generator_for_ecosystem('pypi')

    def authorization(self):
        return {'auth-token': '{token}'.format(token=self.token)}

    def send_json_file(self, endpoint, filename):
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}

        headers.update(self.authorization())
        with open(filename) as json_data:
            response = requests.post(endpoint, data=json_data, headers=headers)
        return response

    def send_data_as_json(self, endpoint, data):
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}

        headers.update(self.authorization())
        json_data = json.dumps(data)
        print(json_data)
        response = requests.post(endpoint, data=json_data, headers=headers)
        return response

    def check_auth_token_validity(self):
        endpoint = self.url + 'api/v1/jobs'
        response = requests.get(endpoint, headers=self.authorization())
        if response.status_code != 200:
            self.print_error_response(response, "detail")
        return response.status_code == 200

    def prepare_jobs_data(self, ecosystem, package, version):
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

    def start_component_analysis(self, ecosystem, package, version, thread_id):
        jobs_data = self.prepare_jobs_data(ecosystem, package, version)
        endpoint = "{jobs_api_url}api/v1/jobs/flow-scheduling?state=running".\
            format(jobs_api_url=self.url)
        print(endpoint)
        print(thread_id)
        response = self.send_data_as_json(endpoint, jobs_data)
        assert response.status_code == 201
        print(response)
        print(response.json())

    def wait_for_component_analysis(self, s3, ecosystem, package, version):
        timeout = 300 * 60
        sleep_amount = 10

        bucket = "bayesian-core-data"

        key = s3.component_key(ecosystem, package, version)
        print(key)

        for _ in range(timeout // sleep_amount):
            current_date = datetime.datetime.now(datetime.timezone.utc)
            last_modified = s3.read_object_metadata(bucket, key, "LastModified")
            delta = current_date - last_modified
            print(current_date, "   ", last_modified, "   ", delta, "   ", delta.seconds)
            if delta.days == 0 and delta.seconds < sleep_amount * 2:
                print("done!")
                # s3.read_core_data_from_bucket(context, package, version, ecosystem, bucket)
                return True
            time.sleep(sleep_amount)

        # raise Exception('Timeout waiting for the job metadata in S3!')

        print('Timeout waiting for the job metadata in S3!\n'
              '(timetout is se to {s} seconds)'.format(s=timeout))
        return False

    def component_analysis(self, i, s3):
        s3.connect()
        self.start_component_analysis()
        return self.wait_for_component_analysis(s3, "pypi", "clojure_py", "0.2.4")
