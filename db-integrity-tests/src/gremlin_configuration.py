"""Configuration for the connection to the Gremlin service."""
import os


class GremlinConfiguration:
    """Class representing configuration for the connection to the Gremlin service."""

    def __init__(self):
        """Construct the configuration structure from the environment variables."""
        self.url = os.environ.get('F8A_GREMLIN_URL')

        # check if the required environment variable has been set

        assert self.url is not None, \
            "Please set up F8A_GREMLIN_URL environment variable"
