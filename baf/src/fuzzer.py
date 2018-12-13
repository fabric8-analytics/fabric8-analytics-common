"""API fuzzer logic."""

from fastlog import log
from pprint import pprint

import json
import os
import sys

from setup import add_slash, yes_no, enabled_disabled
from rest_api_calls import send_payload

from random_payload_generator import RandomPayloadGenerator


def load_json(filename):
    """Load and decode JSON file."""
    with open(filename) as fin:
        return json.load(fin)


def fuzz(data):
    """Fuzz the payload."""
    rdg = RandomPayloadGenerator()
    new_key = rdg.generate_random_key_for_dict(data)
    new_data = rdg.generate_random_payload(restrict_types=(list, dict))
    print(new_key)
    pprint(new_data)


def construct_url(test):
    """Construct URL for the REST API call."""
    server_env_var = test["Server"]
    server_url = os.environ.get(server_env_var)
    if server_url is None:
        log.error("The following environment variable is not set {var}".format(var=server_env_var))

    url = "{base}{prefix}{method}".format(base=add_slash(server_url),
                                          prefix=add_slash(test["Prefix"]),
                                          method=test["Endpoint"])
    return url


def run_test(cfg, test):
    """Run one selected test."""
    url = construct_url(test)
    log.info("URL to test: " + url)

    dry_run = cfg["dry_run"]
    add_items = yes_no(test["Add items"])
    remove_items = yes_no(test["Remove items"])
    change_types = yes_no(test["Change types"])
    mutate_payload = yes_no(test["Mutate payload"])
    expected_status = test["Expected status"]
    filename = test["Payload"]

    log.info("Add items operation:        " + enabled_disabled(add_items))
    log.info("Remove items operation:     " + enabled_disabled(remove_items))
    log.info("Change item type operation: " + enabled_disabled(change_types))
    log.info("Mutate payload operation:   " + enabled_disabled(mutate_payload))
    log.info("Original payload file:      " + filename)

    original_json = load_json(filename)
    pprint(original_json)

    if not dry_run:
        if test["Method"] == "POST":
            log.info("POSTing data")
            response = send_payload(url, original_json, cfg["access_token"])
            assert response.status_code == 200
            print(response)
            print(response.json())

    log.success("Finished")
