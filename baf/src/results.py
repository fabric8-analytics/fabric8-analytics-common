"""Results gathered from tests."""


class Results():
    """Class representing results gathered from tests."""

    def __init__(self):
        """Prepare empty result structure."""
        self.tests = []

    def add_test_result(self, test, test_result, cause=None, data=None, payload=None):
        """Add new results for a test into all results."""
        result = {}
        result["Test"] = test
        result["Result"] = str(test_result)
        result["Cause"] = cause
        result["Payload"] = payload
        result["Data"] = data
        self.tests.append(result)
