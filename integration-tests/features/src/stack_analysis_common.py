"""Common functions used to test stack analysis API."""


def get_result_from_payload(json_resp):
    """Try to get result node from the payload."""
    assert json_resp is not None
    assert 'result' in json_resp
    # read the actual result
    return json_resp.get('result')


def contains_alternate_node(json_resp):
    """Check for the existence of alternate node in the stack analysis."""
    result = get_result_from_payload(json_resp)
    return bool(result) and isinstance(result, list) \
        and (result[0].get('recommendation', {}) or {}).get('alternate', None) is not None
