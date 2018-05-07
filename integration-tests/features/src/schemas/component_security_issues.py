"""Component security issues schema in the S3 database."""

from pytest_voluptuous import S, Partial, Exact
from voluptuous import Invalid, Url, Any, Optional
from voluptuous.validators import All, Length

from .predicates import *
from .common import *


# see [deployment]-bayesian-core-data/maven/io.vertx.vertx-core


# an example of security issues metadata stored in S3:

#    {
#      "_audit": {
#        "ended_at": "2017-05-15T19:29:48.215012",
#        "started_at": "2017-05-15T19:29:34.588837",
#        "version": "v1"
#      },
#      "_release": "maven:io.vertx:vertx-core:3.0.0",
#      "details": [],
#      "schema": {
#        "name": "security_issues",
#        "version": "3-0-0"
#      },
#      "status": "success",
#      "summary": []
#    }


SCHEMA = S({"name": "security_issues",
            "version": Any("3-0-0", "3-0-1")})


SUMMARY = S(list)


DETAILS = S(list)


# security issues schema for component (not package)
COMPONENT_SECURITY_ISSUES_SCHEMA = S({"_audit": Any(None, AUDIT),
                                      Optional("_release"): str,
                                      "schema": SCHEMA,
                                      "status": STATUS,
                                      "summary": SUMMARY,
                                      "details": DETAILS})
