import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def create_component_analysis_timing_graph(durations):
    N = len(durations)

    selectors = ["security_issues", "github_details", "source_licenses",
                 "metadata", "keywords_tagging", "dependency_snapshot",
                 "digests", "code_metrics"]

    colors = ["#cc4040", "#cccc40", "#40cc40", "#40cccc",
              "#cccccc", "#804040", "#808040", "#408040"]

    fig, ax = plt.subplots()

    column1data = np.array([duration["overall"].duration_seconds
                           for duration in durations.values()])

    column2data = [np.array([duration[selector].duration_seconds
                            for duration in durations.values()]) for selector in selectors]

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35        # the width of the bars

    column1 = ax.bar(ind, column1data, width, color='orange')

    bottom = np.zeros(N)
    column2 = []
    for elem, color in zip(column2data, colors):
        column2.append(ax.bar(ind + width, elem, width, bottom=bottom, color=color))
        bottom += elem

    plt.ylabel('duration (seconds)')
    plt.title('component analysis')

    plt.xticks(ind, durations.keys())

    legend_labels = selectors[:]
    legend_labels.insert(0, "overall")

    legend_keys = [column1[0]]
    for c in column2:
        legend_keys.append(c[0])

    ax.legend(legend_keys, legend_labels)

    return fig


def create_graph(title, y_axis_label, labels, values):
    N = len(values)
    indexes = np.arange(N)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # major ticks every 20, minor ticks every 5
    major_ticks = np.arange(0, N + 1, 20)
    minor_ticks = np.arange(0, N + 1, 5)

    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)

    # and a corresponding grid
    ax.grid(which='both')

    # or if you want differnet settings for the grids:
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)

    plt.xlabel("call #")
    plt.ylabel(y_axis_label)

    plt.bar(indexes, values, 0.70, color='yellow',
            edgecolor='black', label=title)

    fig.suptitle(title)

    return fig


def create_summary_graph(title, y_axis_label, labels, values):
    N = len(values)
    indexes = np.arange(N)

    fig = plt.figure()
    plt.xlabel("call #")
    plt.ylabel(y_axis_label)
    plt.grid(True)
    plt.xticks(indexes, labels)
    locs, plt_labels = plt.xticks()
    plt.setp(plt_labels, rotation=90)
    plt.bar(indexes, values, 0.80, color='yellow',
            edgecolor='black', label=title)

    # plt.legend(loc='lower right')

    for tick in plt_labels:
        tick.set_horizontalalignment("left")
        tick.set_verticalalignment("top")
        tick.set_visible(False)

    for tick in plt_labels[::5]:
        tick.set_visible(True)

    plt.tick_params(axis='x', which='major', labelsize=10)

    fig.subplots_adjust(bottom=0.4)
    fig.suptitle(title)
    return fig


def create_statistic_graph(title, y_axis_label, labels, min_values, max_values, avg_values):
    N = len(labels)
    indexes = np.arange(N)

    fig = plt.figure()
    plt.xlabel("pause time (seconds)")
    plt.ylabel(y_axis_label)
    plt.grid(True)
    plt.xticks(indexes, labels)
    locs, plt_labels = plt.xticks()
    plt.setp(plt_labels, rotation=90)

    plt.bar(indexes - 0.27, min_values, 0.25, color='red',
            edgecolor='black', label='min values')
    plt.bar(indexes, avg_values, 0.25, color='yellow',
            edgecolor='black', label='avg values')
    plt.bar(indexes + 0.27, max_values, 0.25, color='green',
            edgecolor='black', label='max values')

    plt.legend(loc='upper left')
    for tick in plt_labels:
        tick.set_horizontalalignment("left")
        tick.set_verticalalignment("top")
    plt.tick_params(axis='x', which='major', labelsize=10)
    # fig.subplots_adjust(bottom=0.4)
    fig.suptitle(title)
    return fig


def save_graph(fig, imageFile):
    plt.savefig(imageFile, facecolor=fig.get_facecolor())


def generate_wait_times_graph(title, name, values):
    labels = range(1, 1 + len(values))
    fig = create_graph(title, "seconds", labels, values)
    save_graph(fig, name + ".png")
    plt.close(fig)


def generate_timing_statistic_graph(title, name, pauses, min_times, max_times, avg_times):
    labels = range(1, 1 + len(pauses))
    fig = create_statistic_graph(title, "seconds", pauses, min_times, max_times, avg_times)
    save_graph(fig, name + ".png")
    plt.close(fig)


def generate_component_analysis_timing_graph(durations):
    fig = create_component_analysis_timing_graph(durations)
    save_graph(fig, "test.png")
    plt.close(fig)
