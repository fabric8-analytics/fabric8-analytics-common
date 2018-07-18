"""Functions used to generate history graphs.

Source data for all graphs are retrieved from the 'history repository' with
QA Dashboard and its data.
"""

# NOTE: we have to use the following order of imports and matplotlib.use must be call between
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import re

import git_utils


# parameters for graph
# TODO: make these options configurable via config.ini
DEFAULT_WIDTH = 1024
DEFAULT_HEIGHT = 600
DPI = 100


# pattern used to check if the given commit contain history data
COMMIT_MESSAGE_PATTERN = r"Dashboard (20\d\d-\d\d-\d\d)"


def diff_two_lists(first, second):
    """Utility function to create new list with diffs between two other lists."""
    assert len(first) == len(second)
    return [x - y for x, y in zip(first, second)]


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


def get_commit_date(commit_message):
    """Get commit date directly from the message (we use parseable format)."""
    match = re.match(COMMIT_MESSAGE_PATTERN, commit_message)
    if match is not None:
        return match.group(1)
    else:
        return None


def read_history_commits():
    """Read all commits with 'proper' history records."""
    return git_utils.read_commits("repositories/logs.txt", COMMIT_MESSAGE_PATTERN)


def get_values_as_str(history, key):
    """Retrieve values from sequence of dictionaries."""
    return [i[key] for i in history]


def get_values_as_int(history, key):
    """Retrieve values from sequence of dictionaries, convert all values to int."""
    return [int(i[key]) for i in history]


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


def draw_graph(title, filename, history, plot_function):
    """Draw graph with code coverage history."""
    fig = plt.figure(1, figsize=(1.0 * DEFAULT_WIDTH / DPI, 1.0 * DEFAULT_HEIGHT / DPI), dpi=DPI)
    ax = fig.add_axes([0.05, 0.20, 0.90, 0.60])

    fig.suptitle(title, fontsize=16)

    # show grid in graph
    ax.grid(which='both')

    plot_function(ax, history)

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

    fig.savefig(filename)

    # close the graph explicitly to save resources
    plt.close(fig)
