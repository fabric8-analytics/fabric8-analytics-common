from server_configuration import *
from s3_configuration import *


class Configuration():

    def __init__(self):
        self.stage = ServerConfiguration('STAGE')
        self.prod = ServerConfiguration('PROD')
        self.s3 = S3Configuration()

    def __repr__(self):
        return "Stage: {s}\nProd: {p}\nS3: {d}".format(s=self.stage, p=self.prod, d=self.s3)
