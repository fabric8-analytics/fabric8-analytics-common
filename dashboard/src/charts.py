"""Charts generator."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import numpy as np

DEFAULT_WIDTH = 400
DEFAULT_HEIGHT = 400
DPI = 100


def save_graph(fig, imageFile, dpi=DPI):
    """Save graph into the raster or vector file."""
    plt.savefig(imageFile, facecolor=fig.get_facecolor(), dpi=dpi)


def pie_chart_for_repository(repository, labels, fractions, colors):
    """Prepare pie chart for given repository, sequence of labels, fractions, and colors."""
    fig = plt.figure(1, figsize=(1.0 * DEFAULT_WIDTH / DPI, 1.0 * DEFAULT_HEIGHT / DPI), dpi=DPI)
    ax = fig.add_axes([0.06, 0.00, 0.88, 0.88])
    fig.suptitle(repository, fontsize=16)

    patches, texts, autotexts = ax.pie(fractions, colors=colors, labels=labels, autopct='%1.1f%%',
                                       shadow=False)

    # font setup
    proptease = fm.FontProperties()
    proptease.set_size('small')
    plt.setp(autotexts, fontproperties=proptease)
    plt.setp(texts, fontproperties=proptease)

    return fig, ax


def prepare_data_for_cyclomatic_complexity_chart(cyclomatic_complexity):
    """Prepare data (values, labels, colors) for the cyclomatic complexity chart."""
    filtered_complexity = {k: v for k, v in cyclomatic_complexity.items()
                           if v > 0 and k != "status"}

    labels = sorted(filtered_complexity.keys())

    fractions = [filtered_complexity[key] for key in labels]

    colors = ('#60a060', 'yellow', 'orange', 'red', 'magenta', 'black')

    return labels, fractions, colors


def prepare_data_for_maintability_index(maintainability_index):
    """Prepare data (values, labels, colors) for the maintainability index chart."""
    filtered_index = {k: v for k, v in maintainability_index.items()
                      if v > 0 and k != "status"}

    labels = sorted(filtered_index.keys())

    fractions = [filtered_index[key] for key in labels]

    colors = ('#60a060', 'yellow', 'red')

    return labels, fractions, colors


def prepare_data_for_code_coverage(coverage_data):
    """Prepare data (values, labels, colors) for the unit test code coverage chart."""
    labels = ("covered", "not\ncovered")

    coverage = float(coverage_data["coverage"])
    coverage_ratio = coverage / 100.0
    fractions = [coverage_ratio, 1.0 - coverage_ratio]

    colors = ('#60a060', 'red')

    return labels, fractions, colors


def prepare_fractions_from_common_results_struct(results):
    """Prepare list of fraction values for passed/failed tests."""
    correct = float(results["passed%"])
    incorrect = float(results["failed%"])
    return [correct, incorrect]


def prepare_data_for_dead_code_chart(dead_code_measurement):
    """Prepare data (values, labels, colors) for the dead code measurement chart."""
    labels = ("without\ndead code", "with\ndead code")
    fractions = prepare_fractions_from_common_results_struct(dead_code_measurement)
    colors = ('#40a040', 'red')
    return labels, fractions, colors


def prepare_data_for_common_errors_chart(common_errors):
    """Prepare data (values, labels, colors) for the common errors chart."""
    labels = ("without\nerrors", "at least 1\nerror detected")
    fractions = prepare_fractions_from_common_results_struct(common_errors)
    colors = ('#40a040', 'red')
    return labels, fractions, colors


def generate_cyclomatic_complexity_chart(repository, cyclomatic_complexity):
    """Generate chart with cyclomatic complexity data for given repository."""
    labels, fractions, colors = prepare_data_for_cyclomatic_complexity_chart(cyclomatic_complexity)
    fig, ax = pie_chart_for_repository(repository, labels, fractions, colors)

    filename = "cyclomatic_complexity_{repository}.png".format(repository=repository)
    save_graph(fig, filename, DPI)
    plt.close(fig)


def generate_maintainability_index_chart(repository, maintainability_index):
    """Generate chart with maintainability index data for given repository."""
    labels, fractions, colors = prepare_data_for_maintability_index(maintainability_index)
    fig, ax = pie_chart_for_repository(repository, labels, fractions, colors)

    filename = "maintainability_index_{repository}.png".format(repository=repository)
    save_graph(fig, filename, DPI)
    plt.close(fig)


def generate_code_coverage_chart(repository, code_coverage):
    """Generate chart with code coverage chart for given repository."""
    if code_coverage is not None:
        labels, fractions, colors = prepare_data_for_code_coverage(code_coverage)
        fig, ax = pie_chart_for_repository(repository, labels, fractions, colors)

        filename = "code_coverage_{repository}.png".format(repository=repository)
        save_graph(fig, filename, DPI)
        plt.close(fig)


def generate_dead_code_chart(repository, dead_code_measurement):
    """Generate chart with dead code measurement."""
    if dead_code_measurement is not None:
        labels, fractions, colors = prepare_data_for_dead_code_chart(dead_code_measurement)
        fig, ax = pie_chart_for_repository(repository, labels, fractions, colors)

        filename = "dead_code_{repository}.png".format(repository=repository)
        save_graph(fig, filename, DPI)
        plt.close(fig)


def generate_common_errors_chart(repository, common_errors):
    """Generate chart with common errors measurement."""
    if common_errors is not None:
        labels, fractions, colors = prepare_data_for_common_errors_chart(common_errors)
        fig, ax = pie_chart_for_repository(repository, labels, fractions, colors)

        filename = "common_errors_{repository}.png".format(repository=repository)
        save_graph(fig, filename, DPI)
        plt.close(fig)


def generate_charts(results):
    """Generate all charts for the QA dashboard."""
    for repository in results.repositories:
        generate_cyclomatic_complexity_chart(repository,
                                             results.repo_cyclomatic_complexity[repository])
        generate_maintainability_index_chart(repository,
                                             results.repo_maintainability_index[repository])
        generate_code_coverage_chart(repository,
                                     results.unit_test_coverage[repository])
        generate_dead_code_chart(repository, results.dead_code[repository])
        generate_common_errors_chart(repository, results.common_errors[repository])


if __name__ == "__main__":
    # execute only if this module is run as a script
    # (just test charts)

    # cyclomatic complexity charts
    data = {"A": 749, "B": 48, "C": 3, "D": 0, "E": 0, "F": 0, "status": True}
    generate_cyclomatic_complexity_chart("fabric8-analytics-common", data)

    data = {"A": 276, "B": 21, "C": 12, "D": 0, "E": 0, "F": 0, "status": True}
    generate_cyclomatic_complexity_chart("fabric8-analytics-server", data)

    # code coverage charts
    data = {"statements": "1000",
            "missed": "500",
            "coverage": "50",
            "progress_bar_class": "something",
            "progress_bar_width": "ignore"}
    generate_code_coverage_chart("fabric8-analytics-common", data)

    data = {"statements": "1000",
            "missed": "100",
            "coverage": "10",
            "progress_bar_class": "something",
            "progress_bar_width": "ignore"}
    generate_code_coverage_chart("fabric8-analytics-server", data)

    data = {"statements": "1000",
            "missed": "900",
            "coverage": "90",
            "progress_bar_class": "something",
            "progress_bar_width": "ignore"}
    generate_code_coverage_chart("fabric8-analytics-something-else", data)

    data = {"display_results": True,
            "files": 100,
            "total": 100,
            "passed": 35,
            "failed": 65,
            "passed%": "35",
            "failed%": "65"}
    generate_dead_code_chart("fabric8-analytics-something-else", data)

    data = {"display_results": True,
            "files": 100,
            "total": 100,
            "passed": 35,
            "failed": 65,
            "passed%": "35",
            "failed%": "65"}
    generate_common_errors_chart("fabric8-analytics-something-else", data)
