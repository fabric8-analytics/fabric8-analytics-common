"""API fuzzer logic."""

from fastlog import log
from pprint import pprint

import json
import os
import itertools
import copy

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


def perform_test(url, http_method, dry_run, payload, cfg, expected_status):
    if dry_run:
        log.info("(dry run)")
        pprint(payload)
    else:
        if http_method == "POST":
            log.info("POSTing data")
            response = send_payload(url, payload, cfg["access_token"])
            assert response.status_code == expected_status


def run_tests_with_removed_items_one_iteration(url, http_method, dry_run, original_payload,
                                               cfg, expected_status, items_count, remove_flags):
    """One iteration for the run_tests_with_removed_items()."""
    keys = list(original_payload.keys())
    # deep copy
    new_payload = copy.deepcopy(original_payload)
    for i in range(items_count):
        remove_flag = remove_flags[i]
        if remove_flag:
            key = keys[i]
            log.info("Removing item #{n} with key '{k}' from payload".format(n=i, k=key))
            del new_payload[key]
    perform_test(url, http_method, dry_run, new_payload, cfg, expected_status)


def run_tests_with_removed_items(url, http_method, dry_run, original_payload, cfg,
                                 expected_status):
    """Run tests with items removed from the original payload."""
    iteration = 0
    with log.indent():
        items_count = len(original_payload)
        # lexicographics ordering
        remove_flags_list = list(itertools.product([True, False], repeat=items_count))
        # the last item contains (False, False, False...) and we are not interesting
        # in removing ZERO items
        remove_flags_list = remove_flags_list[:-1]

        with log.indent():
            log.info("Iteration #{n}".format(n=iteration))
            with log.indent():
                for remove_flags in remove_flags_list:
                    run_tests_with_removed_items_one_iteration(url, http_method, dry_run,
                                                               original_payload, cfg,
                                                               expected_status, items_count,
                                                               remove_flags)
            iteration += 1


def run_test(cfg, test):
    """Run one selected test."""
    url = construct_url(test)
    log.info("URL to test: " + url)

    http_method = test["Method"]
    log.info("HTTP method:   " + http_method)

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

    original_payload = load_json(filename)
    perform_test(url, http_method, dry_run, original_payload, cfg, expected_status)

    if remove_items:
        log.info("Run tests with items removed from original payload")
        run_tests_with_removed_items(url, http_method, dry_run, original_payload, cfg,
                                     expected_status)

    log.success("Finished")
