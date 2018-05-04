"""Common predicates used by various schema definitions."""

import datetime
import re

from voluptuous import Invalid


def string_p(value):
    """Predicate that checks if the given value is a string."""
    if type(value) is not str:
        raise Invalid("invalid value type {value}".format(value=value))


def timestamp_p(value):
    """Predicate that checks if the given string contain proper timestamp."""
    # check if the value has the expected type
    string_p(value)

    timeformat = '%Y-%m-%dT%H:%M:%S.%f'
    try:
        # try to parse the input value
        datetime.datetime.strptime(value, timeformat)
    except ValueError as e:
        raise Invalid("invalid datetime value {value}".format(value=value))


def posint_p(value):
    """Predicate that checks if the given value is a positive integer."""
    # check if the value has the expected type
    if type(value) is not int:
        raise Invalid("invalid value type {value}".format(value=value))
    if value <= 0:
        raise Invalid("invalid value {value}, positive integer expected".format(value=value))


def negint_p(value):
    """Predicate that checks if the given value is a negative integer."""
    # check if the value has the expected type
    if type(value) is not int:
        raise Invalid("invalid value type {value}".format(value=value))
    if value >= 0:
        raise Invalid("invalid value {value}, negative integer expected".format(value=value))


def posint_zero_p(value):
    """Predicate that checks if the given value is positive integer or zero."""
    # check if the value has the expected type
    if type(value) is not int:
        raise Invalid("invalid value type {value}".format(value=value))
    if value < 0:
        raise Invalid("invalid value {value}, positive value or zero expected".format(value=value))


def negint_zero_p(value):
    """Predicate that checks if the given value is negative integer or zero."""
    # check if the value has the expected type
    if type(value) is not int:
        raise Invalid("invalid value type {value}".format(value=value))
    if value > 0:
        raise Invalid("invalid value {value}, negative value or zero expected".format(value=value))


def posfloat_p(value):
    """Predicate that checks if the given value is positive float."""
    # check if the value has the expected type
    if type(value) is not float:
        raise Invalid("invalid value type {value}".format(value=value))
    if value <= 0.0:
        raise Invalid("invalid value {value}, positive float expected".format(value=value))


def posfloat_zero_p(value):
    """Predicate that checks if the given value is positive float or zero."""
    # check if the value has the expected type
    if type(value) is not float:
        raise Invalid("invalid value type {value}".format(value=value))
    if value < 0.0:
        raise Invalid("invalid value {value}, positive float or zero expected".format(value=value))


def negfloat_p(value):
    """Predicate that checks if the given value is positive float."""
    # check if the value has the expected type
    if type(value) is not float:
        raise Invalid("invalid value type {value}".format(value=value))
    if value >= 0.0:
        raise Invalid("invalid value {value}, negative float expected".format(value=value))


def negfloat_zero_p(value):
    """Predicate that checks if the given value is positive float or zero."""
    # check if the value has the expected type
    if type(value) is not float:
        raise Invalid("invalid value type {value}".format(value=value))
    if value > 0.0:
        raise Invalid("invalid value {value}, negative float or zero expected".format(value=value))


def md5_p(value):
    """Predicate that checks if the given value seems to be MD5 hash."""
    # check if the value has the expected type
    string_p(value)

    # MD5 hash has 32 hexadecimal characters
    if not re.fullmatch(r"^[a-f0-9]{32}$", value):
        raise Invalid("the value '{value}' does not seem to be MD5 hash".format(value=value))


def sha1_p(value):
    """Predicate that checks if the given value seems to be SHA1 hash."""
    # check if the value has the expected type
    string_p(value)

    # SHA-1 hash has 40 hexadecimal characters
    if not re.fullmatch(r"^[a-f0-9]{40}$", value):
        raise Invalid("the value '{value}' does not seem to be SHA1 hash".format(value=value))


def sha256_p(value):
    """Predicate that checks if the given value seems to be SHA256 hash."""
    # check if the value has the expected type
    string_p(value)

    # SHA-256 hash has 64 hexadecimal characters
    if not re.fullmatch(r"^[a-fA-F0-9]{64}$", value):
        raise Invalid("the value '{value}' does not seem to be SHA256 hash".format(value=value))
