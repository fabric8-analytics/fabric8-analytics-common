"""Utility functions to check attributes returned in API responses and read from the AWS S3."""
import datetime
import re


def check_attribute_presence(node, attribute_name):
    """Check the attribute presence in the given dictionary or list.

    To be used to check the deserialized JSON data etc.
    """
    found_attributes = node if type(node) is list else node.keys()
    assert attribute_name in node, \
        "'%s' attribute is expected in the node, " \
        "found: %s attributes " % (attribute_name, ", ".join(found_attributes))


def check_attributes_presence(node, attribute_names):
    """Check the presence of all attributes in the dictionary or in the list.

    To be used to check the deserialized JSON data etc.
    """
    for attribute_name in attribute_names:
        found_attributes = node if type(node) is list else node.keys()
        assert attribute_name in node, \
            "'%s' attribute is expected in the node, " \
            "found: %s attributes " % (attribute_name, ", ".join(found_attributes))


def check_and_get_attribute(node, attribute_name):
    """Check the attribute presence and if the attribute is found, return its value."""
    check_attribute_presence(node, attribute_name)
    return node[attribute_name]


def check_uuid(uuid):
    """Check if the string contains a proper UUID.

    Supported format: 71769af6-0a39-4242-94be-1f84f04c8a56
    """
    regex = re.compile(
        r'^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z',
        re.I)
    match = regex.match(uuid)
    return bool(match)


def is_string(attribute):
    """Check if given attribute is a string."""
    assert attribute is not None
    assert isinstance(attribute, str)


def check_timestamp(timestamp):
    """Check if the string contains proper timestamp value.

    The following four formats are supported:
    2017-07-19 13:05:25.041688
    2017-07-17T09:05:29.101780
    2017-07-19 13:05:25
    2017-07-17T09:05:29
    """
    is_string(timestamp)

    # some attributes contains timestamp without the millisecond part
    # so we need to take care of it
    if len(timestamp) == len("YYYY-mm-dd HH:MM:SS") and '.' not in timestamp:
        timestamp += '.0'

    assert len(timestamp) >= len("YYYY-mm-dd HH:MM:SS.")

    # we have to support the following formats:
    #    2017-07-19 13:05:25.041688
    #    2017-07-17T09:05:29.101780
    # -> it is needed to distinguish the 'T' separator
    #
    # (please see https://www.tutorialspoint.com/python/time_strptime.htm for
    #  an explanation how timeformat should look like)

    timeformat = "%Y-%m-%d %H:%M:%S.%f"
    if timestamp[10] == "T":
        timeformat = "%Y-%m-%dT%H:%M:%S.%f"

    # just try to parse the string to check whether
    # the ValueError exception is raised or not
    datetime.datetime.strptime(timestamp, timeformat)


def check_job_token_attributes(token):
    """Check that the given JOB token contains all required attributes."""
    attribs = ["limit", "remaining", "reset"]
    for attr in attribs:
        assert attr in token
        assert int(token[attr]) >= 0


def check_status_attribute(data):
    """Check the value of the status attribute, that should contain just two allowed values."""
    status = check_and_get_attribute(data, "status")
    assert status in ["success", "error"]


def check_summary_attribute(data):
    """Check the summary attribute that can be found all generated metadata."""
    summary = check_and_get_attribute(data, "summary")
    assert type(summary) is list or type(summary) is dict


def release_string(ecosystem, package, version=None):
    """Construct a string with ecosystem:package or ecosystem:package:version tuple."""
    return "{e}:{p}:{v}".format(e=ecosystem, p=package, v=version)


def check_release_attribute(data, ecosystem, package, version=None):
    """Check the content of _release attribute.

    Check that the attribute _release contains proper release string for given ecosystem
    and package.
    """
    check_attribute_presence(data, "_release")
    assert data["_release"] == release_string(ecosystem, package, version)


def check_schema_attribute(data, expected_schema_name, expected_schema_version):
    """Check the content of the schema attribute.

    This attribute should contains dictionary with name and version that are checked as well.
    """
    # read the toplevel attribute 'schema'
    schema = check_and_get_attribute(data, "schema")

    # read attributes from the 'schema' node
    name = check_and_get_attribute(schema, "name")
    version = check_and_get_attribute(schema, "version")

    # check the schema name
    assert name == expected_schema_name, "Schema name '{n1}' is different from " \
        "expected name '{n2}'".format(n1=name, n2=expected_schema_name)

    # check the schema version (ATM we are able to check just one fixed version)
    assert version == expected_schema_version, "Schema version {v1} is different from expected " \
        "version {v2}".format(v1=version, v2=expected_schema_version)


def check_audit_metadata(data):
    """Check the metadata stored in the _audit attribute.

    Check if all common attributes can be found in the audit node
    in the component or package metadata.
    """
    check_attribute_presence(data, "_audit")
    audit = data["_audit"]

    check_attribute_presence(audit, "version")
    assert audit["version"] == "v1"

    check_attribute_presence(audit, "started_at")
    check_timestamp(audit["started_at"])

    check_attribute_presence(audit, "ended_at")
    check_timestamp(audit["ended_at"])


def get_details_node(context):
    """Get content of details node, given it exists."""
    data = context.s3_data

    return check_and_get_attribute(data, 'details')


def check_cve_pattern(with_score):
    """Return the pattern for matching CVE entry."""
    if with_score:
        # please note that in graph DB, the CVE entries have the following format:
        # CVE-2012-1150:5.0
        # don't ask me why, but the score is stored in one field together with ID itself
        # the : character is used as a separator
        return r"CVE-(\d{4})-\d{4,}:(\d+\.\d+)"
    else:
        return r"CVE-(\d{4})-\d{4,}"


def check_cve_value(cve, with_score=False):
    """Check CVE values in CVE records."""
    pattern = check_cve_pattern(with_score)

    match = re.fullmatch(pattern, cve)
    assert match is not None, "Improper CVE number %s" % cve

    year = int(match.group(1))
    current_year = datetime.datetime.utcnow().year

    # well the lower limit is a bit arbitrary
    # (according to SRT guys it should be 1999)
    assert year >= 1999 and year <= current_year

    if with_score:
        score = float(match.group(2))
        assert score >= 0.0 and score <= 10.0


def check_hash_value(hash_value):
    """Check if the value is proper hash in hex."""
    assert hash_value is not None
    pattern = r"[A-Za-z0-9]+"
    match = re.fullmatch(pattern, hash_value)
    assert match is not None, "Improper hash value %s" % hash_value
