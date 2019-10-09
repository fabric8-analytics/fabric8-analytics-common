"""Dead code statistic and common errors statistic history generators.

Source data for all graphs are retrieved from the 'history repository' with
QA Dashboard and its data.
"""

import re
from config import Config
import git_utils
import history_generator
import csv

STARTING_DATE = "2018-06-01"


def line_with_summary(line, summary_postfix):
    """Check if the processed line contains dead code measurement summary."""
    return line.endswith(summary_postfix)


def parse_summary(line, pattern):
    """Parse the line containing dead code measurement summary."""
    pattern = re.compile(pattern)
    match = pattern.match(line)
    if len(match.groups()) == 2:
        return {"files_with_issues": match.group(1),
                "total_files": match.group(2)}
    else:
        return None


def line_with_check_passed(line, prefix):
    """Check if the processed line contains dead code measurement summary that passed."""
    return line.startswith(prefix)


def parse_check_passed(line, pattern):
    """Parse the line containing dead code measurement summary that passed."""
    pattern = re.compile(pattern)
    match = pattern.match(line)
    if len(match.groups()) == 1:
        return {"files_with_issues": 0,
                "total_files": match.group(1)}
    else:
        return None


def try_to_read_summary(filename, summary_postfix, summary_pattern, check_passed_prefix,
                        check_passed_pattern):
    """Try to read summary from the specified input file."""
    # it is ok if the file does not exist - the history data don't have to be
    # available in all commits
    with open(filename) as fin:
        for line in fin:
            if line_with_summary(line.strip(), summary_postfix):
                return parse_summary(line, summary_pattern)
            elif line_with_check_passed(line.strip(), check_passed_prefix):
                return parse_check_passed(line, check_passed_pattern)
    return None


def read_summary(filename, summary_postfix, summary_pattern, check_passed_prefix,
                 check_passed_pattern):
    """Read dead code summary from the file containing dead code or common errors report."""
    try:
        # this function might throws an exception
        return try_to_read_summary(filename, summary_postfix, summary_pattern, check_passed_prefix,
                                   check_passed_pattern)
    except Exception:
        return None


def get_filename_with_dead_code_stats(hist_repo, repo_to_measure):
    """Get the filename that contains dead code statistic."""
    return "repositories/{repo}/dashboard/{repo_to_measure}.dead_code.txt".format(
           repo=hist_repo, repo_to_measure=repo_to_measure)


def get_filename_with_common_errors_stats(hist_repo, repo_to_measure):
    """Get the filename that contains common errors statistic."""
    return "repositories/{repo}/dashboard/{repo_to_measure}.common_errors.txt".format(
           repo=hist_repo, repo_to_measure=repo_to_measure)


def read_history(hist_repo, commits, repo_to_measure, summary_postfix, summary_pattern,
                 checks_passed_prefix, checks_passed_pattern,
                 get_filename_function):
    """Read dead code history for the selected repository."""
    git_utils.checkout(hist_repo, "master")
    hist_repo = git_utils.update_repository_name(hist_repo)
    filename = get_filename_function(hist_repo, repo_to_measure)

    history = []

    # checkout to every commit and read the code coverage statistic
    for commit in commits:
        commit_hash = commit[0]
        commit_date = history_generator.get_commit_date(commit[1])
        git_utils.checkout(hist_repo, commit_hash)
        summary = read_summary(filename, summary_postfix, summary_pattern, checks_passed_prefix,
                               checks_passed_pattern)
        if summary is not None:
            summary["date"] = commit_date
            history.append(summary)

    return history


def compute_correct_files(all_files, incorrect_files):
    """Compute the sequence of 'correct' files."""
    return history_generator.diff_two_lists(all_files, incorrect_files)


def plot_series_to_graph(ax, history, all_files_label, incorrect_files_label, correct_files_label):
    """Plot all data series onto the graph."""
    # x-axis value
    x_axis = history_generator.get_values_as_str(history, "date")

    # y-axis values (series)
    files = history_generator.get_values_as_int(history, "total_files")
    incorrect = history_generator.get_values_as_int(history, "files_with_issues")
    correct = compute_correct_files(files, incorrect)

    ax.plot(x_axis, files, "b-", label=all_files_label)
    ax.plot(x_axis, incorrect, "r-", label=incorrect_files_label)
    ax.plot(x_axis, correct, "g-", label=correct_files_label)


