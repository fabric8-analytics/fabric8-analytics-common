"""Reproducer for the issue https://github.com/openshiftio/openshift.io/issues/2012."""

import requests

URL = "http://STAGE_DATABASE"


def gremlin_search_package_in_ecosystem(ecosystem, package):
    """Search packages from the selected ecosystem."""
    query = 'g.V().has("ecosystem", "{ecosystem}").has("name", "{package}")'.\
        format(ecosystem=ecosystem, package=package)
    print(query)
    data = post_query(query)
    try:
        print("*** " + package + " ***")
        assert data["result"]["data"] is not None
        properties = data["result"]["data"][0]["properties"]
        if "latest_version" in properties:
            latest_version = properties["latest_version"][0]["value"]
            if latest_version == "":
                print("latest_version: EMPTY!")
                print()
                return 1
            else:
                print("latest_version: {v}".format(v=latest_version))
                print()
                return 0
        else:
            print("latest_version attribute does not exist!!!")
            print()
            return 1
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
    "array-differ",
    "array-flatten",
    "array-reduce",
    "array-slice",
    "array-union",
    "array-uniq",
    "array-unique",
    "lodash",
    "lodash.assign",
    "lodash.assignin",
    "lodash._baseuniq",
    "lodash.bind",
    "lodash.camelcase",
    "lodash.clonedeep",
    "lodash.create",
    "lodash._createset",
    "lodash.debounce",
    "lodash.defaults",
    "lodash.filter",
    "lodash.findindex",
    "lodash.flatten",
    "lodash.foreach",
    "lodash.isplainobject",
    "lodash.mapvalues",
    "lodash.memoize",
    "lodash.mergewith",
    "lodash.once",
    "lodash.pick",
    "lodash._reescape",
    "lodash._reevaluate",
    "lodash._reinterpolate",
    "lodash.reject",
    "lodash._root",
    "lodash.some",
    "lodash.tail",
    "lodash.template",
    "lodash.union",
    "lodash.without",
    "npm",
    "underscore"
]


errors = 0
for package in packages:
    errors += gremlin_search_package_in_ecosystem("npm", package)

print("Found {n} errors in {p} packages".format(n=errors, p=len(packages)))
