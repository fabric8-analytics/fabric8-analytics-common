"""Component dependency snapshot schema in the S3 database."""

from pytest_voluptuous import S
from voluptuous import Any, Optional

from .predicates import *
from .common import *


# see [deployment]-bayesian-core-data/maven/io.vertx.vertx-core


# an example of dependency snapshot metadata stored in S3:

#    {
#      "_audit": {
#        "ended_at": "2017-05-15T19:32:13.442347",
#        "started_at": "2017-05-15T19:32:13.429106",
#        "version": "v1"
#      },
#      "_release": "maven:io.vertx:vertx-core:3.0.0",
#      "details": {
#        "runtime": [
#          {
#            "declaration": "io.netty:netty-codec-http 4.0.28.Final",
#            "ecosystem": "maven",
#            "name": "io.netty:netty-codec-http",
#            "resolved_at": "2017-05-15T19:32:13.437819",
#            "version": "4.0.28.Final"
#          },
#          {
#            "declaration": "io.netty:netty-common 4.0.28.Final",
#            "ecosystem": "maven",
#            "name": "io.netty:netty-common",
#            "resolved_at": "2017-05-15T19:32:13.441035",
#            "version": "4.0.28.Final"
#          },
#          {
#            "declaration": "io.netty:netty-transport 4.0.28.Final",
#            "ecosystem": "maven",
#            "name": "io.netty:netty-transport",
#            "resolved_at": "2017-05-15T19:32:13.441353",
#            "version": "4.0.28.Final"
#          },
#          {
#            "declaration": "org.slf4j:slf4j-api 1.7.7",
#            "ecosystem": "maven",
#            "name": "org.slf4j:slf4j-api",
#            "resolved_at": "2017-05-15T19:32:13.441676",
#            "version": "1.7.7"
#          },
#          {
#            "declaration": "com.fasterxml.jackson.core:jackson-databind 2.5.3",
#            "ecosystem": "maven",
#            "name": "com.fasterxml.jackson.core:jackson-databind",
#            "resolved_at": "2017-05-15T19:32:13.441998",
#            "version": "2.5.3"
#          }
#        ]
#      },
#      "schema": {
#        "name": "dependency_snapshot",
#        "version": "1-0-0"
#      },
#      "status": "success",
#      "summary": {
#        "dependency_counts": {
#          "runtime": 11
#        },
#        "errors": []
#      }
#    }


SCHEMA = S({"name": "dependency_snapshot",
            "version": Any("1-0-0")})


SUMMARY = S({"dependency_counts": dict,
             "errors": list})


RUNTIME = S({"declaration": str,
             "ecosystem": ECOSYSTEM,
             "name": str,
             "resolved_at": timestamp_p,
             "version": str})


DETAILS = S({"runtime": [RUNTIME]})


# dependency snapshot metadata for component (not package)
COMPONENT_DEPENDENCY_SNAPSHOT_SCHEMA = S({"_audit": Any(None, AUDIT),
                                          Optional("_release"): str,
                                          "schema": SCHEMA,
                                          "status": STATUS,
                                          "summary": SUMMARY,
                                          "details": DETAILS})
