"""Configuration for the Dashboard."""
from server_configuration import ServerConfiguration
from s3_configuration import S3Configuration


class Configuration():
    """Class representing configuration for the Dashboard."""

    def __init__(self):
        """Construct the configuration structure."""
        self.stage = ServerConfiguration('STAGE')
        self.prod = ServerConfiguration('PROD')
        self.s3 = S3Configuration()

    def __repr__(self):
        """Return string representation for the configuration object."""
        return "Stage: {s}\nProd: {p}\nS3: {d}".format(s=self.stage, p=self.prod, d=self.s3)
