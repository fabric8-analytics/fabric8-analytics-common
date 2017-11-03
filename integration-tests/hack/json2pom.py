#!/bin/env python3

"""Read JSON taken from the stack analysis DB and re-creates pom.xml from the data."""

import sys
import json


def print_header():
    """Print the header for the pom.xml manifest file."""
    print("""
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.redhat.bayessian.test</groupId>
  <artifactId>test-app-junit-dependency</artifactId>
  <version>1.0</version>
  <dependencies>""")


def print_footer():
    """Print the footer for the pom.xml manifest file."""
    print("""
  </dependencies>
</project>""")


def print_dependency(version, groupId, artifactId):
    """Add one dependency into the pom.xml manifest file."""
    print("""
    <dependency>
      <groupId>{groupId}</groupId>
      <artifactId>{artifactId}</artifactId>
      <version>{version}</version>
    </dependency>""".format(groupId=groupId, artifactId=artifactId,
                            version=version))


def json2pom(input):
    """Transform the given JSON input file into the project file."""
    print_header()

    dependencies = json.load(input)

    # transform all dependencies found in the source JSON file
    for dependency in dependencies:
        version = dependency["version"]
        name = dependency["name"]
        assert version
        assert name
        (groupId, artifactId) = name.split(":")
        print_dependency(version, groupId, artifactId)

    print_footer()


json2pom(sys.stdin)
