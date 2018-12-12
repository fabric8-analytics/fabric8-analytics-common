"""Setup for the BAF tests."""

import os
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
        print("OK: {name} environment is set and will be used as "
              "authorization token".format(name=env_var_name))
    else:
        print("Warning: the {name} environment variable is not"
              " set.\n"
              "Most tests that require authorization will probably fail".format(
                  name=env_var_name))


def check_api_tokens_presence():
    """Check if API token is present in environment variable(s)."""
    # we need RECOMMENDER_API_TOKEN or RECOMMENDER_REFRESH_TOKEN to be set
    if not os.environ.get("RECOMMENDER_REFRESH_TOKEN"):
        _missing_api_token_warning("RECOMMENDER_API_TOKEN")
    else:
        _missing_api_token_warning("RECOMMENDER_REFRESH_TOKEN")


def setup():
    """Perform BAF setup."""
    log.info("Setup")
    with log.indent():
        cli_arguments = cli_parser.parse_args()
        generate_html = cli_arguments.html

        license_service_url = read_url_from_env_var("OSIO_AUTH_SERVICE")
        refresh_token = os.environ.get("RECOMMENDER_REFRESH_TOKEN")

        if not license_service_url:
            log.error("OSIO_AUTH_SERVICE is not set")
            os.exit(-1)

        log.info("HTML generator: " + ("enabled" if generate_html else "disabled"))
        log.info("Auth service URL: " + license_service_url)
        log.info("Refresh token: " + ("set" if refresh_token else "not set"))
        log.info("Success")

    log.info("Auth. token generation")
    with log.indent():
        # we can retrieve access token by using refresh/offline token
        access_token = retrieve_access_token(refresh_token, license_service_url)
        if access_token is None:
            os.exit(-1)
        log.success("Success")

    return {"access_token": access_token,
            "generate_html": generate_html}
