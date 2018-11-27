"""The main module of the QA Dashboard."""
import json
import datetime
import os
import sys
import requests

from fastlog import log

from config import Config
from repositories import Repositories
from ci_jobs import CIJobs


ci_job_types = [
    "test_job",
    "build_job",
    "pylint_job",
    "pydoc_job"
]

JENKINS_URL = "https://ci.centos.org"
JOBS_STATUSES_FILENAME = "jobs.json"

FAILURE_THRESHOLD = 5


def read_jobs_statuses(filename):
    """Deserialize statuses for all jobs from the JSON file."""
    with open(filename) as fin:
        return json.load(fin)["jobs"]


def store_jobs_statuses(filename, data):
    """Serialize statuses of all jobs into the JSON file."""
    with open(filename, "w") as fout:
        fout.write(data)


def jenkins_api_query_job_statuses(jenkins_url):
    """Construct API query to Jenkins (CI)."""
    return "{url}/api/json?tree=jobs[name,color]".format(url=jenkins_url)


def jenkins_api_query_build_statuses(jenkins_url):
    """Construct API query to Jenkins (CI)."""
    return "{url}/api/json?tree=builds[result]".format(url=jenkins_url)


def jobs_as_dict(raw_jobs):
    """Construct a dictionary with job name as key and job status as value."""
    return dict((job["name"], job["color"]) for job in raw_jobs if "color" in job)


def read_ci_jobs_statuses(jenkins_url):
    """Read statuses of all jobs from the Jenkins (CI)."""
    api_query = jenkins_api_query_job_statuses(jenkins_url)
    response = requests.get(api_query)
    raw_jobs = response.json()["jobs"]
    return jobs_as_dict(raw_jobs)


def read_job_statuses(ci_jobs):
    """Read job statuses from the CI, but only if its necessary."""
    log.info("Read job statuses")
    return read_ci_jobs_statuses(JENKINS_URL)


def main():
    """Entry point to the QA Dashboard."""
    log.setLevel(log.INFO)
    log.info("Setup")
    with log.indent():
        config = Config()
        repositories = Repositories(config)

    log.success("Setup done")

    ci_jobs = CIJobs()

    job_statuses = read_job_statuses(ci_jobs)

    with log.indent():
        for repository in repositories.repolist:

            for job_type in ci_job_types:
                with log.indent():
                    url = ci_jobs.get_job_url(repository, job_type)
                    name = ci_jobs.get_job_name(repository, job_type)
                    badge = ci_jobs.get_job_badge(repository, job_type)
                    job_status = job_statuses.get(name)

                    if url is not None:
                        api_query = jenkins_api_query_build_statuses(url)
                        response = requests.get(api_query)
                        builds = response.json()["builds"]
                        failures = 0
                        for b in builds:
                            if b["result"] != "SUCCESS":
                                failures += 1
                            else:
                                break
                        if failures >= FAILURE_THRESHOLD:
                            print("Repository: {}".format(repository))
                            print("URL to job: {}".format(url))
                            print("Failures:   {}".format(failures))
                            print()

    log.success("Data prepared")


if __name__ == "__main__":
    # execute only if run as a script
    main()
