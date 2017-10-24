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
    total = 0

    with open(filename) as fin:
        for line in fin:
            line = line.rstrip()
            if line.endswith(".py"):
                source = line.strip()
            if line.endswith("    Pass"):
                if source:
                    passed += 1
                    total += 1
                    files[source] = True
            if line.endswith("    Fail"):
                if source:
                    failed += 1
                    total += 1
                    files[source] = False
    return {"files": files,
            "total": total,
            "passed": passed,
            "failed": failed,
            "failed%": percentage(passed, failed)}


def parse_pylint_results(repository):
    return parse_linter_results(repository + ".linter")


def parse_docstyle_results(repository):
    return parse_linter_results(repository + ".pydocstyle")


def parse_line_count(line):
    line = line.strip()
    line_count, filename = line.split(" ")
    # remove prefix that is not relevant much
    if filename.startswith("./"):
        filename = filename[len("./"):]
    return int(line_count), filename


def get_source_files(repository):
    command = ("pushd {repo}; wc -l `find . -path ./venv -prune -o -name '*.py' -print` " +
               "| head -n -1 > ../{repo}.count;popd").format(repo=repository)
    os.system(command)
    filenames = []
    line_counts = {}
    total_lines = 0
    count = 0

    with open("{repo}.count".format(repo=repository)) as fin:
        for line in fin:
            count += 1
            line_count, filename = parse_line_count(line)
            filenames.append(filename)
            line_counts[filename] = line_count
            total_lines += line_count

    return {"count": count,
            "filenames": filenames,
            "line_counts": line_counts,
            "total_lines": total_lines}


def update_overall_status(results, repository):
    remarks = ""
    status = False

    source_files = results.source_files[repository]["count"]
    linter_checks = results.repo_linter_checks[repository]
    docstyle_checks = results.repo_docstyle_checks[repository]

    linter_checks_total = linter_checks["total"]
    docstyle_checks_total = docstyle_checks["total"]

    if source_files == linter_checks_total and \
       source_files == docstyle_checks_total:
        if linter_checks["failed"] == 0 and docstyle_checks["failed"] == 0:
            status = True
    else:
        remarks = "not all source files are checked"
        if linter_checks_total != docstyle_checks_total:
            remarks += ", linter checked {n1} files, but pydocstyle checked {n2} files".format(
                n1=linter_checks_total, n2=docstyle_checks_total)

    results.overall_status[repository] = status
    results.remarks[repository] = remarks


def delete_work_files(repository):
    """Cleanup the CWD from the work files used to analyze given repository."""
    os.remove("{repo}.count".format(repo=repository))
    os.remove("{repo}.linter".format(repo=repository))
    os.remove("{repo}.pydocstyle".format(repo=repository))


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

    results.repositories = repositories

    # clone repositories + run pylint + run docstyle script + accumulate results
    for repository in repositories:
        clone_repository(repository)
        run_pylint(repository)
        run_docstyle_check(repository)

        results.source_files[repository] = get_source_files(repository)
        results.repo_linter_checks[repository] = parse_pylint_results(repository)
        results.repo_docstyle_checks[repository] = parse_docstyle_results(repository)

        delete_work_files(repository)
        update_overall_status(results, repository)

    generate_dashboard(results)


if __name__ == "__main__":
    # execute only if run as a script
    main()
