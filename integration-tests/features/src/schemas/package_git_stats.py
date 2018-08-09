"""Package git stats schema in the S3 database."""

from pytest_voluptuous import S
from voluptuous import Any, Optional

from .predicates import *
from .common import *


# see [deployment]-bayesian-core-data/maven/io.vertx.vertx-core

# an example of git stats metadata stored in S3:

#    {
#      "_audit": {
#        "ended_at": "2018-04-17T19:31:03.522623",
#        "started_at": "2018-04-17T19:30:38.836564",
#        "version": "v1"
#      },
#      "_release": "maven:io.vertx:vertx-core:None",
#      "details": {
#        "master": {
#          "month": {
#            "average_changes": [
#              12.301136363636363,
#              8.409090909090908
#            ],
#            "commit_count": 82,
#            "committer_count": 9,
#            "newest_commit": 1523901558,
#            "oldest_commit": 1521561510,
#            "trend": 0.6,
#            "trend_status": "increasing"
#          },
#          "organizations": [
#            "braintags.de",
#            "ca.ibm.com",
#            "creativeprogramming.it"
#          ],
#          "overall": {
#            "average_changes": [
#              31.919922334666982,
#              21.981172040480114
#            ],
#            "commit_count": 3387,
#            "committer_count": 137,
#            "newest_commit": 1523901558,
#            "oldest_commit": 1375369856,
#            "trend": 0.011340104037651722,
#            "trend_status": "calm"
#          },
#          "year": {
#            "average_changes": [
#              15.317827298050139,
#              12.039275766016713
#            ],
#            "commit_count": 678,
#            "committer_count": 38,
#            "newest_commit": 1523901558,
#            "oldest_commit": 1492707362,
#            "trend": 0.05194208227993566,
#            "trend_status": "calm"
#          }
#        }
#      },
#      "status": "success",
#      "summary": []
#    }


# see https://github.com/fabric8-analytics/fabric8-analytics-worker/blob/master/f8a_worker/
# workers/git_stats.py#L80
TREND_STATUS = S(Any("increasing", "decreasing", "calm"))


STATS = S({"average_changes": [float],
           "commit_count": posint_zero_p,
           "committer_count": posint_zero_p,
           "newest_commit": posint_p,
           "oldest_commit": posint_p,
           "trend": posfloat_p,
           "trend_status": TREND_STATUS})


MASTER = S({"organizations": [str],
            "overall": STATS,
            "month": STATS,
            "year": STATS})


DETAILS = S({"master": MASTER})


# git stats schema for package (not component)
PACKAGE_GIT_STATS_SCHEMA = S({"_audit": Any(None, AUDIT),
                              Optional("_release"): str,
                              # "schema": dict,
                              "status": STATUS,
                              "summary": [str],
                              "details": DETAILS})
