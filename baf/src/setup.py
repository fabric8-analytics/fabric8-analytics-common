"""Setup for the BAF tests."""

import os
import sys
from fastlog import log

from cliargs import cli_parser
from auth import retrieve_access_token

# The following endpoint is used to get the access token from OSIO AUTH service
_AUTH_ENDPOINT = "/api/token/refresh"


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


def setup():
    """Perform BAF setup."""
    log.info("Setup")
    with log.indent():
        cli_arguments = cli_parser.parse_args()
        dry_run = cli_arguments.dry
        generate_html = cli_arguments.html
        generate_csv = cli_arguments.csv

        if not dry_run:
            check_api_tokens_presence()
            license_service_url = read_url_from_env_var("OSIO_AUTH_SERVICE")
            refresh_token = os.environ.get("RECOMMENDER_REFRESH_TOKEN")

            if not license_service_url:
                log.error("OSIO_AUTH_SERVICE is not set")
                sys.exit(-1)
        else:
            license_service_url = "N/A"
            refresh_token = None

        log.info("Dry run:          " + enabled_disabled(dry_run))
        log.info("HTML generator:   " + enabled_disabled(generate_html))
        log.info("CSV generator:    " + enabled_disabled(generate_csv))
        log.info("Auth service URL: " + license_service_url)
        log.info("Refresh token:    " + ("set" if refresh_token else "not set"))
        log.info("Success")

    access_token = get_access_token(dry_run, refresh_token, license_service_url)

    return {"access_token": access_token,
            "generate_html": generate_html,
            "generate_csv": generate_csv,
            "dry_run": dry_run}
