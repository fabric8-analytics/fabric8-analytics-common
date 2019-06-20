#!/usr/bin/python3

"""Script to retrieve the refresh_token attribute value from token.json file.

Information about usage of this script can be found in:
integration_tests.adoc
"""

import json

with open('token.json') as fin:
    payload = json.load(fin)
    assert payload is not None
    assert "refresh_token" in payload
    r = payload["refresh_token"]
    assert r is not None
    print(r)

    with open('refresh_token.txt', 'w') as fout:
        fout.write(r)
