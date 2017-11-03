"""Functions that handle and construct authorization tokens for server and jobs APIs."""


def jobs_api_authorization(context):
    """Construct header with authorization token for the jobs API calls.

    Returned dict can be added to the 'request' object.
    """
    return {'auth-token': '{token}'.format(token=context.jobs_api_token)}


def authorization(context):
    """Construct header with authorization token for the server API calls.

    Returned dict can be added to the 'request' object.
    """
    return {'Authorization': 'Bearer {token}'.format(token=context.token)}
