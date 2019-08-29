# vim: set fileencoding=utf-8

"""Script to download list of most used Maven packages and generate e2e test template.

Usage: python3 generate_maven_list.py > test.feature
       - generates test for circa 100 most used NPM packages

Requirements:
       - Python3 interpreter (CPython 3.6 or 3.7 is preffered)
       - additional libraries: requests, xmltodict, BeautifulSoup
"""

import sys
import requests
import xmltodict
from bs4 import BeautifulSoup


# template used to format the output
#                ecosystem package  version  sequence number
TEMPLATE = "     | {0:10} | {1:55} | {2:20} | #{3}"


def read_most_popular_components():
    """Read most popular Maven components from the provided HTML page."""
    url = 'https://javalibs.com/charts/dependencies'
    text = requests.get(url).text
    soup = BeautifulSoup(text, "html.parser")
    output = []
    for link in soup.tbody.findAll('br'):
        output.append(link.next_element[5:-4])
    return output


def get_version_for_component(component):
    """Get the version for provided component."""
    c1, c2 = component.split(":")
    c1 = c1.replace(".", "/")
    component = c1 + "/" + c2
    try:
        url = "https://repo1.maven.org/maven2/" + component + "/maven-metadata.xml"
        response = requests.get(url)
        doc = xmltodict.parse(response.text)
        versions = doc["metadata"]["versioning"]["versions"]["version"]
        return versions[-1]
    except Exception as e:
        sys.stderr.write(str(e))
        return None  # for now


if __name__ == '__main__':
    components = read_most_popular_components()

    i = 1

    for component in components:
        version = get_version_for_component(component)
        if version is not None:
            print(TEMPLATE.format("maven", component, version, i))
            i += 1
