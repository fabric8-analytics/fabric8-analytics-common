"""Data structures validation against schemas."""

from behave import given, then, when

# component-related schemas
from src.schemas.component_code_metrics import COMPONENT_CODE_METRICS_SCHEMA
from src.schemas.component_digests import COMPONENT_DIGESTS_SCHEMA
from src.schemas.component_dependency_snapshot import COMPONENT_DEPENDENCY_SNAPSHOT_SCHEMA
from src.schemas.component_keywords_tagging import COMPONENT_KEYWORDS_TAGGING_SCHEMA


@then(u'I should find that the metadata conformns to component_code_metrics schema')
def check_component_code_metrics_schema(context):
    """Check if the component code metrics metadata conformns to schema."""
    json_data = context.s3_data
    assert COMPONENT_CODE_METRICS_SCHEMA == json_data


@then(u'I should find that the metadata conformns to component_digests schema')
def check_component_digests_schema(context):
    """Check if the component digests metadata conformns to schema."""
    json_data = context.s3_data
    assert COMPONENT_DIGESTS_SCHEMA == json_data


@then(u'I should find that the metadata conformns to component_dependency_snapshot schema')
def check_component_dependency_snapshot_schema(context):
    """Check if the component dependency snapshot metadata conformns to schema."""
    json_data = context.s3_data
    assert COMPONENT_DEPENDENCY_SNAPSHOT_SCHEMA == json_data


@then(u'I should find that the metadata conformns to component_keywords_tagging schema')
def check_component_keywords_tagging_schema(context):
    """Check if the component keywords tagging metadata conformns to schema."""
    json_data = context.s3_data
    assert COMPONENT_KEYWORDS_TAGGING_SCHEMA == json_data