def plot_common_series_to_graph(ax, history):
    """Plot all data series onto the graph."""
    plot_series_to_graph(ax, history, "All files", "With issue", "Without issue")


def plot_dead_code_series_to_graph(ax, history):
    """Plot all data series onto the graph."""
    plot_series_to_graph(ax, history, "All files", "Detected dead code", "Files w/o dead code")


def plot_common_errors_series_to_graph(ax, history):
    """Plot all data series onto the graph."""
    plot_series_to_graph(ax, history, "All files", "Detected common errors",
                         "Files w/o common errors")


def read_dead_code_history(hist_repo, commits, repo_to_measure):
    """Read dead code history for given repository."""
    return read_history(hist_repo, commits, repo_to_measure,
                        'seems to contain dead code and/or unused imports',
                        r'(\d+) source files out of (\d+) files seems',
                        'All checks passed for',
                        r'All checks passed for (\d+) source files',
                        get_filename_with_dead_code_stats)


def read_common_errors_history(hist_repo, commits, repo_to_measure):
    """Read common errors history for given repository."""
    return read_history(hist_repo, commits, repo_to_measure,
                        'files needs to be checked and fixed',
                        r'(\d+) source files out of (\d+) files needs',
                        'All checks passed for',
                        r'All checks passed for (\d+) source files',
                        get_filename_with_common_errors_stats)


def generate_graph_with_dead_code(repo_to_measure, dead_code_history):
    """Generate graph with the overall dead code for the selected repository."""
    # there's no need to generate graph with no value or with only one value
    if dead_code_history is not None and len(dead_code_history) >= 1:
        title = "Dead code history for the " + repo_to_measure
        filename = "dead_code_history_{repo}.png".format(repo=repo_to_measure)
        history_generator.draw_graph(title, filename, dead_code_history,
                                     plot_dead_code_series_to_graph)


def generate_graph_with_common_errors(repo_to_measure, common_errors_history):
    """Generate graph with the overall common errors statistic for the selected repository."""
    # there's no need to generate graph with no value or with only one value
    if common_errors_history is not None and len(common_errors_history) >= 1:
        title = "Common errors history for the " + repo_to_measure
        filename = "common_errors_history_{repo}.png".format(repo=repo_to_measure)
        history_generator.draw_graph(title, filename, common_errors_history,
                                     plot_common_errors_series_to_graph)


def issues_data(record):
    """Retrieve issues data from record."""
    total = int(record["total_files"])
    issues = int(record["files_with_issues"])
    correct = total - issues
    return total, issues, correct


