"""Component toplevel schema in the S3 database."""

from pytest_voluptuous import S
from voluptuous import Any, Optional

from .predicates import *
from .common import *


# see [deployment]-bayesian-core-data/maven/io.vertx.vertx-core

# an example of component toplevel metadata stored in S3:

#    {
#      "analyses": [
#        "keywords_tagging",
#        "dependency_snapshot",
#        "source_licenses",
#        "metadata",
#        "digests",
#        "security_issues"
#      ],
#      "audit": null,
#      "dependents_count": -1,
#      "ecosystem": "maven",
#      "finished_at": "2018-04-17T19:26:52.862359",
#      "id": 326448,
#      "package": "io.vertx:vertx-core",
#      "package_info": {
#        "dependents_count": -1,
#        "relative_usage": "not used"
#      },
#      "release": "maven:io.vertx:vertx-core:3.5.1",
#      "started_at": "2018-04-17T19:23:07.615107",
#      "subtasks": null,
#      "version": "3.5.1"
#    }


ANALYSES = S(["keywords_tagging",
              "dependency_snapshot",
              "source_licenses",
              "metadata",
              "digests",
              "security_issues",
              "languages",
              "binary_data",
              "crypto_algorithms",
              "code_metrics",
              "redhat_downstream",
              "github_details"])


COMPONENT_TOPLEVEL_SCHEMA = S({"analyses": ANALYSES,
                               Optional("_audit"): Any(None, AUDIT),
                               "audit": Any(None, str),
                               "dependents_count": int,
                               "ecosystem": ECOSYSTEM,
                               "started_at": timestamp_p,
                               "finished_at": timestamp_p,
                               "id": int,
                               "package": str,
                               "package_info": dict,
                               Optional("_release"): str,
                               "release": str,
                               Optional("latest_version"): Any(None, str),
                               "subtasks": Any(None, str),
                               "version": str}, required=True)
