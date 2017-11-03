"""Module with functions that read data and metadata from the S3 and retrieve durations."""

from s3interface import *
from duration import *
from botocore.exceptions import *


def read_component_analysis_from_core_data(s3, ecosystem, component, version):
    """Read component analysis from the core data and retrieve duration info from it."""
    bucket = "bayesian-core-data"

    durations = {}

    key = s3.component_key(ecosystem, component, version)
    data = s3.read_object(bucket, key)
    durations["overall"] = Duration.from_data(data)

    analyses = data.get("analyses")

    # Remove this analysis because it is not performed on component-version level
    if "github_details" in analyses:
        analyses.remove("github_details")
    # analyses.remove("code_metrics")

    for analysis in analyses:
        key = s3.component_analysis_key(ecosystem, component, version, analysis)
        try:
            data = s3.read_object(bucket, key)
            durations[analysis] = Duration.from_audit(data)
        except ClientError:
            print("Warning: duration for the following analysis won't be "
                  "be computed: {a}".format(a=analysis))

    return durations


def read_component_analysis_from_core_package(s3, ecosystem, component):
    """Read component analysis from core package data and retrieve duration info from it."""
    bucket = "bayesian-core-package-data"

    durations = {}

    key = s3.component_core_package_data_key(ecosystem, component)
    data = s3.read_object(bucket, key)
    durations["overall"] = Duration.from_data(data)

    # we have to specify analysis manually here
    analyses = ["git_stats", "github_details", "keywords_tagging", "libraries_io"]

    for analysis in analyses:
        key = s3.component_core_package_data_analysis_key(ecosystem, component, analysis)
        try:
            data = s3.read_object(bucket, key)
            durations[analysis] = Duration.from_audit(data)
        except ClientError:
            print("Warning: duration for the following analysis won't be "
                  "be computed: {a}".format(a=analysis))

    return durations


def read_component_analysis_audit_duration(s3, ecosystem, component, version):
    """Read durations for the core data and core package data as well."""
    return {"core-data":
            read_component_analysis_from_core_data(s3, ecosystem, component, version),
            "core-package-data":
            read_component_analysis_from_core_package(s3, ecosystem, component)}
