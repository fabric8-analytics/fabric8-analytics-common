import datetime


class Duration():

    def __init__(self, started_at_str, finished_at_str):
        self.started_at = Duration.parse_timestamp(started_at_str)
        self.finished_at = Duration.parse_timestamp(finished_at_str)
        self.duration = self.finished_at - self.started_at
        self.duration_seconds = self.duration.total_seconds()

    def parse_timestamp(string):
        timeformat = '%Y-%m-%dT%H:%M:%S.%f'
        return datetime.datetime.strptime(string, timeformat)
