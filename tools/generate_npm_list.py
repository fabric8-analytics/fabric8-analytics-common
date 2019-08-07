# vim: set fileencoding=utf-8

"""Script to download list of most used NPM packages and generate e2e test template.

Usage: python3 generate_npm_list.py > test.feature
       - generates test for circa 1000 most used NPM packages

       python3 generate_npm_list.py 100 > test.feature
       - generates test for N most used NPM packages (N=100 in this example)

Requirements:
       - Python3 interpreter (CPython 3.6 or 3.7 is preffered)
       - the `npm` tool needs to be installed
"""

import requests
import re
import subprocess
import sys


# base URL of GitHub gist with list of most used NPM packages
BASE_URL = "https://gist.githubusercontent.com/anvaka/"

# commit hash - it will probably change in the future
COMMIT_HASH = "8e8fa57c7ee1350e3491/raw/27c81e27e0ebd7331db1fd1ecf14f2179530c083/"
NPM_PACKAGES_URL = BASE_URL + COMMIT_HASH + "01.most-dependent-upon.md"

# template used to format the output
#                ecosystem package  version  sequence number
TEMPLATE = "     | {0:10} | {1:19} | {2:20} | #{3}"


def download_npm_list(url):
    """Download list of most used NPM packages."""
    return requests.get(url).text


def read_npm_list(url, download):
    """Read NPM list either from provided URL or from the text file (cache)."""
    if download:
        raw_npm_list = download_npm_list(NPM_PACKAGES_URL)
        with open("raw_npm_list.txt", "w") as fout:
            fout.write(raw_npm_list)
    else:
        with open("raw_npm_list.txt", "r") as fin:
            raw_npm_list = fin.read()
    return raw_npm_list


def is_proper_component_name(component):
    """Check if the component name is properly formatted."""
    return "@" not in component and "/" not in component


def filter_component_names(raw_npm_list):
    """Filter the raw NPM list to get list of proper component names."""
    pattern = re.compile("^[0-9]+.")
    components = []
    for line in raw_npm_list.splitlines():
        if pattern.match(line):
            try:
                i1 = line.index("[")
                i2 = line.index("]")
                component = line[i1+1:i2]
                if is_proper_component_name(component):
                    components.append(component)
                else:
                    print("Ingoring the following component:", component)
            except Exception as e:
                print("Ignoring line:", line)
    return components


def install_component(component):
    """Install selected component locally."""
    print("Installing component", component)
    subprocess.run(["npm", "install", component])


def install_components(components):
    """Install all provided components."""
    for component in components:
        install_component(component)


def process_component(component, i):
    """Process selected component - generate list of E/P/V for it."""
    out = subprocess.run(["npm", "show", component, "version"], stdout=subprocess.PIPE)
    version = out.stdout.strip().decode("utf-8")
    print(TEMPLATE.format("npm", component, version, i))


def process_components(components):
    """Process all provided components."""
    i = 1
    for component in components:
        process_component(component, i)
        i += 1


def process_npm_list(url, n, download):
    """Process NPM componennts."""
    raw_npm_list = read_npm_list(url, download)
    components = filter_component_names(raw_npm_list)

    # use at most N components
    if len(components) > n:
        components = components[:n]

    # install_components(components)
    process_components(components)


if __name__ == '__main__':
    n = 1000
    # process CLI arguments
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    process_npm_list(NPM_PACKAGES_URL, n, download=False)
