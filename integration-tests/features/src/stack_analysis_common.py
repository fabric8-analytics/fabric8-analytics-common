"""Common functions used to test stack analysis API."""


def contains_alternate_node(json_resp):
    """Check for the existence of alternate node in the stack analysis."""
    assert json_resp is not None
    assert 'result' in json_resp
    # read the actual result
    result = json_resp.get('result')
    return bool(result) and isinstance(result, list) \
        and (result[0].get('recommendation', {}) or {}).get('alternate', None) is not None
