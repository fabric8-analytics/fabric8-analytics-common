# vim: set fileencoding=utf-8

"""Script to download list of most used PyPi packages and generate e2e test template.

Usage: python3 generate_pypi_list.py > test.feature
       - generates test for circa 1000 most used PyPi packages

       python3 generate_pypi_list.py 100 > test.feature
       - generates test for N most used PyPi packages (N=100 in this example)

Requirements:
       - Python3 interpreter (CPython 3.6 or 3.7 is preffered)
       - the `yolk3k` package needs to be installed
         (pip3 install --user yolk3k)
"""

import requests
import subprocess
import sys
import csv


# base URL of GitHub resource with list of most used PyPi packages
BASE_URL = "https://raw.githubusercontent.com/pypy/pypy.packages/master/"

PYPI_PACKAGES_URL = BASE_URL + "downloads.csv"

# template used to format the output
#                ecosystem package  version  sequence number
TEMPLATE = "     | {0:10} | {1:19} | {2:20} | #{3}"


def download_pypi_list(url):
    """Download list of most used PyPi packages."""
    return requests.get(url).text


def read_pypi_list(url, download):
    """Read PyPi list either from provided URL or from the text file (cache)."""
    if download:
        raw_pypi_list = download_pypi_list(PYPI_PACKAGES_URL)
        with open("raw_pypi_list.csv", "w") as fout:
            fout.write(raw_pypi_list)

    lst = []
    with open("raw_pypi_list.csv") as fin:
        csv_reader = csv.reader(fin)
        # skip the first line that contains header
        next(csv_reader)
        for row in csv_reader:
            lst.append(row)
    return lst


def filter_component_names(raw_pypi_list):
    """Filter the raw PYPI list to get list of proper component names."""
    components = []
    for record in raw_pypi_list:
        components.append(record[0])
    return components


def process_component(component, i):
    """Process selected component - generate list of E/P/V for it."""
    out = subprocess.run(["yolk", "-M", component, "-f", "version"], stdout=subprocess.PIPE)
    version = out.stdout.strip().decode("utf-8")
    print(TEMPLATE.format("pypi", component, version, i))


def process_components(components):
    """Process all provided components."""
    i = 1
    for component in components:
        process_component(component, i)
        i += 1


def process_pypi_list(url, n, download):
    """Process PYPI componennts."""
    raw_pypi_list = read_pypi_list(url, download)
    components = filter_component_names(raw_pypi_list)

    # use at most N components
    if len(components) > n:
        components = components[:n]

    process_components(components)


if __name__ == '__main__':
    n = 1000
    # process CLI arguments
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    process_pypi_list(PYPI_PACKAGES_URL, n, download=True)
