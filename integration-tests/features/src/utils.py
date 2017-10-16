"""Unsorted utility functions."""
import requests


def download_file_from_url(url):
    """Download file from the given URL and do basic check of response."""
    response = requests.get(url)
    assert response.status_code == 200
    assert response.text is not None
    return response.text


def split_comma_separated_list(l):
    """Split the list into elements separated by commas."""
    return [i.strip() for i in l.split(',')]
