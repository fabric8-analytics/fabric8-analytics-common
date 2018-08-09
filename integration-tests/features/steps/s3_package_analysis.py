"""Definitions of tests for packages metadata stored in the AWS S3 database."""
from behave import then, when
from src.attribute_checks import *
from src.s3interface import *
import time


@then('I should find the correct GitHub details metadata for package {package} '
      'from ecosystem {ecosystem}')
def check_github_details_file(context, package, ecosystem):
    """Check all relevant attributes stored in the JSON with GitHub details."""
    data = context.s3_data

    check_audit_metadata(data)
    check_release_attribute(data, ecosystem, package)
    check_status_attribute(data)

    check_attribute_presence(data, "summary")
    check_attribute_presence(data, "details")

    check_schema_attribute(data, "github_details", "2-0-1")


@then('I should find empty details about GitHub repository')
def check_empty_github_details(context):
    """Check that the details about GitHub repository are empty."""
    details = get_details_node(context)
    assert not details, "Empty 'details' node is expected"


@then('I should find the correct keywords tagging metadata for package {package} '
      'from ecosystem {ecosystem}')
def check_keywords_tagging_file(context, package, ecosystem):
    """Check that the tagging metadata are correct for given package and ecosystem."""
    data = context.s3_data

    check_audit_metadata(data)
    check_release_attribute(data, ecosystem, package)
    check_status_attribute(data)

    details = get_details_node(context)
    check_attribute_presence(details, "package_name")
    check_attribute_presence(details, "repository_description")


@then('I should find the weight for the word {word} in the {where}')
def check_weight_for_word_in_keywords_tagging(context, word, where):
    """Check that the given word and its weight can be found in the tagging report."""
    selector = S3Interface.selector_to_key(where)
    assert selector in ["package_name", "repository_description", "description"]

    details = get_details_node(context)
    word_dict = check_and_get_attribute(details, selector)

    check_attribute_presence(word_dict, word)
    assert float(word_dict[word]) > 0.0


@then('I should find the correct libraries io metadata for package {package} '
      'from ecosystem {ecosystem}')
def check_libraries_io_file(context, package, ecosystem):
    """Check the content of package metadata taken from libaries.io."""
    data = context.s3_data

    check_audit_metadata(data)
    check_release_attribute(data, ecosystem, package)
    check_status_attribute(data)


@then('I should find that the latest package version {version} was published on {date}')
def check_latest_package_version_publication(context, version, date):
    """Check the latest package version and publication date."""
    releases = _get_releases_node_from_libraries_io(context)

    latest_release = check_and_get_attribute(releases, 'latest')

    check_attribute_presence(latest_release, "version")
    check_attribute_presence(latest_release, "published_at")

    stored_version = latest_release["version"]
    stored_date = latest_release["published_at"]

    assert stored_version == version, \
        "Package latest version differs, {v} is expected, but {f} is found instead".\
        format(v=version, f=stored_version)

    assert latest_release["published_at"] == date, \
        "Package latest release data differs, {d} is expected, but {f} is found instead".\
        format(d=date, f=stored_date)


def _get_releases_node_from_libraries_io(context):
    details = get_details_node(context)

    return check_and_get_attribute(details, 'releases')


@then('I should find that the recent package version {version} was published on {date}')
def check_recent_package_version_publication(context, version, date):
    """Check the release date for selected package version."""
    releases = _get_releases_node_from_libraries_io(context)

    # TODO: update together with https://github.com/openshiftio/openshift.io/issues/1040
    latest_release = check_and_get_attribute(releases, 'latest')

    recent_releases = check_and_get_attribute(latest_release, 'recent')

    # try to find the exact version published at given date
    for v, published_at in recent_releases.items():
        if v == version and date == published_at:
            return

    # nothing was found
    raise Exception('Can not find the package recent version {v} published at {d}'.format(
        v=version, d=date))


@then('I should find {expected_count:d} releases for this package')
def check_releases_count(context, expected_count):
    """Check the number of releases for given package."""
    releases = _get_releases_node_from_libraries_io(context)

    releases_count = check_and_get_attribute(releases, 'count')

    assert int(releases_count) == expected_count, \
        "Expected {e} releases, but found {f}".format(e=expected_count, f=releases_count)


@then('I should find {expected_repo_count:d} dependent repositories for this package')
def check_dependent_repositories_count(context, expected_repo_count):
    """Check the number of dependent repositories for given package."""
    details = get_details_node(context)

    dependent_repositories = check_and_get_attribute(details, 'dependent_repositories')

    repo_count = check_and_get_attribute(dependent_repositories, 'count')

    assert int(repo_count) == expected_repo_count, \
        "Expected {e} repositories, but found {f} instead".format(e=expected_repo_count,
                                                                  f=repo_count)


