"""Component code metrics schema in the S3 database."""

from pytest_voluptuous import S, Partial, Exact
from voluptuous import Invalid, Url, Any, Optional
from voluptuous.validators import All, Length

from .predicates import *
from .common import *


# see [deployment]-bayesian-core-data/maven/io.vertx.vertx-core

# an example of code metrics metadata stored in S3:

#    {
#      "_audit": {
#        "ended_at": "2017-05-15T19:30:25.922925",
#        "started_at": "2017-05-15T19:30:21.262559",
#        "version": "v1"
#      },
#      "_release": "maven:io.vertx:vertx-core:3.0.0",
#      "details": {
#        "languages": [
#          {
#            "blank_lines": 0,
#            "code_lines": 8,
#            "comment_lines": 0,
#            "files_count": 1,
#            "language": "JSON"
#          },
#          {
#            "blank_lines": 5809,
#            "code_lines": 26108,
#            "comment_lines": 18981,
#            "files_count": 309,
#            "language": "Java",
#            "metrics": {
#              "functions": {
#                "average_cyclomatic_complexity": 1.31,
#                "average_javadocs": 0.48,
#                "function": [
#                  {
#                    "cyclomatic_complexity": 1,
#                    "javadocs": 0,
#                    "name": "examples.BufferExamples.example1()"
#                  },
#                  {
#                    "classes": 0,
#                    "functions": 2,
#                    "javadocs": 2,
#                    "name": "io.vertx.core.VoidHandler"
#                  }
#                ]
#              },
#              "packages": {
#                "classes": 227,
#                "functions": 2048,
#                "javadoc_lines": 7401,
#                "javadocs": 1195,
#                "multi_comment_lines": 8277,
#                "single_comment_lines": 78
#              }
#            }
#          }
#        ]
#      },
#      "schema": {
#        "name": "code_metrics",
#        "version": "1-0-0"
#      },
#      "status": "success",
#      "summary": {
#        "blank_lines": 5809,
#        "code_lines": 26116,
#        "comment_lines": 18981,
#        "total_files": 310,
#        "total_lines": 50906
#      }
#    }


SCHEMA = S({"name": "code_metrics",
            "version": Any("1-0-0")})


SUMMARY = S({"blank_lines": posint_p,
             "code_lines": posint_p,
             "comment_lines": posint_p,
             "total_files": posint_p,
             "total_lines": posint_p})


DETAILS = S({"languages": list})


# code metrics metadata for component (not package)
COMPONENT_CODE_METRICS_SCHEMA = S({"_audit": Any(None, AUDIT),
                                   Optional("_release"): str,
                                   "schema": SCHEMA,
                                   "status": STATUS,
                                   "summary": SUMMARY,
                                   "details": DETAILS})
