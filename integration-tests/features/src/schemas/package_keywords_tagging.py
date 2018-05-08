"""Package keywords tagging schema in the S3 database."""

from pytest_voluptuous import S, Partial, Exact
from voluptuous import Invalid, Url, Any, Optional
from voluptuous.validators import All, Length

from .predicates import *
from .common import *


# see [deployment]-bayesian-core-package-data/maven/io.vertx.vertx-core


# see [deployment]-bayesian-core-data/maven/io.vertx.vertx-core

# an example of keywords tagging metadata stored in S3:

#    {
#      "_audit": {
#        "ended_at": "2018-04-17T19:39:49.245875",
#        "started_at": "2018-04-17T19:33:15.124772",
#        "version": "v1"
#      },
#      "_release": "maven:io.vertx:vertx-core:None",
#      "details": {
#        "README": {
#          "access": 1.0,
#          "alpn": 0.0,
#          "applicative": 1.6437451970367156e-152,
#          "artifact": 1.633364297778037e-229,
#          "browser": 1.0,
#          "bsd": 1.3642892449336676e-106,
#          "build": 1.0,
#          "classpath": 1.0,
#          "components": 1.0,
#          "configure": 1.0,
#          "core": 1.0,
#          "directive": 1.0,
#          "http": 1.0,
#          "include": 1.0,
#          "integrity": 1.4395073438152264e-224,
#          "jvm": 1.0,
#          "linux": 1.0,
#          "logged": 0.0,
#          "low-level": 1.2848356779569426e-65,
#          "native": 1.0,
#          "packages": 1.0,
#          "phase": 5.206058656821496e-262,
#          "properties": 1.0,
#          "repository": 1.0,
#          "run-configuration": 0.0,
#          "sockets": 1.0,
#          "system": 1.0,
#          "system-properties": 3.1407427235077263e-242,
#          "tcp": 1.0,
#          "test": 5.206058656821496e-262,
#          "transport": 1.5976425669017134e-241,
#          "verify": 4.856793410885697e-79,
#          "vert.x": 1.0,
#          "vertx": 0.0,
#          "website": 1.0
#        },
#        "gh_topics": [
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
#        ],
#        "package_name": {
#          "core": 1.0,
#          "io": 1.0,
#          "vertx": 5.6658564596684805e-304
#        }
#      },
#      "schema": {
#        "name": "package_keywords_tagging",
#        "version": "1-0-0"
#      },
#      "status": "success",
#      "summary": []
#    }

SCHEMA = S({"name": "package_keywords_tagging",
            "version": Any("1-0-0")})


SUMMARY = S(list)


DETAILS = S({"package_name": dict,  # str + posfloat
             "gh_topics": [str],
             "README": dict})


# keywords tagging schema for package (not component)
PACKAGE_KEYWORDS_TAGGING_SCHEMA = S({"_audit": Any(None, AUDIT),
                                     "_release": str,
                                     "schema": SCHEMA,
                                     "status": STATUS,
                                     "summary": SUMMARY,
                                     "details": DETAILS})
