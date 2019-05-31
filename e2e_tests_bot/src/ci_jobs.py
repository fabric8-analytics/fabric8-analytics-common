"""Simple and dirty Jenkins interface."""

from urllib.parse import urljoin

from fastlog import log
import requests


def construct_job_url(url_prefix, url_suffix):
    """Construct the URL to job on CI from CI prefix and suffix with job name."""
    return urljoin(urljoin(url_prefix, "job/"), url_suffix)


def remove_prefix(text, prefixes):
    """Remove the prefix from input string (if the string starts with prefix)."""
    for prefix in prefixes:
        if text.startswith(prefix):
            return text[len(prefix):]
    return text


def jenkins_api_query_build_statuses(jenkins_url):
    """Construct API query to Jenkins (CI)."""
    return "{url}/api/json?tree=builds[result,number]".format(url=jenkins_url)


def log_builds(last_build, total_builds_cnt, success_builds_cnt):
    """Log informations about builds found."""
    with log.indent():
        log.info("Last build: {n}".format(n=last_build))
        log.info("Total builds: {n}".format(n=total_builds_cnt))
        log.info("Success builds: {n}".format(n=success_builds_cnt))


def get_total_builds(builds):
    """Get number of all builds."""
    return [b for b in builds if b["result"] is not None]


def get_success_builds(builds):
    """Get number of success builds."""
    return [b for b in builds if b["result"] == "SUCCESS"]


def read_build_history(job_url):
    """Read total number of remembered builds and succeeded builds as well."""
    log.info("Read build history")
    with log.indent():
        api_query = jenkins_api_query_build_statuses(job_url)
        log.info(api_query)
        response = requests.get(api_query)
        builds = response.json()["builds"]

        last_build_info = builds[0]
        last_build = int(last_build_info["number"])
        last_build_status = last_build_info["result"]

        # None, True, False
        if last_build_status is not None:
            last_build_status = last_build_status == "SUCCESS"

        total_builds = get_total_builds(builds)
        success_builds = get_success_builds(builds)
        total_builds_cnt = len(total_builds)
        success_builds_cnt = len(success_builds)

        log_builds(last_build, total_builds_cnt, success_builds_cnt)

        log.success("Done")
    return last_build, last_build_status, total_builds_cnt, success_builds_cnt


def read_build_cause(job_url, build_id):
    """Read cause why the e2e job has been started."""
    api_query = job_url + "/" + str(build_id) + "/api/json"
    response = requests.get(api_query)
    actions = response.json()["actions"]

    cause = None
    for action in actions:
        if "_class" in action and action["_class"] == "hudson.model.CauseAction":
            cause = action["causes"][0]

    # None or real build cause
    return cause


def read_changes(jenkins_url, build_url, build_id):
    """Read changes for the cause why the e2e job has been started."""
    api_query = "{jenkins}/{job}{build}/api/json".format(jenkins=jenkins_url,
                                                         job=build_url, build=build_id)
    response = requests.get(api_query)
    payload = response.json()
    cause = payload["actions"][0]["causes"][0]["shortDescription"]

    changes = ""
    changeSetItems = payload["changeSet"]["items"]
    if changeSetItems:
        for changeSetItem in changeSetItems:
            changes += changeSetItem["date"] + ": " + changeSetItem["authorEmail"] + ": " + \
                       changeSetItem["comment"]
    else:
        changes = "No changes detected"
    return cause, changes
