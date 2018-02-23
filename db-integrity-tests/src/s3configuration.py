"""Configuration for the connection to the S3."""
import os


class S3Configuration:
    """Class representing configuration for the connection to the S3."""

    def __init__(self):
        """Construct the configuration structure from the environment variables."""
        self.access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        self.secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.region_name = os.environ.get('S3_REGION_NAME')
        # optional
        self.deployment_prefix = os.environ.get('DEPLOYMENT_PREFIX')

        # check if all required environment variables have been set

        assert self.access_key_id is not None, \
            "Please set up AWS_ACCESS_KEY_ID environment variable"

        assert self.secret_access_key is not None, \
            "Please set up AWS_SECRET_ACCESS_KEY_ID environment variable"

        assert self.region_name is not None, \
            "Please set up S3_REGION_NAME environment variable"
