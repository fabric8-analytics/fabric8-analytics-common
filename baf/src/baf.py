"""The main module of the Bayesian API Fuzzer."""

from fastlog import log
import json
import os
from pprint import pprint
from rest_api_calls import send_payload
from csv_reader import read_csv_as_dicts
from setup import setup, add_slash

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
    if test["Method"] == "POST":
        log.info("POSTing data")
        filename = test["Payload"]
        input_json = load_json(filename)
        response = send_payload(url, input_json, cfg["access_token"])
        assert response.status_code == 200
        print(response)
        print(response.json())
    log.success("Finished")


def main():
    """Entry point to the Bayesian API Fuzzer."""
    log.setLevel(log.INFO)
    cfg = setup()
    print(cfg)

    log.info("Run tests")
    with log.indent():
        tests = read_csv_as_dicts("tests.csv")
        if not tests or len(tests) == 0:
            log.error("No tests loaded!")
            os.exit(-1)
        if len(tests) == 1:
            log.info("Loaded 1 test")
        else:
            log.info("Loaded {n} tests".format(n=len(tests)))
        i = 1
        for test in tests:
            log.info("Starting test #{n}".format(n=i))
            with log.indent():
                run_test(cfg, test)
            i += 1


if __name__ == "__main__":
    # execute only if run as a script
    main()
