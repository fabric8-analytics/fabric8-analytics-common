"""Code coverage history generator.

This version creates a graph named `code_coverage_history_{repository}.png`
with the history of code coverage for all supported/measure repositories.

Source data for all graphs are retrieved from the 'history repository' with
QA Dashboard and its data.
"""


import os
import re

# NOTE: we have to use the following order of imports and matplotlib.use must be call between
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from repositories import Repositories
from config import *
import git_utils
import unit_tests


# parameters for graph
# TODO: make these options configurable via config.ini
DEFAULT_WIDTH = 1024
DEFAULT_HEIGHT = 600
DPI = 100


# pattern used to check if the given commit contain history data
COMMIT_MESSAGE_PATTERN = r"Dashboard (20\d\d-\d\d-\d\d)"


def read_summary(filename):
    """Read code coverage summary from the file containing code coverage report."""
    try:
        # it is ok if the file does not exist - the history data don't have to be
        # available in all commits
        with open(filename) as fin:
            for line in fin:
                if unit_tests.line_with_unit_test_summary(line.strip()):
                    return unit_tests.parse_unit_test_statistic(line)
    except Exception as e:
        return None


def get_commit_date(commit_message):
    """Get commit date directly from the message (we use parseable format)."""
    match = re.match(COMMIT_MESSAGE_PATTERN, commit_message)
    if match is not None:
        return match.group(1)
    else:
        return None


def get_filename_with_coverage(hist_repo, repo_to_measure):
    """Get the filename that contains code coverage."""
    return "repositories/{repo}/dashboard/{repo_to_measure}.coverage.txt".format(
           repo=hist_repo, repo_to_measure=repo_to_measure)


def read_code_coverage_history(hist_repo, commits, repo_to_measure):
    """Read code coverage history for the selected repository."""
    git_utils.checkout(hist_repo, "master")
    hist_repo = git_utils.update_repository_name(hist_repo)
    filename = get_filename_with_coverage(hist_repo, repo_to_measure)

    code_coverage_history = []

    # checkout to every commit and read the code coverage statistic
    for commit in commits:
        commit_hash = commit[0]
        commit_date = get_commit_date(commit[1])
        git_utils.checkout(hist_repo, commit_hash)
        summary = read_summary(filename)
        if summary is not None:
            summary["date"] = commit_date
            code_coverage_history.append(summary)
    return code_coverage_history


def get_values_as_str(history, key):
    """Retrieve values from sequence of dictionaries."""
    return [i[key] for i in history]


def get_values_as_int(history, key):
    """Retrieve values from sequence of dictionaries, convert all values to int."""
    return [int(i[key]) for i in history]


def compute_covered(statements, missed):
    """Compute the sequence of 'covered' statements."""
    assert len(statements) == len(missed)
    covered = []
    for i in range(len(statements)):
        covered.append(statements[i] - missed[i])
    return covered


def setup_ticks(step):
    """Configure ticks so only each n-th tick will be visible."""
    plt.xticks(size=7)
    plt.yticks(size=10)

    locs, plt_labels = plt.xticks()
    plt.setp(plt_labels, rotation=90)
    for tick in plt_labels:
        tick.set_visible(False)

    for tick in plt_labels[::step]:
        tick.set_visible(True)


def plot_all_series_to_graph(ax, history):
    """Plot all data series onto the graph."""
    # x-axis value
    x_axis = get_values_as_str(history, "date")

    # y-axis values (series)
    statements = get_values_as_int(history, "statements")
    missed = get_values_as_int(history, "missed")
    covered = compute_covered(statements, missed)

    ax.plot(x_axis, statements, "b-", label="Statements")
    ax.plot(x_axis, missed, "r-", label="Missed")
    ax.plot(x_axis, covered, "g-", label="Covered")


def draw_graph(repo_to_measure, history):
    """Draw graph with code coverage history."""
    fig = plt.figure(1, figsize=(1.0 * DEFAULT_WIDTH / DPI, 1.0 * DEFAULT_HEIGHT / DPI), dpi=DPI)
    ax = fig.add_axes([0.05, 0.20, 0.90, 0.60])

    title = "Code coverage history for the " + repo_to_measure
    fig.suptitle(title, fontsize=16)

    # show grid in graph
    ax.grid(which='both')

    plot_all_series_to_graph(ax, history)

    # make sure the y-axis starts at zero
    # NOTE: this needs to be called after all series are already added to the graph!
    ax.set_ylim(ymin=0)

    # show ticks in graph
    items = len(history)

    # TODO: make this part more inteligent
    step = 1
    if items > 20:
        step = 2
        if items > 40:
            step = 3
    setup_ticks(step)

    # add a legend to the graph
    ax.legend()

    filename = "code_coverage_history_{repo}.png".format(repo=repo_to_measure)
    fig.savefig(filename)

    # close the graph explicitly to save resources
    plt.close(fig)


def generate_graph_with_overall_coverage(hist_repo, commits, repo_to_measure):
    """Generate graph with the overall code coverage for the selected repository."""
    code_coverage_history = read_code_coverage_history(hist_repo, commits, repo_to_measure)

    # there's no need to generate graph with no value or with only one value
    if code_coverage_history is not None and len(code_coverage_history) >= 1:
        draw_graph(repo_to_measure, code_coverage_history)


def prepare_hist_repository(hist_repo):
    """Prepare the repository with history data.

    First, the repository is cloned or (if its been cloned already) new content is fetched.
    Additionaly, the repository is checkout to 'master' because we are not sure about its
    previous status.
    Then the log file with all commits is generated.
    """
    git_utils.clone_or_fetch_repository(hist_repo, full_history=True)
    git_utils.checkout(hist_repo, "master")
    git_utils.create_log(hist_repo)


def main():
    """Entry point to the CC history generator."""
    config = Config()
    hist_repo = config.get_repo_with_history_data()
    prepare_hist_repository(hist_repo)

    # generate graph for all supported repositories
    for repository in config.get_repolist():
        commits = git_utils.read_commits("repositories/logs.txt", COMMIT_MESSAGE_PATTERN)
        generate_graph_with_overall_coverage(hist_repo, commits, repository)


if __name__ == "__main__":
    # execute only if run as a script
    main()
