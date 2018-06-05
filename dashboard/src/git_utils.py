"""Git utility functions."""

import os
import re


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


def create_log(repository):
    """Retrieve the log for the given repository."""
    repository = update_repository_name(repository)
    command = ("pushd repositories/{repo} >> /dev/null; " +
               "git log --pretty=oneline > ../logs.txt; " +
               "popd >> /dev/null").format(repo=repository)
    os.system(command)


def read_all_commits(filename):
    """Read all commits from the given GIT log file."""
    commits = []
    with open(filename) as fin:
        for line in fin:
            splitted = line.strip().split(" ", 1)
            commits.append(splitted)
    commits.reverse()
    return commits


def read_commits(filename, pattern):
    """Read commits from the given GIT log file that pass the selected pattern."""
    commits = read_all_commits(filename)
    # filter commits
    return [commit for commit in commits if re.fullmatch(pattern, commit[1])]


def checkout(repository, commit):
    """Perform the GIT checkout in the selected repository."""
    repository = update_repository_name(repository)
    command = ("pushd repositories/{repo} >> /dev/null; " +
               "git checkout {commit}; " +
               "popd >> /dev/null").format(repo=repository, commit=commit)
    os.system(command)
