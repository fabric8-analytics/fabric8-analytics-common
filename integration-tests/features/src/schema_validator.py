"""JSON schema validator implemented in its own module to have only one place to change version."""
from jsonschema import Draft4Validator


def validate_schema(data):
    """Validate the schema against metaschema."""
    Draft4Validator.check_schema(data)
