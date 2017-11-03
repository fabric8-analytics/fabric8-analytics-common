"""Module containing a class to represent duration of any analysis read from the S3 database."""

import datetime


class Duration():
    """Class that represents duration of any analysis read from the S3 database."""

    def __init__(self, started_at_str, finished_at_str):
        """Create instance of Duration class and compute durations from provided parameters."""
        self.started_at = Duration.parse_timestamp(started_at_str)
        self.finished_at = Duration.parse_timestamp(finished_at_str)
        self.duration = self.finished_at - self.started_at
        self.duration_seconds = self.duration.total_seconds()

    def from_data(s3data):
        """Fetch duration from the actual data."""
        return Duration(s3data.get("started_at"), s3data.get("finished_at"))

    def from_audit(s3data):
        """Fetch duration from the audit node."""
        audit = s3data.get("_audit")
        return Duration(audit.get("started_at"), audit.get("ended_at"))

    def parse_timestamp(string):
        """Parse the timestamp from data read from the S3 database."""
        timeformat = '%Y-%m-%dT%H:%M:%S.%f'
        return datetime.datetime.strptime(string, timeformat)

    def __repr__(self):
        """Provide textual representation of the Duration object."""
        return "{started} .. {finished} .. {duration}".format(started=self.started_at,
                                                              finished=self.finished_at,
                                                              duration=self.duration_seconds)
