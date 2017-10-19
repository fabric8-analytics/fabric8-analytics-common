"""Configuration for the connection to the S3."""
import os


class S3Configuration:
    """Class representing configuration for the connection to the S3."""

    def __init__(self):
        """Construct the configuration structure from the environment variables."""
        self.access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        self.secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.region_name = os.environ.get('S3_REGION_NAME')
