"""Reproducer for the issue https://github.com/openshiftio/openshift.io/issues/1619."""

import requests

URL = "http://STAGE_DATABASE"


def gremlin_search_packages_for_the_ecosystem(ecosystem=None):
    """Search packages from the selected ecosystem."""
    ecosystem = ecosystem if ecosystem is not None else "npm"
    for i in range(0, 1697):
        # get just the name of the package
        query = 'g.V().has("pecosystem", ecosystem)[{i}].value("pname")'.format(i=i)
        name = post_query(query)["result"]["data"][0]

        # now try to get all attributes
        query = 'g.V().has("pecosystem", "npm")[{i}]'.format(i=i)
        data = post_query(query)
        try:
            # try to access metadata returned when there's no exception
            x = data["result"]["data"][0]
            assert x
        except Exception:
            print(name)


def post_query(query):
    """Post the query to the Gremlin."""
    data = {"gremlin": query}
    response = requests.post(URL, json=data)
    return response.json()


gremlin_search_packages_for_the_ecosystem("npm")
