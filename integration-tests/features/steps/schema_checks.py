"""Data structures validation against schemas."""

from behave import given, then, when

# component-related schemas
from src.schemas.component_code_metrics import COMPONENT_CODE_METRICS_SCHEMA


@then(u'I should find that the metadata conformns to component_code_metrics schema')
def check_component_code_metrics_schema(context):
    """Check if the component code metrics metadata conformns to schema."""
    json_data = context.s3_data
    assert COMPONENT_CODE_METRICS_SCHEMA == json_data
