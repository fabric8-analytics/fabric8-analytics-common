#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Tests 3scale registration endpoint."""
import requests
import json
import uuid

from behave import given, then, when

from src.json_utils import check_id_value_in_json_response


@given('backbone service is running')
def running_backbone_api(context):
    """Check if 3scale pod is running."""
    return context.is_backbone_api_running


@when('I post {input_file} to Backbone API {endpoint}')
def post_backbone_api(context, input_file, endpoint):
    """Post data to backbone API."""
    filename = 'data/{input_file}'.format(input_file=input_file)
    with open(filename, 'r') as f:
        content = f.read()
    request_id = uuid.uuid4().hex
    content = content.replace('{req_id}', request_id)

    headers = {'Content-Type': 'application/json'}

    context.response = requests.post('{}/{}'.format(context.backbone_api_url, endpoint),
                                     json=json.loads(content), headers=headers)
    context.external_request_id = request_id


@then('I should receive a valid {worker} json response')
def check_valid_response(context, worker):
    """Check if backbone API call response is valid."""
    assert context.response.status_code == 200

    json_data = context.response.json()
    assert json_data[worker] == 'success'

    check_id_value_in_json_response(context, 'external_request_id')


def try_to_find_worker(worker, json_data):
    """Try to find worker in JSON data returned from the service."""
    found = False
    for t in json_data['tasks']:
        if t['task_name'] == worker_name:
            found = True
            break
    assert found


@then('I should find a valid {worker} database entry')
def verify_database_entry(context, worker):
    """Check if backbone API call creates a database entry."""
    worker_name = '{}_v2'.format(worker)
    recommender_token = context.token

    headers = {'Authorization': 'Bearer {}'.format(recommender_token)}
    url = '{}/api/v1/stack-analyses/{}/_debug'.format(context.coreapi_url,
                                                      context.external_request_id)

    resp = requests.get(url, headers=headers)
    assert resp.status_code == 200

    json_data = resp.json()
    assert len(json_data['tasks']) >= 1

    try_to_find_worker(worker, json_data)
