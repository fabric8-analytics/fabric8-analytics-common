from api import *


class JobsApi(Api):

    def __init__(self, url):
        super().__init__(url)

    def authorization(self):
        return {'auth-token': '{token}'.format(token=self.token)}
