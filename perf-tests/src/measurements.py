from s3interface import *
from duration import *


def read_component_analysis_from_core_data(s3, ecosystem, component, version):
    bucket = "bayesian-core-data"

    durations = {}

    key = s3.component_key(ecosystem, component, version)
    data = s3.read_object(bucket, key)
    durations["overall"] = Duration.from_data(data)

    analyses = data.get("analyses")

    # Remove this analysis because it is not performed on component-version level
    analyses.remove("github_details")
    # analyses.remove("code_metrics")

    for analysis in analyses:
        key = s3.component_analysis_key(ecosystem, component, version, analysis)
        data = s3.read_object(bucket, key)
        durations[analysis] = Duration.from_audit(data)

    return durations


def read_component_analysis_from_core_package(s3, ecosystem, component):
    bucket = "bayesian-core-package-data"

    durations = {}

    key = s3.component_core_package_data_key(ecosystem, component)
    data = s3.read_object(bucket, key)
    durations["overall"] = Duration.from_data(data)

    # we have to specify analysis manually here
    analyses = ["github_details", "keywords_tagging", "libraries_io"]

    for analysis in analyses:
        key = s3.component_core_package_data_analysis_key(ecosystem, component, analysis)
        data = s3.read_object(bucket, key)
        durations[analysis] = Duration.from_audit(data)

    return durations


def read_component_analysis_audit_duration(s3, ecosystem, component, version):
    return {"core-data":
            read_component_analysis_from_core_data(s3, ecosystem, component, version),
            "core-package-data":
            read_component_analysis_from_core_package(s3, ecosystem, component)}
