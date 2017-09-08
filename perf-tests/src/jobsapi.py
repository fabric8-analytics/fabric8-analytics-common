from api import *
import time
import datetime


class JobsApi(Api):

    def __init__(self, url, token):
        super().__init__(url, token)

    def authorization(self):
        return {'auth-token': '{token}'.format(token=self.token)}

    def send_json_file(self, endpoint, filename):
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}

        headers.update(self.authorization())
        with open(filename) as json_data:
            response = requests.post(endpoint, data=json_data, headers=headers)
        return response

    def start_component_analysis(self):
        filename = "data/job_pypi_clojure_py.json"
        endpoint = "{jobs_api_url}api/v1/jobs/flow-scheduling?state=running".\
            format(jobs_api_url=self.url)
        response = self.send_json_file(endpoint, filename)
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
                return
            time.sleep(sleep_amount)
        raise Exception('Timeout waiting for the job metadata in S3!')

    def component_analysis(self, s3):
        s3.connect()
        self.start_component_analysis()
        self.wait_for_component_analysis(s3, "pypi", "clojure_py", "0.2.4")
