"""Component digests schema in the S3 database."""

from pytest_voluptuous import S, Partial, Exact
from voluptuous import Invalid, Url, Any, Optional
from voluptuous.validators import All, Length

from .predicates import *
from .common import *


# see [deployment]-bayesian-core-data/maven/io.vertx.vertx-core


# an example of digests metadata stored in S3:

#    {
#      "_audit": {
#        "ended_at": "2017-05-15T19:30:03.497703",
#        "started_at": "2017-05-15T19:29:43.603343",
#        "version": "v1"
#      },
#      "_release": "maven:io.vertx:vertx-core:3.0.0",
#      "details": [
#        {
#          "md5": "43812a9fd6a3bda6b433953e2fdf3856",
#          "path": "io/vertx/core/net/impl/NetClientImpl.class",
#          "sha1": "edeffbfc7d8df7efb0b4cae2886053275e24af35",
#          "sha256": "cf5f9077726835f02728f4245db9c826c666c82f495605d66be1068cd3e18cba",
#          "ssdeep":
# "192:5DvQUTllITeemQb9HqzoLd6MQ1qyfEYleMr6Wu5B6RcoLfCUb+rbwWdPdNAI:2mmTecbBg3ERMXuKiufCUaXwWVdNAI"
#        },
#        {
#          "md5": "3e5f1334c1eb22833706b7ee0816e7ef",
#          "path": "io/vertx/core/net/impl/NetServerImpl$1.class",
#          "sha1": "9708554c725a45a5fec6a80c0dc21635dcfa09bf",
#          "sha256": "60f9f27f39f8abf78b4614705db2251962f4adc648fe94ac57442d0da87859e4",
#          "ssdeep":
# "48:b4JI5nl7CgvSLgjSg3ig3tg1HaA7R/6yg3Agon1pg5gBgZJk/f/gWLog5owaTU:0Jal7CtLkSNo4H7R/6ybrpGocK/MBwaY"
#        },
#        {
#          "md5": "e8cd690cb53c843af46d35cceb674720",
#          "path": "io/vertx/core/streams/impl/PumpImpl.class",
#          "sha1": "0934b98c49b7ed44156dfb5f7db8db539c880de3",
#          "sha256": "3c0a4f9195903ebfc267f285c59821ce115d0fd5d180dc98fcfbd37244dce464",
#          "ssdeep":
# "96:5H93rpVrlGhVqGKdD4CbEDxqZJpB8ybIeDqUnoAgOw:5d3rp1lGhoGKdD4CbEeXxIe20oAgOw"
#        },
#        {
#          "md5": "1b6fb37af0ebe9fdb8d062a861269b20",
#          "path": "vertx-java/template/cheatsheet.templ",
#          "sha1": "c4e0474c267bbf0970c81a6d31fb86e93f2c5f51",
#          "sha256": "8367510076d6cefc11b3a4207e09d2d84c1bde2acc8334b430bbaeea805dd987",
#          "ssdeep":
# "48:uX06RkW2tXtkC1tEKEVamPizQWjD3Dy/YtIwx:K/8oC1KKwamPirBtHx"
#        },
#        {
#          "md5": "220d3874ac21e6461e3edbe692cbfbdf",
#          "path": "vertx-java/template/common-lib.templ",
#          "sha1": "9f9a50536c4f4a4136e4727045ba2ab271f3c1ff",
#          "sha256": "e15a2bcce5c49018d3dcf8436a78dc39581ef4747c624c79956aa3b20910e03b",
#          "ssdeep":
# "48:uxYZdxeXlONqrWHPcXxaKqEzy82quGbNX9++cVp3tyaiciQxxYXqNqPWVL+eX5:UIdxeXlONqwPwaLyX9+19yainQxxWqN/"
#        },
#        {
#          "artifact": true,
#          "md5": "780002937700aa49b7df345aec80105c",
#          "path": "vertx-core-3.0.0.jar",
#          "sha1": "72bb3e2f4e3128874c864a83b740a256ac840efa",
#          "sha256": "dd8fc9b005c4ca8bd526a32ef6f2c5d5c6eb1153dc6badb2a40f15dc10db1f7b",
#          "ssdeep":
# "12288:FLJrFmihAExJPo65Fu1PYQ8HCZS/9yoDgOufa+FpuqnqBGbRke:/Fm+NJb5Fu1PYQ2Cs8SLOE8ke"
#        }
#      ],
#      "schema": {
#        "name": "digests",
#        "version": "1-0-0"
#      },
#      "status": "success",
#      "summary": []
#    }

SCHEMA = S({"name": "digests",
            "version": Any("1-0-0")})


SUMMARY = S(list)


DETAIL = S({Optional("artifact"): bool,
            "md5": md5_p,
            "path": str,
            "sha1": str,
            "sha256": str,
            "ssdeep": str})


DETAILS = S([DETAIL])


# digests schema for component (not package)
COMPONENT_DIGESTS_SCHEMA = S({"_audit": Any(None, AUDIT),
                              "_release": str,
                              "details": DETAILS,
                              "schema": SCHEMA,
                              "status": STATUS,
                              "summary": SUMMARY})
