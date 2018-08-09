"""Reproducer for the issue https://github.com/openshiftio/openshift.io/issues/1619."""

import requests

URL = "http://STAGE_DATABASE"


def gremlin_search_package_in_ecosystem(ecosystem, package):
    """Search packages from the selected ecosystem."""
    query = 'g.V().has("ecosystem", "{ecosystem}").has("name", "{package}").out("has_version")'.\
        format(ecosystem=ecosystem, package=package)
    print(query)
    data = post_query(query)
    try:
        print("*** " + package + " ***")
        assert data["result"]["data"] is not None
        for e in data["result"]["data"]:
            print(e["label"])
        print()
    except Exception as e:
        print("none")


def post_query(query):
    """Post the query to the Gremlin."""
    data = {"gremlin": str(query)}
    response = requests.post(URL, json=data)
    # print(response.status_code)
    data = response.json()
    return data


packages = [
    "sequence",
    "array-differ"
]


for package in packages:
    gremlin_search_package_in_ecosystem("npm", package)
