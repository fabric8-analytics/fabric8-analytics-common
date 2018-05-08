"""Package libraries.io schema in the S3 database."""

from pytest_voluptuous import S, Partial, Exact
from voluptuous import Invalid, Url, Any, Optional
from voluptuous.validators import All, Length

from .predicates import *
from .common import *


# see [deployment]-bayesian-core-package-data/maven/io.vertx.vertx-core

# an example of libraries.io metadata stored in S3:

#    {
#      "_audit": {
#        "ended_at": "2018-04-17T19:30:38.106694",
#        "started_at": "2018-04-17T19:30:37.095370",
#        "version": "v1"
#      },
#      "_release": "maven:io.vertx:vertx-core:None",
#      "details": {
#        "dependent_repositories": {
#          "count": 6262
#        },
#        "dependents": {
#          "count": 150
#        },
#        "releases": {
#          "count": 48,
#          "recent": [
#            {
#              "number": "3.3.0.CR2",
#              "published_at": "2016-06-14T09:17:32.000Z"
#            },
#            {
#              "number": "3.3.0",
#              "published_at": "2016-06-22T21:55:40.000Z"
#            },
#            {
#              "number": "3.3.1",
#              "published_at": "2016-07-07T21:01:22.000Z"
#            },
#            {
#              "number": "3.3.2",
#              "published_at": "2016-07-10T14:05:18.000Z"
#            },
#            {
#              "number": "3.3.3",
#              "published_at": "2016-09-08T15:23:27.000Z"
#            },
#            {
#              "number": "3.4.0.Beta1",
#              "published_at": "2017-02-05T21:47:35.000Z"
#            },
#            {
#              "number": "3.4.0",
#              "published_at": "2017-03-06T20:06:22.000Z"
#            },
#            {
#              "number": "3.4.1",
#              "published_at": "2017-03-15T13:46:59.000Z"
#            },
#            {
#              "number": "3.4.2",
#              "published_at": "2017-06-14T19:18:42.000Z"
#            },
#            {
#              "number": "3.5.0.Beta1",
#              "published_at": "2017-08-07T14:54:22.000Z"
#            }
#          ]
#        }
#      },
#      "schema": {
#        "name": "libraries_io",
#        "version": "2-0-0"
#      },
#      "status": "success",
#      "summary": []
#    }


# currently supported schema(s)
SCHEMA = S({"name": "libraries_io",
            "version": "2-0-0"})


# libraries.io details
DETAILS = S({"dependent_repositories": dict,
             "dependents": dict,
             "releases": dict})


# libraries.io schema for package (not component)
PACKAGE_LIBRARIES_IO_SCHEMA = S({"_audit": Any(None, AUDIT),
                                 "_release": str,
                                 "schema": SCHEMA,
                                 "status": STATUS,
                                 "summary": [str],
                                 "details": DETAILS})
