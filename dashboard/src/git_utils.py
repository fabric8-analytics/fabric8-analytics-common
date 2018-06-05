"""Git utility functions."""

import os


def is_repository_cloned(repository):
    """Check if the directory with cloned repository exist."""
    return os.path.isdir(repository)


def clone_repository(repository):
    """Clone the selected repository."""
    print("Cloning the repository {repository}".format(repository=repository))
    prefix = "https://github.com/"
    command = "pushd repositories; git clone --single-branch --depth 1 {prefix}/{repo}.git; popd".\
        format(prefix=prefix, repo=repository)
    os.system(command)


def fetch_repository(repository):
    """Fetch the selected repository."""
    print("Fetching changes from the repository {repository}".format(repository=repository))
    command = "pushd repositories/{repository}; git fetch; popd".format(repository=repository)
    os.system(command)


def clone_or_fetch_repository(repository):
    """Clone or fetch the selected repository."""
    if is_repository_cloned(repository):
        fetch_repository(repository)
    else:
        clone_repository(repository)
