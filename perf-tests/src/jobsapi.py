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

