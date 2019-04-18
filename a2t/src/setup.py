"""Setup for the BAF tests.

Copyright (c) 2019 Red Hat Inc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
from fastlog import log

from auth import retrieve_access_token

# The following endpoint is used to get the access token from OSIO AUTH service
_AUTH_ENDPOINT = "/api/token/refresh"

DEFAULT_INPUT_FILE = "scenarios.csv"


def add_slash(url):
    """Add a slash at the end of URL if the slash is not already presented."""
    if url and not url.endswith('/'):
        url += '/'
    return url


def read_url_from_env_var(env_var_name):
    """Read URL from selected environment variable."""
    return add_slash(os.environ.get(env_var_name, None))


def missing_api_token_warning(env_var_name):
    """Print warning or basic info about missing API token."""
    if os.environ.get(env_var_name):
        log.success("OK: {name} environment is set and will be used as "
                    "authorization token".format(name=env_var_name))
    else:
        log.warning("Warning: the {name} environment variable is not"
                    " set.\n"
                    "Most tests that require authorization will probably fail".format(
                        name=env_var_name))


def check_api_tokens_presence():
    """Check if API token is present in environment variable(s)."""
    # we need RECOMMENDER_API_TOKEN or RECOMMENDER_REFRESH_TOKEN to be set
    if not os.environ.get("RECOMMENDER_REFRESH_TOKEN"):
        missing_api_token_warning("RECOMMENDER_API_TOKEN")
    else:
        missing_api_token_warning("RECOMMENDER_REFRESH_TOKEN")


def yes_no(string):
    """Parse 'yes' and 'Yes' strings to True, all other values to False."""
    return string is not None and string in {"yes", "Yes"}


def enabled_disabled(b):
    """Convert boolean value to 'enabled' or 'disabled'."""
    return "enabled" if b else "disabled"


def get_access_token(dry_run, refresh_token, license_service_url):
    """Get the access token if possible."""
    if not dry_run:
        log.info("Auth. token generation")
        with log.indent():
            # we can retrieve access token by using refresh/offline token
            access_token = retrieve_access_token(refresh_token, license_service_url)
            if access_token is None:
                sys.exit(-1)
            log.success("Success")
    else:
        access_token = None
    return access_token


def parse_tags(tags):
    """Parse string containing list of tags."""
    if tags is not None:
        tags = set(tags.split(","))
    return tags


def tags_as_str(tags):
    """Convert list of tags to string."""
    return " ".join(tags) if tags else "all tests"


def refresh_token_as_str(refresh_token):
    """Convert refresh token settings (set/not set) into string."""
    return "set" if refresh_token else "not set"


def setup(cli_arguments):
    """Perform BAF setup."""
    log.info("Setup")

    refresh_token = None
    api_token = None

    with log.indent():
        input_file = cli_arguments.input or DEFAULT_INPUT_FILE
        dry_run = cli_arguments.dry
        tags = parse_tags(cli_arguments.tags)

        if not dry_run:
            check_api_tokens_presence()
            license_service_url = read_url_from_env_var("OSIO_AUTH_SERVICE")
            refresh_token = os.environ.get("RECOMMENDER_REFRESH_TOKEN")
            api_token = os.environ.get("RECOMMENDER_API_TOKEN")

            if not license_service_url:
                log.error("OSIO_AUTH_SERVICE is not set")
                sys.exit(-1)
        else:
            license_service_url = "N/A"

        log.info("Dry run:          " + enabled_disabled(dry_run))
        log.info("Input file:       " + input_file)
        log.info("Auth service URL: " + license_service_url)
        log.info("Run tests:        " + tags_as_str(tags))
        log.info("Refresh token:    " + refresh_token_as_str(refresh_token))
        log.success("Success")

    if api_token is not None:
        access_token = api_token
    else:
        access_token = get_access_token(dry_run, refresh_token, license_service_url)

    return {"access_token": access_token,
            "tags": tags,
            "dry_run": dry_run,
            "input_file": input_file}
