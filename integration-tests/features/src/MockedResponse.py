"""Supports for mocking data for tests."""
import json


class MockedResponse():
    """Class that provides mocked data used by tests.

    The json() method allow us to use this class to mock HTTP responses.
    """

    def __init__(self, filename):
        """Load given JSON file and parse it."""
        self.content = MockedResponse.json_load(filename)

    def json(self):
        """Return a content read in constructor.

        It allow us to use this class to mock HTTP responses.
        """
        return self.content

    @staticmethod
    def json_load(filename):
        """Load and parse JSON file."""
        with open(filename) as data_file:
            return json.load(data_file)