def generate_csv(filename, history):
    """Generate CVS file for given repository."""
    with open(filename, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow(["Date", "Total sources", "Sources with issues", "Correct sources"])
        for i in history:
            date = i["date"]
            total, issues, correct = issues_data(i)
            writer.writerow([date, total, issues, correct])


def generate_csv_with_dead_code(repo_to_measure, dead_code_history):
    """Generate CVS file with dead code history for given repository."""
    if dead_code_history is not None:
        filename = "dead_code_history_{repo}.csv".format(repo=repo_to_measure)
        generate_csv(filename, dead_code_history)


def generate_csv_with_common_errors(repo_to_measure, common_errors_history):
    """Generate CVS file with common errors history for given repository."""
    if common_errors_history is not None:
        filename = "common_errors_history_{repo}.csv".format(repo=repo_to_measure)
        generate_csv(filename, common_errors_history)


def find_repo_data_for_commit(commit_date, records):
    """Find code metrics data in repodata for given commit date."""
    if records is None:
        return "", "", ""
    for i in records:
        if i["date"] == commit_date:
            return issues_data(i)
    # fallback - the first date data
    if len(records) >= 1:
        i = records[0]
        return issues_data(i)
    else:
        return 0, 0, 0


def get_csv_header(repositories):
    """Generate CSV header."""
    row = ["Repository"]

    for repository in repositories:
        row.append(repository)
        row.append("")
        row.append("")

    row.append("Summary")
    row.append("")
    row.append("")
    return row


def get_date_row(repositories):
    """Generate row with dates."""
    row = ["Date"]
    for repository in repositories:
        row.append("Sources")
        row.append("Issues")
        row.append("Correct")

    # one more for summary
    row.append("Sources")
    row.append("Issues")
    row.append("Correct")

    return row


def get_repodata_row_for_commit(commit_date, repositories, all_data):
    """Retrieve repodata for all repositories for selected commit."""
    row = []
    row.append(commit_date)
    sumtotal = 0
    sumissues = 0
    sumcorrect = 0
    for repository in repositories:
        total, issues, correct = find_repo_data_for_commit(commit_date, all_data[repository])
        row.append(total)
        row.append(issues)
        row.append(correct)
        sumtotal += total
        sumissues += issues
        sumcorrect += correct

    # summary
    row.append(sumtotal)
    row.append(sumissues)
    row.append(sumcorrect)
    return row


def summary_for_commit(commit_date, repositories, all_data):
    """Compute summary for given date."""
    sumtotal = 0
    sumissues = 0
    sumcorrect = 0
    for repository in repositories:
        total, issues, correct = find_repo_data_for_commit(commit_date, all_data[repository])
        sumtotal += total
        sumissues += issues
        sumcorrect += correct

    return sumtotal, sumissues, sumcorrect


def generate_csv_with_all_history(repositories, commits, filename, all_data):
    """Generate CSV file with all history data."""
    with open(filename, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow(get_csv_header(repositories))
        writer.writerow(get_date_row(repositories))

        for commit in commits:
            commit_date = history_generator.get_commit_date(commit[1])
            row = get_repodata_row_for_commit(commit_date, repositories, all_data)
            writer.writerow(row)


def generate_graph_with_all_history(repositories, commits, filename, title, all_data,
                                    starting_date):
    """Generate graph with the whole history of common issues/dead code for all repositories."""
    history = []
    ignore_old_commits = True

    for commit in commits:
        commit_date = history_generator.get_commit_date(commit[1])
        if commit_date == starting_date:
            ignore_old_commits = False

        if not ignore_old_commits:
            total, issues, correct = summary_for_commit(commit_date, repositories, all_data)
            history.append({"date": commit_date,
                            "total_files": total,
                            "files_with_issues": issues})

    history_generator.draw_graph(title, filename, history,
                                 plot_common_series_to_graph)


def main():
    """Entry point to the dead code history generator."""
    config = Config()
    hist_repo = config.get_repo_with_history_data()
    history_generator.prepare_hist_repository(hist_repo)
    all_dead_code = {}
    all_common_errors = {}

    repositories = config.get_repolist()

    # generate graph for all supported repositories
    for repository in repositories:
        commits = history_generator.read_history_commits()

        dead_code_history = read_dead_code_history(hist_repo, commits, repository)
        common_errors_history = read_common_errors_history(hist_repo, commits, repository)
        all_dead_code[repository] = dead_code_history
        all_common_errors[repository] = common_errors_history

        generate_graph_with_dead_code(repository, dead_code_history)
        generate_graph_with_common_errors(repository, common_errors_history)

        generate_csv_with_dead_code(repository, dead_code_history)
        generate_csv_with_common_errors(repository, common_errors_history)

    generate_graph_with_all_history(repositories, commits, "all_common_errors.png",
                                    "Common errors across all repositories",
                                    all_common_errors, STARTING_DATE)

    generate_graph_with_all_history(repositories, commits, "all_dead_code.png",
                                    "Dead code across all repositories",
                                    all_dead_code, STARTING_DATE)

    generate_csv_with_all_history(repositories, commits, "all_common_errors.csv", all_common_errors)
    generate_csv_with_all_history(repositories, commits, "all_dead_code.csv", all_dead_code)


if __name__ == "__main__":
    # execute only if run as a script
    main()
