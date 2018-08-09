"""Package toplevel schema in the S3 database."""

from pytest_voluptuous import S

from .predicates import *
from .common import *


# see [deployment]-bayesian-core-data/maven/io.vertx.vertx-core

# an example of package toplevel metadata stored in S3:

#    {
#      "analyses": [],
#      "finished_at": "2018-04-17T19:41:29.956490",
#      "id": 12648,
#      "package_id": 12,
#      "started_at": "2018-04-17T19:25:46.216090"
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


PACKAGE_TOPLEVEL_SCHEMA = S({"analyses": ANALYSES,
                             "id": posint_p,
                             "package_id": posint_p,
                             "started_at": timestamp_p,
                             "finished_at": timestamp_p})
