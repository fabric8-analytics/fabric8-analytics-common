"""Component metadata schema in the S3 database."""

from pytest_voluptuous import S
from voluptuous import Url, Any, Optional

from .common import AUDIT, STATUS


# see [deployment]-bayesian-core-data/maven/io.vertx.vertx-core


# an example of componetn metadata stored in S3:

#    {
#      "_audit": {
#        "ended_at": "2017-05-15T19:31:10.078349",
#        "started_at": "2017-05-15T19:30:48.199773",
#        "version": "v1"
#      },
#      "_release": "maven:io.vertx:vertx-core:3.0.0",
#      "details": [
#        {
#          "code_repository": {
#            "type": "unknown",
#            "url": "git@github.com:eclipse/vert.x.git"
#          },
#          "declared_license":
# "The Apache Software License, Version 2.0, Eclipse Public License - v 1.0",
#          "dependencies": [
#            "io.netty:netty-codec-http 4.0.28.Final",
#            "log4j:log4j 1.2.17",
#            "io.vertx:vertx-codegen 3.0.0",
#            "io.netty:netty-handler 4.0.28.Final",
#            "com.fasterxml.jackson.core:jackson-core 2.5.3",
#            "io.netty:netty-buffer 4.0.28.Final",
#
# ... shortened...
#
#            "io.vertx:vertx-docgen 3.0.0",
#            "io.netty:netty-common 4.0.28.Final",
#            "io.netty:netty-transport 4.0.28.Final",
#            "org.slf4j:slf4j-api 1.7.7",
#            "com.fasterxml.jackson.core:jackson-databind 2.5.3"
#          ],
#          "description":
# "Sonatype helps open source projects to set up Maven repositories on https://oss.sonatype.org/",
#          "devel_dependencies": [
#            "junit:junit 4.11",
#            "org.apache.directory.server:apacheds-protocol-dns 1.5.7"
#          ],
#          "ecosystem": "java-pom",
#          "homepage":
# "http://nexus.sonatype.org/oss-repository-hosting.html/vertx-parent/vertx-core",
#          "name": "Vert.x Core",
#          "version": "3.0.0"
#        }
#      ],
#      "schema": {
#        "name": "metadata",
#        "version": "3-1-0"
#      },
#      "status": "success",
#      "summary": []
#    }


SCHEMA = S({"name": "metadata",
            "version": Any("3-1-0", "3-2-0", "3-3-0")})


SUMMARY = S(list)


CODE_REPOSITORY = S({"type": str,
                     "url": str})  # Url()}) # Url does not seem to support git@...


DETAIL = S({Optional("code_repository"): CODE_REPOSITORY,
            Optional("declared_license"): str,
            Optional("declared_licenses"): [str],
            Optional("dependencies"): [str],
            Optional("description"): Any(None, str),
            Optional("devel_dependencies"): [str],
            Optional("ecosystem"): str,
            Optional("homepage"): Url(),
            Optional("name"): str,
            Optional("version"): str})


DETAILS = S([DETAIL])


# metadata schema for component (not package)
COMPONENT_METADATA_SCHEMA = S({"_audit": Any(None, AUDIT),
                               Optional("_release"): str,
                               "schema": SCHEMA,
                               "status": STATUS,
                               "summary": SUMMARY,
                               "details": DETAILS})
