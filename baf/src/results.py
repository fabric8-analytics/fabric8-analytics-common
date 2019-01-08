"""Results gathered from tests."""

from json import dumps


def pretty_print(payload):
    """Perform a pretty printing of the input payload."""
    return dumps(payload, indent=4)


class Results():
    """Class representing results gathered from tests."""

    def __init__(self):
        """Prepare empty result structure."""
        self.tests = []

    def add_test_result(self, test, url, test_result, cause=None, data=None, payload=None,
                        status_code=None):
        """Add new results for a test into all results."""
        result = {}
        result["Test"] = test
        result["Url"] = url
        result["Result"] = str(test_result.name)
        result["Cause"] = cause
        result["Payload"] = payload
        result["Payload_pp"] = pretty_print(payload)
        result["Data"] = data
        result["Status code"] = status_code
        self.tests.append(result)
