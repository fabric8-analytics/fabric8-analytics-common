"""The main module of the e2e test checker."""

from fastlog import log

from config import Config
from ci_jobs import read_build_history, read_build_cause, read_changes
from mm_client import login_and_send_message


def read_last_processed():
    """Read last processed build number."""
    with open("last_processed", "r") as fin:
        return int(fin.readline())


def write_last_processed(last_build):
    """Write last processed build number."""
    with open("last_processed", "w") as fin:
        return fin.write("{n}".format(n=last_build))


def construct_message(jenkins_url, master_build_url, last_build, last_build_status,
                      build_cause, cause, changes):
    """Construct message to be send to Mattermost."""
    if last_build_status:
        message = "Master e2e job has finished with success status!\n"
    else:
        message = "Master e2e job has failed!\n"
    message += "Build number {n}\n".format(n=last_build)
    message += "Job log {u}{n}/console\n".format(u=master_build_url, n=last_build)
    message += "Upstream project: {u}\n".format(u=build_cause["upstreamProject"])
    message += "Upstream build: {n}\n".format(n=build_cause["upstreamBuild"])
    message += "Upstream log: {j}{u}{n}/console\n".format(j=jenkins_url,
                                                          u=build_cause["upstreamUrl"],
                                                          n=build_cause["upstreamBuild"])
    message += "Cause: {c}\n".format(c=cause)
    message += "Changes:\n{c}\n".format(c=changes)
    return message.strip()


def process_new_build(config, last_build, last_build_status, jenkins_url, master_build_url):
    """Process new detected build."""
    if last_build_status is not None:
        if last_build_status:
            log.info("And the last build is OK")
        else:
            log.error("And the last build failed!")
        build_cause = read_build_cause(master_build_url, last_build)
        if build_cause is not None:
            cause, changes = read_changes(jenkins_url, build_cause["upstreamUrl"],
                                          build_cause["upstreamBuild"])
            message = construct_message(jenkins_url, master_build_url,
                                        last_build, last_build_status,
                                        build_cause, cause, changes)
            log.info("Sending message:")
            log.warning(message)
            login_and_send_message(config.get_mm_url(),
                                   config.get_mm_user_login(), config.get_mm_user_password(),
                                   config.get_mm_team(), config.get_mm_channel(),
                                   message)
    else:
        log.info("Still building")


def main():
    """Entry point to the QA Dashboard."""
    log.setLevel(log.INFO)

    log.info("Started")

    with log.indent():
        log.info("Setup")
        config = Config()
        jenkins_url = config.get_jenkins_url()
        master_build_url = jenkins_url + config.get_master_build_job()
        log.success("Setup done")

    last_processed_build = read_last_processed()

    log.info("Last processed build: {n}".format(n=last_processed_build))

    last_build, last_build_status, total_builds_cnt, success_builds_cnt = \
        read_build_history(master_build_url)

    if last_build >= last_processed_build:
        log.info("New build(s) detected!")
        with log.indent():
            process_new_build(config, last_build, last_build_status, jenkins_url, master_build_url)

        write_last_processed(last_build)
    else:
        log.info("No new build(s) detected...")


if __name__ == "__main__":
    # execute only if run as a script
    main()
