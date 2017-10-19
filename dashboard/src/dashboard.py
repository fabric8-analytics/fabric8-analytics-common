import json
import time
import datetime
import os
import sys
import requests

from coreapi import *
from jobsapi import *
from configuration import *
from results import *
from html_generator import *


def check_environment_variable(env_var_name):
    print("Checking: {e} environment variable existence".format(
        e=env_var_name))
    if env_var_name not in os.environ:
        print("Fatal: {e} environment variable has to be specified"
              .format(e=env_var_name))
        sys.exit(1)
    else:
        print("    ok")


def check_environment_variables():
    environment_variables = [
        "F8A_API_URL_STAGE",
        "F8A_API_URL_PROD",
        "F8A_JOB_API_URL_STAGE",
        "F8A_JOB_API_URL_PROD",
        "RECOMMENDER_API_TOKEN_STAGE",
        "RECOMMENDER_API_TOKEN_PROD",
        "JOB_API_TOKEN_STAGE",
        "JOB_API_TOKEN_PROD",
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "S3_REGION_NAME"]
    for environment_variable in environment_variables:
        check_environment_variable(environment_variable)


def check_system(core_api, jobs_api):
    # try to access system endpoints
    print("Checking: core API and JOBS API endpoints")
    core_api_available = core_api.is_api_running()
    jobs_api_available = jobs_api.is_api_running()

    if core_api_available and jobs_api_available:
        print("    ok")
    else:
        print("    Fatal: tested system is not available")

    # check the authorization token for the core API
    print("Checking: authorization token for the core API")
    core_api_auth_token = core_api.check_auth_token_validity()

    if core_api_auth_token:
        print("    ok")
    else:
        print("    error")

    # check the authorization token for the jobs API
    print("Checking: authorization token for the jobs API")
    jobs_api_auth_token = jobs_api.check_auth_token_validity()

    if jobs_api_auth_token:
        print("    ok")
    else:
        print("    error")

    return {"core_api_available": core_api_available,
            "jobs_api_available": jobs_api_available,
            "core_api_auth_token": core_api_auth_token,
            "jobs_api_auth_token": jobs_api_auth_token}


repositories = [
    "fabric8-analytics-common",
    "fabric8-analytics-server",
    "fabric8-analytics-worker",
    "fabric8-analytics-jobs",
    "fabric8-analytics-tagger",
    "fabric8-analytics-stack-analysis",
    "fabric8-analytics-license-analysis",
    "fabric8-analytics-data-model",
    "fabric8-analytics-recommender"
]


def clone_repository(repository):
    prefix = "https://github.com/fabric8-analytics"
    command = "git clone --single-branch --depth 1 {prefix}/{repo}.git".format(prefix=prefix,
                                                                               repo=repository)
    os.system(command)


def run_pylint(repository):
    command = "pushd {repo};./run-linter.sh > ../{repo}.linter;popd".format(repo=repository)
    os.system(command)


def run_docstyle_check(repository):
    command = "pushd {repo};./check-docstyle.sh > ../{repo}.pydocstyle;popd".format(repo=repository)
    os.system(command)


def percentage(passed, failed):
    total = passed + failed
    if total == 0:
        return "0"
    perc = 100.0 * failed / total
    return "{:.0f}".format(perc)


def parse_linter_results(filename):
    source = None

    files = {}
    passed = 0
    failed = 0

    with open(filename) as fin:
        for line in fin:
            if line.endswith(".py\n"):
                source = line.strip()
            if line.endswith("    Pass\n"):
                if source:
                    passed += 1
                    files[source] = True
            if line.endswith("    Fail\n"):
                if source:
                    failed += 1
                    files[source] = False
    return {"files": files,
            "passed": passed,
            "failed": failed,
            "failed%": percentage(passed, failed)}


def parse_pylint_results(results, repository):
    results.repo_linter_checks[repository] = parse_linter_results(repository + ".linter")


def parse_docstyle_results(results, repository):
    results.repo_docstyle_checks[repository] = parse_linter_results(repository + ".pydocstyle")


def get_source_files(results, repository):
    command = "pushd {repo}; wc -l `find . -name '*.py' -print` | head -n -1 " + \
              "> ../{repo}.count;popd".format(repo=repository)
    os.system(command)
    files = {}
    count = 0

    with open("{repo}.count".format(repo=repository)) as fin:
        for line in fin:
            count += 1

    results.source_files[repository] = {"count": count}


def main():
    check_environment_variables()
    results = Results()

    cfg = Configuration()

    core_api = CoreApi(cfg.stage.core_api_url, cfg.stage.core_api_token)
    jobs_api = JobsApi(cfg.stage.jobs_api_url, cfg.stage.jobs_api_token)
    results.stage = check_system(core_api, jobs_api)

    core_api = CoreApi(cfg.prod.core_api_url, cfg.prod.core_api_token)
    jobs_api = JobsApi(cfg.prod.jobs_api_url, cfg.prod.jobs_api_token)
    results.production = check_system(core_api, jobs_api)

    check_system(core_api, jobs_api)

    results.repositories = repositories

    # clone repositories + run pylint + run docstyle script + accumulate results
    for repository in repositories:
        clone_repository(repository)
        run_pylint(repository)
        run_docstyle_check(repository)
        get_source_files(results, repository)
        parse_pylint_results(results, repository)
        parse_docstyle_results(results, repository)

    generate_dashboard(results)


if __name__ == "__main__":
    # execute only if run as a script
    main()
