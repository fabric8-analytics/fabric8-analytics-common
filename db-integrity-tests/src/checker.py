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

    def check_timestamp(self, timestamp):
        """Check if the string contains proper timestamp value.

        The following four formats are supported:
        2017-07-19 13:05:25.041688
        2017-07-17T09:05:29.101780
        2017-07-19 13:05:25
        2017-07-17T09:05:29
        """
        assert timestamp is not None
        assert isinstance(timestamp, str)

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
