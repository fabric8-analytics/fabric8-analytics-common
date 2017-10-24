from urllib.parse import urljoin

from api import *
import time


class CoreApi(Api):

    def __init__(self, url, token):
        super().__init__(url, token)

    def authorization(self):
        return {'Authorization': 'Bearer {token}'.format(token=self.token)}

    def check_auth_token_validity(self):
        endpoint = self.url + 'api/v1/component-search/foobar'
        response = requests.get(endpoint, headers=self.authorization())
        if response.status_code != 200:
            self.print_error_response(response, "error")
        return response.status_code == 200

    def start_stack_analysis(self):
        filename = 'data/requirements_click_6_star.txt'
        manifest_file_dir = os.path.dirname(filename)
        path_to_manifest_file = os.path.abspath(manifest_file_dir)
        files = {'manifest[]': ("requirements.txt", open(filename, 'rb')),
                 'filePath[]': (None, path_to_manifest_file)}
        endpoint = self.url + 'api/v1/stack-analyses'
        response = requests.post(endpoint, files=files, headers=self.authorization())
        response.raise_for_status()
        print(response.json())
        job_id = response.json().get("id")
        print("job ID: " + job_id)
        return job_id

    def wait_for_stack_analysis(self, job_id, thread_id="", i=0):
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

    def stack_analysis(self, thread_id=None, i=0):
        job_id = self.start_stack_analysis()
        return self.wait_for_stack_analysis(job_id, thread_id, i)

    def component_analysis_url(self, ecosystem, component, version):
        """Construct URL for the component analyses REST API call."""
        return urljoin(self.url,
                       'api/v1/component-analyses/{e}/{c}/{v}'.format(e=ecosystem,
                                                                      c=component,
                                                                      v=version))

    def component_analysis(self, thread_id=None, i=0,
                           ecosystem=None, component=None, version=None):
        url = self.component_analysis_url(ecosystem, component, version)
        response = requests.get(url, headers=self.authorization())
        status_code = response.status_code
        return status_code
