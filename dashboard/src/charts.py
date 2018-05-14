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
    fig = plt.figure(1, figsize=(1.0 * DEFAULT_WIDTH / DPI, 1.0 * DEFAULT_WIDTH / DPI), dpi=DPI)
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


def generate_charts(results):
    """Generate all charts for the QA dashboard."""
    for repository in results.repositories:
        generate_cyclomatic_complexity_chart(repository,
                                             results.repo_cyclomatic_complexity[repository])
        generate_maintainability_index_chart(repository,
                                             results.repo_maintainability_index[repository])


if __name__ == "__main__":
    # execute only if this module is run as a script
    # (just test charts)

    # cyclomatic complexity charts
    data = {"A": 749, "B": 48, "C": 3, "D": 0, "E": 0, "F": 0, "status": True}
    generate_cyclomatic_complexity_chart("fabric8-analytics-common", data)

    data = {"A": 276, "B": 21, "C": 12, "D": 0, "E": 0, "F": 0, "status": True}
    generate_cyclomatic_complexity_chart("fabric8-analytics-server", data)
