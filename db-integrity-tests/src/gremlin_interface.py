"""Interface to the Gremlin database."""


import requests


class GremlinInterface:
    """Interface to the Gremlin database."""

    def __init__(self, gremlinConfiguration):
        """Initialize the Gremlin interface object."""
        self.configuration = gremlinConfiguration

    def post_query(self, query):
        """Post the already constructed query to the Gremlin."""
        data = {"gremlin": str(query)}
        return requests.post(self.configuration.url, json=data)
