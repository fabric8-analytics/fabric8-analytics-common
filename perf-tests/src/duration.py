import datetime


class Duration():

    def __init__(self, started_at_str, finished_at_str):
        self.started_at = Duration.parse_timestamp(started_at_str)
        self.finished_at = Duration.parse_timestamp(finished_at_str)
        self.duration = self.finished_at - self.started_at
        self.duration_seconds = self.duration.total_seconds()

    def from_data(s3data):
        return Duration(s3data.get("started_at"), s3data.get("finished_at"))

    def from_audit(s3data):
        audit = s3data.get("_audit")
        return Duration(audit.get("started_at"), audit.get("ended_at"))

    def parse_timestamp(string):
        timeformat = '%Y-%m-%dT%H:%M:%S.%f'
        return datetime.datetime.strptime(string, timeformat)

    def __repr__(self):
        return "{started} .. {finished} .. {duration}".format(started=self.started_at,
                                                              finished=self.finished_at,
                                                              duration=self.duration_seconds)
