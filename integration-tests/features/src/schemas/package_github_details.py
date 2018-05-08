"""Package GitHub details schema in the S3 database."""

from pytest_voluptuous import S, Partial, Exact
from voluptuous import Invalid, Url, Any, Optional
from voluptuous.validators import All, Length

from .predicates import *
from .common import *


# see [deployment]-bayesian-core-data/maven/io.vertx.vertx-core

# an example of GitHub details metadata stored in S3:

#    {
#      "_audit": {
#        "ended_at": "2018-04-17T19:30:39.802408",
#        "started_at": "2018-04-17T19:30:37.214113",
#        "version": "v1"
#      },
#      "_release": "maven:io.vertx:vertx-core:None",
#      "details": {
#        "contributors_count": 30,
#        "forks_count": 1343,
#        "last_year_commits": {
#          "sum": 602,
#          "weekly": [
#            31,
#            14,
#            ... shortede here ...
#            14,
#            18,
#            29,
#            8
#          ]
#        },
#        "license": {
#          "key": "other",
#          "name": "Other",
#          "spdx_id": null,
#          "url": null
#        },
#        "open_issues_count": 153,
#        "stargazers_count": 7719,
#        "subscribers_count": 595,
#        "topics": [
#          "concurrency",
#          "event-loop",
#          "high-performance",
#          "http2",
#          "java",
#          "jvm",
#          "netty",
#          "nio",
#          "non-blocking",
#          "reactive",
#          "vertx"
#        ]
#      },
#      "schema": {
#        "name": "github_details",
#        "version": "2-0-1"
#      },
#      "status": "success",
#      "summary": []
#    }


# schema(s) for GitHub details metadata
SCHEMA = S({"name": "github_details",
            "version": "2-0-1"})


# TODO: weekly -> sum checks
LAST_YEAR_COMMITS = S({"sum": posint_zero_p,
                       "weekly": [posint_zero_p]})


# info about license(s)
LICENSE = S({"key": str,
             "name": str,
             "spdx_id": Any(None, str),
             "url": Any(None, Url)})


# GitHub details
DETAILS = S({"contributors_count": posint_zero_p,
             "forks_count": posint_zero_p,
             "last_year_commits": LAST_YEAR_COMMITS,
             "open_issues_count": posint_zero_p,
             "stargazers_count": posint_zero_p,
             "subscribers_count": posint_zero_p,
             "topics": [str],
             "license": LICENSE})


# GitHub details schema for package (not component)
PACKAGE_GITHUB_DETAILS_SCHEMA = S({"_audit": Any(None, AUDIT),
                                   "_release": str,
                                   "schema": SCHEMA,
                                   "status": STATUS,
                                   "summary": [str],
                                   "details": DETAILS})
