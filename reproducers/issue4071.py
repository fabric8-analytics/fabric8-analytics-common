"""Reproducer for the issue https://github.com/openshiftio/openshift.io/issues/4071."""

import requests

URL = "https://license-analysis.api.prod-preview.openshift.io/api/v1/license-recommender"


def call_license_recommender(url, payload):
    """Call the license-recommender endpoint."""
    response = requests.post(url, data=payload)
    print(response.status_code)
    print(response.text)


payloads = [
    "issue4071_wrong_input_missing_ecosystem",
    "issue4071_wrong_input_missing_package_name_and_version",
    "issue4071_wrong_input_missing_package_name",
    "issue4071_wrong_input_missing_package_version",
    "issue4071_wrong_input_missing_resolved"
]


for payload_name in payloads:
    with open(payload_name + ".json") as payload:
        call_license_recommender(URL, payload)
