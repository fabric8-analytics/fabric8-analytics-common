"""Definitions of tests for packages metadata stored in the AWS S3 database."""
from behave import given, then, when
from src.attribute_checks import *
from src.s3interface import *


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

    check_schema_attribute(data, "github_details", "1-0-4")


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
