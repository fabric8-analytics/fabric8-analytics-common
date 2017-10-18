from api import *
import time
import datetime
import json


class JobsApi(Api):

    def __init__(self, url, token):
        super().__init__(url, token)

    def authorization(self):
        return {'auth-token': '{token}'.format(token=self.token)}

    def check_auth_token_validity(self):
        endpoint = self.url + 'api/v1/jobs'
        response = requests.get(endpoint, headers=self.authorization())
        if response.status_code != 200:
            self.print_error_response(response, "detail")
        return response.status_code == 200
