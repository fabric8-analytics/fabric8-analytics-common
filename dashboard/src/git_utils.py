"""Git utility functions."""

import os


def update_repository_name(repository):
    """Update given repository name so it won't contain any prefix(es)."""
    lastSlash = repository.rfind("/")

    # make sure we use just the repo name
    if lastSlash >= 0 and lastSlash < len(repository) - 1:
        return repository[1 + lastSlash:]
    else:
        return repository


def is_repository_cloned(repository):
    """Check if the directory with cloned repository exist."""
    return os.path.isdir("repositories/" + update_repository_name(repository))


def clone_repository(repository, full_history):
    """Clone the selected repository."""
    print("Cloning the repository {repository}".format(repository=repository))
    prefix = "https://github.com"
    if full_history:
        cmd = "pushd repositories; git clone {prefix}/{repo}.git; popd".\
              format(prefix=prefix, repo=repository)
    else:
        cmd = "pushd repositories; git clone --single-branch --depth 1 {prefix}/{repo}.git; popd".\
              format(prefix=prefix, repo=repository)
    os.system(cmd)


def fetch_repository(repository):
    """Fetch the selected repository."""
    repository = update_repository_name(repository)
    print("Fetching changes from the repository {repository}".format(repository=repository))
    command = "pushd repositories/{repository}; git fetch; popd".format(repository=repository)
    os.system(command)


def clone_or_fetch_repository(repository, full_history=False):
    """Clone or fetch the selected repository."""
    if is_repository_cloned(repository):
        fetch_repository(repository)
    else:
        clone_repository(repository, full_history)
