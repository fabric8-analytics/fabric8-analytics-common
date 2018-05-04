"""Common schemas."""

from pytest_voluptuous import S
from voluptuous import Any

from .predicates import timestamp_p


# The audit entry needs to have three attributes
AUDIT = S({"started_at": timestamp_p,
           "ended_at": timestamp_p,
           "version": str})


# Status entry
# TODO: add all non-success values
STATUS = Any("success")


# Ecosystem options
ECOSYSTEM = Any("maven", "npm", "pypi")
