"""All possible test results."""


from enum import Enum


class TestResult(Enum):
    """All possible test results."""

    CONFIGURATION_ERROR = 1
    DRY_RUN = 2
    SUCCESS = 3
    FAILURE = 4
