"""Interface to Mattermost designed to send one message only."""
import requests
import json


def login(base_url, login, password):
    """Login into Mattermost."""
    payload = {
        'login_id': login,
        'password': password
    }

    response = requests.post(base_url + "users/login", data=json.dumps(payload))
    token = response.headers["Token"]
    return token


def construct_headers(token):
    """Construct headers for the REST API call."""
    headers = {'Authorization': 'Bearer ' + token}
    return headers


def get_team_id(base_url, token, team_name):
    """Get team ID for the given team name using REST API."""
    address = base_url + "teams"
    headers = construct_headers(token)
    response = requests.get(address, headers=headers)
    payload = response.json()

    for item in payload:
        if item["name"] == team_name:
            return item["id"]

    return None


def get_channel_id(base_url, token, team_id, channel_name):
    """Get channel ID for the given channel name and team id using REST API."""
    address = base_url + "teams/" + team_id + "/channels/name/" + channel_name
    headers = construct_headers(token)
    response = requests.get(address, headers=headers)
    payload = response.json()
    return payload["id"]


def send_message(base_url, token, channel_id, message):
    """Send message to selected channel."""
    payload = {
        "channel_id": channel_id,
        "message": message,
        "root_id": "",
        "file_ids": [],
        "props": ""
    }

    headers = construct_headers(token)
    response = requests.post(base_url + "posts", data=json.dumps(payload), headers=headers)
    return response


def login_and_send_message(base_url, login_name, password, team, channel, message):
    """Perform login to Mattermost and send message into the selected channel."""
    token = login(base_url, login_name, password)
    team_id = get_team_id(base_url, token, team)
    channel_id = get_channel_id(base_url, token, team_id, channel)
    send_message(base_url, token, channel_id, message)
