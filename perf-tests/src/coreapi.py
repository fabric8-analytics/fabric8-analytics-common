from api import *


class CoreApi(Api):

    def __init__(self, url):
        super().__init__(url)

    def authorization(self):
        return {'Authorization': 'Bearer {token}'.format(token=self.token)}
