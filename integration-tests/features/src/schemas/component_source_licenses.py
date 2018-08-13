"""Component source licenses schema in the S3 database."""

from pytest_voluptuous import S
from voluptuous import Url, Any, Optional

from .predicates import posint_p, posint_zero_p
from .common import AUDIT, STATUS


# see [deployment]-bayesian-core-data/maven/io.vertx.vertx-core

# an example of source licenses metadata stored in S3:

#    {
#      "_audit": {
#        "ended_at": "2017-10-05T14:37:02.970752",
#        "started_at": "2017-10-05T14:34:44.437790",
#        "version": "v1"
#      },
#      "_release": "maven:io.vertx:vertx-core:3.4.1",
#      "details": {
#        "files_count": 426,
#        "licenses": {
#          "Apache 2.0": {
#            "category": "Permissive",
#            "dejacode_url": "https://enterprise.dejacode.com/urn/urn:dje:license:apache-2.0",
#            "homepage_url": "http://www.apache.org/licenses/",
#            "owner": "Apache Software Foundation",
#            "paths": [
#              "io/vertx/core/impl/launcher/commands/ListCommandFactory.java",
#              "io/vertx/core/spi/WebSocketFrameFactory.java",
#              "io/vertx/core/impl/Args.java",
#              "io/vertx/core/Future.java"
#            ],
#            "spdx_license_key": "EPL-1.0",
#            "spdx_url": "https://spdx.org/licenses/EPL-1.0",
#            "text_url": "http://www.eclipse.org/legal/epl-v10.html"
#          },
#          "MIT License": {
#            "category": "Permissive",
#            "dejacode_url": "https://enterprise.dejacode.com/urn/urn:dje:license:mit",
#            "homepage_url": "http://opensource.org/licenses/mit-license.php",
#            "owner": "MIT",
#            "paths": [
#              "io/vertx/core/http/impl/cgbystrom/LICENSE"
#            ],
#            "spdx_license_key": "MIT",
#            "spdx_url": "https://spdx.org/licenses/MIT",
#            "text_url": "http://opensource.org/licenses/mit-license.php"
#          }
#        },
#        "scancode_notice": "Generated with ScanCode and provided on an \"AS IS\" BASIS, ..."
#        "scancode_version": "2.0.1"
#      },
#      "schema": {
#        "name": "source_licenses",
#        "version": "3-0-0"
#      },
#      "status": "success",
#      "summary": {
#        "sure_licenses": [
#          "Apache 2.0",
#          "EPL 1.0",
#          "MIT License"
#        ]
#      }
#    }


# schema version 3.0.0
SCHEMA_3_0_0 = S({"name": "source_licenses",
                 "version": Any("3-0-0")})


# schema version 2.0.0
SCHEMA_2_0_0 = S({"name": "source_licenses",
                 "version": Any("2-0-0")})


DISTINCT_LICENSE = S({"count": posint_p,
                      "license_name": str})


# the schema 2.0.0 is different there
SUMMARY_2_0_0 = S({"all_files": posint_p,
                   "license_files": posint_zero_p,
                   "licensed_files": posint_p,
                   "source_files": posint_p,
                   "distinct_licenses": [DISTINCT_LICENSE],
                   "sure_licenses": [str]})


# list of sure licenses
SUMMARY_3_0_0 = S({"sure_licenses": [str]})


# TODO: add all remaining categories
CATEGORY = Any("Permissive",
               "Copyleft",
               "Copyleft Limited")


LICENSE = S({"category": CATEGORY,
             Optional("dejacode_url"): Url(),
             "homepage_url": Url(),
             "owner": str,
             "paths": [str],
             Optional("reference_url"): Url(),
             "spdx_license_key": str,
             "spdx_url": Any("", Url()),
             "text_url": Any("", Url())})


# a dictionary with licenses
LICENSES = S({str: LICENSE})


# TODO: posint_p or posint_zero_p for empty project?
OSLC_STATS = S({"All files": posint_p,
                "Conflicts (global)": posint_zero_p,
                "Conflicts (ref)": posint_zero_p,
                "Distinct licenses": posint_zero_p,
                "License files": posint_zero_p,
                "Source files": posint_p})


# TODO: posint_p or posint_zero_p?
LICENSE_STATS = S({"count": posint_p,
                   "license_name": str,
                   "variant_id": str})


FILE_2_0_0 = S({"license_name": str,
                Optional("match"): posint_zero_p,
                "variant_id": str})


FILES_2_0_0 = S({"path": str,
                 "result": [FILE_2_0_0]})


DETAILS_2_0_0 = S({"files": [FILES_2_0_0],
                   "license_stats": [LICENSE_STATS],
                   "oslc_stats": OSLC_STATS})


DETAILS_3_0_0 = S({"files_count": posint_p,
                   "licenses": LICENSES,
                   "scancode_notice": str,
                   "scancode_version": str})


# source licenses with schema 3.0.0
COMPONENT_SOURCE_LICENSES_3_0_0_SCHEMA = S({"_audit": Any(None, AUDIT),
                                            Optional("_release"): str,
                                            "schema": SCHEMA_3_0_0,
                                            "status": STATUS,
                                            "summary": SUMMARY_3_0_0,
                                            "details": DETAILS_3_0_0})


# source licenses with schema 2.0.0
COMPONENT_SOURCE_LICENSES_2_0_0_SCHEMA = S({"_audit": Any(None, AUDIT),
                                            Optional("_release"): str,
                                            "schema": SCHEMA_2_0_0,
                                            "status": STATUS,
                                            "summary": SUMMARY_2_0_0,
                                            "details": DETAILS_2_0_0})