@then('I should find {expected_dependents_count:d} dependent projects for this package')
def check_dependents_count(context, expected_dependents_count):
    """Check the number of dependend projects for given package."""
    details = get_details_node(context)

    dependents = check_and_get_attribute(details, 'dependents')

    dependents_count = check_and_get_attribute(dependents, 'count')

    assert int(dependents_count) == expected_dependents_count, \
        "Expected {e} dependents, but found {f} instead".format(e=expected_dependents_count,
                                                                f=dependents_count)


@when('I read {selector} metadata for the package {package} in ecosystem '
      '{ecosystem} from the AWS S3 database bucket {bucket}')
def read_core_package_data_from_bucket(context, selector, package, ecosystem, bucket):
    """Read the selected metadata for the package."""
    # At this moment, the following selectors can be used:
    # package toplevel
    # GitHub details
    # keywords tagging
    # libraries io
    if selector == "package toplevel":
        key = S3Interface.package_key(ecosystem, package)
    else:
        metadata = S3Interface.selector_to_key(selector)
        key = S3Interface.package_analysis_key(ecosystem, package, metadata)

    try:
        s3_data = context.s3interface.read_object(bucket, key)
        assert s3_data is not None
        context.s3_data = s3_data
    except Exception as e:
        m = "Can not read {key} for the E/P {ecosystem} {package} from bucket {bucket}"\
            .format(key=key, ecosystem=ecosystem, package=package, bucket=bucket)
        raise Exception(m) from e
        context.s3_data = None


@then('I should find the correct package toplevel metadata for package {package} '
      'from ecosystem {ecosystem}')
def check_package_toplevel_file(context, package, ecosystem):
    """Check the content of package toplevel file."""
    data = context.s3_data

    check_attribute_presence(data, 'id')
    assert int(data['id'])

    check_attribute_presence(data, 'package_id')
    assert int(data['package_id'])

    check_attribute_presence(data, 'analyses')

    check_attribute_presence(data, 'started_at')
    check_timestamp(data['started_at'])

    check_attribute_presence(data, 'finished_at')
    check_timestamp(data['finished_at'])

    # none - no tests can be done for the 'ecosystem' ATM - there's no info about ecosystem
    # in the package toplevel metadata


@when('I remember timestamps from the last component toplevel metadata')
def remember_timestamps_from_job_toplevel_data(context):
    """Remember the timestamps for the package analysis."""
    data = context.s3_data
    context.job_timestamp_started_at = data['started_at']
    context.job_timestamp_finished_at = data['finished_at']

    # print("\n\nRemember")
    # print(context.job_timestamp_started_at)
    # print(context.job_timestamp_finished_at)


@then('I should find that timestamps from current toplevel metadata are newer than '
      'remembered timestamps')
def check_new_timestamps(context):
    """Check the timestamps for the package analysis."""
    data = context.s3_data

    # print("\n\nCurrent")
    # print(data['started_at'])
    # print(data['finished_at'])

    check_attribute_presence(data, 'started_at')
    check_timestamp(data['started_at'])

    check_attribute_presence(data, 'finished_at')
    check_timestamp(data['finished_at'])

    remembered_started_at = parse_timestamp(context.job_timestamp_started_at)
    remembered_finished_at = parse_timestamp(context.job_timestamp_finished_at)
    current_started_at = parse_timestamp(data['started_at'])
    current_finished_at = parse_timestamp(data['finished_at'])

    assert current_started_at > remembered_started_at, \
        "Current metadata are not newer: failed on started_at attributes comparison"
    assert current_finished_at > remembered_finished_at, \
        "Current metadata are not newer: failed on finished_at attributes comparison"


@when('I wait for new toplevel data for the package {package} in ecosystem '
      '{ecosystem} in the AWS S3 database bucket {bucket}')
def wait_for_package_toplevel_file(context, package, ecosystem, bucket):
    """Wait for the package analysis to finish.

    This function tries to wait for the finish of component (package) analysis by repeatedly
    reading the 'LastModified' attribute from the {ecosystem}/{package}.json bucket
    from the bayesian-core-package-data.
    If this attribute is newer than remembered timestamp, the analysis is perceived as done.
    """
    timeout = 300 * 60
    sleep_amount = 10

    key = S3Interface.package_key(ecosystem, package)

    start_time = datetime.datetime.now(datetime.timezone.utc)

    for _ in range(timeout // sleep_amount):
        current_date = datetime.datetime.now(datetime.timezone.utc)
        try:
            last_modified = context.s3interface.read_object_metadata(bucket, key,
                                                                     "LastModified")
            delta = current_date - last_modified
            # print(current_date, "   ", last_modified, "   ", delta)
            if delta.days == 0 and delta.seconds < sleep_amount * 2:
                # print("done!")
                read_core_package_data_from_bucket(context, "package toplevel", package,
                                                   ecosystem, bucket)
                return
        except ClientError as e:
            print("No analyses yet (waiting for {t})".format(t=current_date - start_time))
        time.sleep(sleep_amount)
    raise Exception('Timeout waiting for the job metadata in S3!')
