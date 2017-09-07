from api import *


class JobsApi(Api):

    def __init__(self, url, token):
        super().__init__(url, token)

    def authorization(self):
        return {'auth-token': '{token}'.format(token=self.token)}
