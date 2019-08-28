"""Class to check attributes read from the AWS S3."""

import datetime
import re


class Checker:
    """Class to check attributes read from the AWS S3."""

    def __init__(self):
        """Initialize the checker."""
        pass

    def check_attribute_presence(self, node, attribute_name):
        """Check the attribute presence in the given dictionary or list.

        To be used to check the deserialized JSON data etc.
        """
        found_attributes = node if type(node) is list else node.keys()
        assert attribute_name in node, \
            "'%s' attribute is expected in the node, " \
            "found: %s attributes " % (attribute_name, ", ".join(found_attributes))

    def check_attributes_presence(self, node, attributes):
        """Check the attributes presence in the given dictionary or list.

        To be used to check the deserialized JSON data etc.
        """
        for attribute_name in attributes:
            self.check_attribute_presence(node, attribute_name)

    def check_and_get_attribute(self, node, attribute_name):
        """Check the attribute presence and if the attribute is found, return its value."""
        self.check_attribute_presence(node, attribute_name)
        return node[attribute_name]

    def check_status_attribute(self, data):
        """Check the value of the status attribute, that should contain just two allowed values."""
        status = self.check_and_get_attribute(data, "status")
        assert status in ["success", "error"]

    def is_string(self, attribute):
        """Check if given attribute is a string."""
        assert attribute is not None
        assert isinstance(attribute, str)

    def check_timestamp(self, timestamp):
        """Check if the string contains proper timestamp value.

        The following four formats are supported:
        2017-07-19 13:05:25.041688
        2017-07-17T09:05:29.101780
        2017-07-19 13:05:25
        2017-07-17T09:05:29
        """
        self.is_string(timestamp)

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

    def get_cve_pattern(self, with_score):
        """Return the pattern for matching CVE entry."""
        if with_score:
            # please note that in graph DB, the CVE entries have the following format:
            # CVE-2012-1150:5.0
            # don't ask me why, but the score is stored in one field together with ID itself
            # the : character is used as a separator
            return r"CVE-(\d{4})-\d{4,}:(\d+\.\d+)"
        else:
            return r"CVE-(\d{4})-\d{4,}"

    def check_cve_value(self, cve, with_score=False):
        """Check CVE values in CVE records."""
        pattern = self.get_cve_pattern(with_score)

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

    def check_audit_metadata(self, data):
        """Check the metadata stored in the _audit attribute.

        Check if all common attributes can be found in the audit node
        in the component or package metadata.
        """
        self.check_attribute_presence(data, "_audit")
        audit = data["_audit"]

        self.check_attribute_presence(audit, "version")
        assert audit["version"] == "v1"

        self.check_attribute_presence(audit, "started_at")
        self.check_timestamp(audit["started_at"])

        self.check_attribute_presence(audit, "ended_at")
        self.check_timestamp(audit["ended_at"])

    def get_details_node(self, data):
        """Get content of details node, given it exists."""
        return self.check_and_get_attribute(data, 'details')

    def check_schema_attribute(self, data, expected_schema_name, expected_schema_version):
        """Check the content of the schema attribute.

        This attribute should contains dictionary with name and version that are checked as well.
        """
        # read the toplevel attribute 'schema'
        schema = self.check_and_get_attribute(data, "schema")

        # read attributes from the 'schema' node
        name = self.check_and_get_attribute(schema, "name")
        version = self.check_and_get_attribute(schema, "version")

        # check the schema name
        assert name == expected_schema_name, "Schema name '{n1}' is different from " \
            "expected name '{n2}'".format(n1=name, n2=expected_schema_name)

        # check the schema version (ATM we are able to check just one fixed version)
        assert version == expected_schema_version, "Schema version {v1} is different from " \
            "expected version {v2}".format(v1=version, v2=expected_schema_version)

    @staticmethod
    def release_string(ecosystem, package, version=None):
        """Construct a string with ecosystem:package or ecosystem:package:version tuple."""
        return "{e}:{p}:{v}".format(e=ecosystem, p=package, v=version)
