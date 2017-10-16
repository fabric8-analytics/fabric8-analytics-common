"""Utility functions to parse specific values, usually from JSON responses."""
import re


def parse_timestamp(string):
    """Parse the timestamp that should be written in standard format."""
    timeformat = '%Y-%m-%dT%H:%M:%S.%f'
    return datetime.datetime.strptime(string, timeformat)


def parse_float_value_from_text_stream(text, key):
    """Parse float value from the text.

    Go through all lines of the text file, find the line with given key
    and parse float value specified here.
    """
    regexp = key + "\s*=\s*(\d.\d*)"
    for line in text.split("\n"):
        if line.startswith(key):
            match = re.fullmatch(regexp, line)
            assert match is not None
            assert match.lastindex == 1
            return float(match.group(1))


def parse_token_clause(token_clause):
    """Parse the clause that could be either 'with', 'using', or 'without'."""
    use_token = {"with": True,
                 "using": True,
                 "without": False}.get(token_clause)
    if use_token is None:
        raise Exception("Wrong clause specified: {t}".format(t=token_clause))
    return use_token
