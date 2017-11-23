"""Tests for Gremlin database."""
import os
import requests

from behave import given, then, when
from urllib.parse import urljoin


@when('I access Gremlin API')
def gremlin_url_access(context):
    """Access the Gremlin service API using the HTTP POST method."""
    post_query(context, "")


def post_query(context, query):
    """Post the already constructed query to the Gremlin."""
    data = {"gremlin": query}
    context.response = requests.post(context.gremlin_url, json=data)
