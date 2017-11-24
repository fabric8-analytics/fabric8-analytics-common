"""Functions for handling JSON responses returned by various API endpoints."""
import string

from src.attribute_checks import *


def get_value_using_path(obj, path):
    """Get the attribute value using the XMLpath-like path specification.

    Return any attribute stored in the nested object and list hierarchy using
    the 'path' where path consists of:
        keys (selectors)
        indexes (in case of arrays)
    separated by slash, ie. "key1/0/key_x".

    Usage:
    get_value_using_path({"x" : {"y" : "z"}}, "x"))   -> {"y" : "z"}
    get_value_using_path({"x" : {"y" : "z"}}, "x/y")) -> "z"
    get_value_using_path(["x", "y", "z"], "0"))       -> "x"
    get_value_using_path(["x", "y", "z"], "1"))       -> "y"
    get_value_using_path({"key1" : ["x", "y", "z"],
                          "key2" : ["a", "b", "c", "d"]}, "key1/1")) -> "y"
    get_value_using_path({"key1" : ["x", "y", "z"],
                          "key2" : ["a", "b", "c", "d"]}, "key2/1")) -> "b"
    """
    keys = path.split("/")
    for key in keys:
        if key.isdigit():
            obj = obj[int(key)]
        else:
            obj = obj[key]
    return obj


def check_timestamp_in_json_response(context, attribute):
    """Check if the timestamp stored in given attribute is correct."""
    timestamp = context.response.json().get(attribute)
    check_timestamp(timestamp)


def check_request_id_value_in_json_response(context, attribute_name):
    """Check the request ID attribute in the JSON response.

    Check if ID is stored in a format like: '71769af6-0a39-4242-94be-1f84f04c8a56'
    """
    response = context.response
    assert response is not None

    json_data = response.json()
    assert json_data is not None

    check_attribute_presence(json_data, attribute_name)
    id_attribute = json_data[attribute_name]

    assert id_attribute is not None
    assert check_uuid(id_attribute)


def check_id_value_in_json_response(context, id_attribute_name):
    """Check the ID attribute in the JSON response.

    Check if ID is stored in a format like: '477e85660c504b698beae2b5f2a28b4e'
    ie. it is a string with 32 characters containing 32 hexadecimal digits
    """
    response = context.response
    assert response is not None

    json_data = response.json()
    assert json_data is not None

    check_attribute_presence(json_data, id_attribute_name)
    id_attribute = json_data[id_attribute_name]

    assert id_attribute is not None
    assert isinstance(id_attribute, str) and len(id_attribute) == 32
    assert all(char in string.hexdigits for char in id_attribute)


def is_empty_json_response(context):
    """Check if the JSON response is empty (but not None)."""
    return context.response.json() == {}
