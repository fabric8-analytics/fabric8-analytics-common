"""Component keywords tagging schema in the S3 database."""

from pytest_voluptuous import S
from voluptuous import Any, Optional

from .common import AUDIT, STATUS


# see [deployment]-bayesian-core-data/maven/io.vertx.vertx-core


# an example of keywords tagging metadata stored in S3:

#    {
#      "_audit": {
#        "ended_at": "2018-04-17T19:25:34.516494",
#        "started_at": "2018-04-17T19:25:31.643800",
#        "version": "v1"
#      },
#      "_release": "maven:io.vertx:vertx-core:3.5.1",
#      "details": {
#        "description": {},
#        "keywords": []
#      },
#      "schema": {
#        "name": "keywords_tagging",
#        "version": "1-0-0"
#      },
#      "status": "success",
#      "summary": []
#    }


SCHEMA = S({"name": "keywords_tagging",
            "version": Any("1-0-0")})


SUMMARY = S(list)


DETAILS = S({"description": dict,
             "keywords": Any(list, None)})


# keywords tagging schema for component (not package)
COMPONENT_KEYWORDS_TAGGING_SCHEMA = S({"_audit": Any(None, AUDIT),
                                       Optional("_release"): str,
                                       "schema": SCHEMA,
                                       "status": STATUS,
                                       "summary": SUMMARY,
                                       "details": DETAILS})
