#!/bin/env python3

""" Read JSON taken from the stack analysis DB and re-creates pom.xml from the data. """

import sys
import json


def print_header():
    print("""
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.redhat.bayessian.test</groupId>
  <artifactId>test-app-junit-dependency</artifactId>
  <version>1.0</version>
  <dependencies>""")


def print_footer():
    print("""
  </dependencies>
</project>""")


def print_dependency(version, groupId, artifactId):
    print("""
    <dependency>
      <groupId>{groupId}</groupId>
      <artifactId>{artifactId}</artifactId>
      <version>{version}</version>
    </dependency>""".format(groupId=groupId, artifactId=artifactId,
                            version=version))


def json2pom(input):
    print_header()

    dependencies = json.load(input)
    for dependency in dependencies:
        version = dependency["version"]
        name = dependency["name"]
        (groupId, artifactId) = name.split(":")
        print_dependency(version, groupId, artifactId)

    print_footer()


json2pom(sys.stdin)
