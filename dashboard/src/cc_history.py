"""Code coverage history generator.

This version creates a graph named `code_coverage_history_{repository}.png`
with the history of code coverage for all supported/measure repositories.

Source data for all graphs are retrieved from the 'history repository' with
QA Dashboard and its data.
"""


from config import *
import git_utils
import unit_tests
import history_generator


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
        commit_date = history_generator.get_commit_date(commit[1])
        git_utils.checkout(hist_repo, commit_hash)
        summary = read_summary(filename)
        if summary is not None:
            summary["date"] = commit_date
            code_coverage_history.append(summary)

    return code_coverage_history


def compute_covered(statements, missed):
    """Compute the sequence of 'covered' statements."""
    return history_generator.diff_two_lists(statements, missed)


def plot_code_coverage_series_to_graph(ax, history):
    """Plot all data series onto the graph."""
    # x-axis value
    x_axis = history_generator.get_values_as_str(history, "date")

    # y-axis values (series)
    statements = history_generator.get_values_as_int(history, "statements")
    missed = history_generator.get_values_as_int(history, "missed")
    covered = compute_covered(statements, missed)

    ax.plot(x_axis, statements, "b-", label="Statements")
    ax.plot(x_axis, missed, "r-", label="Missed")
    ax.plot(x_axis, covered, "g-", label="Covered")


def generate_graph_with_overall_coverage(hist_repo, commits, repo_to_measure):
    """Generate graph with the overall code coverage for the selected repository."""
    code_coverage_history = read_code_coverage_history(hist_repo, commits, repo_to_measure)

    # there's no need to generate graph with no value or with only one value
    if code_coverage_history is not None and len(code_coverage_history) >= 1:
        title = "Code coverage history for the " + repo_to_measure
        filename = "code_coverage_history_{repo}.png".format(repo=repo_to_measure)
        history_generator.draw_graph(title, filename, code_coverage_history,
                                     plot_code_coverage_series_to_graph)


def main():
    """Entry point to the CC history generator."""
    config = Config()
    hist_repo = config.get_repo_with_history_data()
    history_generator.prepare_hist_repository(hist_repo)

    # generate graph for all supported repositories
    for repository in config.get_repolist():
        commits = history_generator.read_history_commits()
        generate_graph_with_overall_coverage(hist_repo, commits, repository)


if __name__ == "__main__":
    # execute only if run as a script
    main()
