import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

DEFAULT_WIDTH = 1680
DEFAULT_HEIGHT = 800
DPI = 100


def seconds_for_analysis(duration, measurement_type, selector):
    if measurement_type in duration:
        data = duration[measurement_type]
        if selector in data:
            return data[selector].duration_seconds
    return 0


def add_legend(ax, columns, component_selectors, component_colors,
               package_selectors, package_colors):
    legend_labels = []
    legend_labels.append("component: overall")

    for label in component_selectors:
        legend_labels.append(label)

    legend_labels.append("package: overall")

    for label in package_selectors:
        legend_labels.append(label)

    legend_keys = []
    legend_keys.append(columns[0][0])

    for c in columns[1]:
        legend_keys.append(c[0])

    legend_keys.append(columns[2][0])

    for c in columns[3]:
        legend_keys.append(c[0])

    ax.legend(legend_keys, legend_labels)


def stacked_column(measurements, ind, ax, columndata, colors, width, offset):
    bottom = np.zeros(measurements)
    column = []
    for elem, color in zip(columndata, colors):
        column.append(ax.bar(ind + offset, elem, width, bottom=bottom, color=color))
        bottom += elem
    return column


def create_component_analysis_timing_graph(durations, width=DEFAULT_WIDTH,
                                           height=DEFAULT_HEIGHT, dpi=DPI):
    N = len(durations)

    component_selectors = ["security_issues", "source_licenses",
                           "metadata", "keywords_tagging", "dependency_snapshot",
                           "digests", "code_metrics"]

    package_selectors = ["github_details", "keywords_tagging", "libraries_io"]

    component_colors = ["#cc4040", "#cccc40", "#40cc40", "#40cccc",
                        "#cccccc", "#804040", "#808040", "#408040"]

    package_colors = ["#0040cc", "#ff4040", "#40ff40"]

    fig, ax = plt.subplots(figsize=(1.0 * width / dpi, 1.0 * height / dpi), dpi=dpi)

    columndata = []
    columndata.append(np.array([duration["core-data"]["overall"].duration_seconds
                      for duration in durations.values()]))

    columndata.append([np.array([seconds_for_analysis(duration, "core-data", selector)
                                for duration in durations.values()])
                      for selector in component_selectors])

    columndata.append(np.array([duration["core-package-data"]["overall"].duration_seconds
                      for duration in durations.values()]))

    columndata.append([np.array([seconds_for_analysis(duration, "core-package-data", selector)
                                for duration in durations.values()])
                      for selector in package_selectors])

    ind = np.arange(N)   # the x locations for the groups
    width = 0.30         # the width of the bars
    offset = width / 3   # offset for the second column(s)

    pitch = width + 0.2  # pitch between component and package column tuples

    columns = []
    columns.append(ax.bar(ind, columndata[0], width, color='orange'))
    columns.append(stacked_column(N, ind, ax, columndata[1], component_colors, width, offset))
    columns.append(ax.bar(ind + pitch, columndata[2], width, color='yellow'))
    columns.append(stacked_column(N, ind, ax, columndata[3], package_colors, width, offset + pitch))

    plt.ylabel('duration (seconds)')
    plt.title('component analysis')
    plt.xticks(ind, durations.keys())

    add_legend(ax, columns, component_selectors, component_colors, package_selectors,
               package_colors)

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


def create_statistic_graph(title, y_axis_label, labels, min_values, max_values, avg_values,
                           x_axis_label="pause time (seconds)", width=DEFAULT_WIDTH,
                           height=DEFAULT_HEIGHT, dpi=DPI):
    N = len(labels)
    indexes = np.arange(N)

    fig = plt.figure(figsize=(1.0 * width / dpi, 1.0 * height / dpi), dpi=dpi)
    plt.xlabel(x_axis_label)
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


def save_graph(fig, imageFile, dpi=DPI):
    plt.savefig(imageFile, facecolor=fig.get_facecolor(), dpi=dpi)


def generate_wait_times_graph(title, name, values):
    labels = range(1, 1 + len(values))
    fig = create_graph(title, "seconds", labels, values)
    save_graph(fig, name + ".png")
    plt.close(fig)


def generate_timing_statistic_graph(title, name, pauses, min_times, max_times, avg_times,
                                    width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
    labels = range(1, 1 + len(pauses))
    fig = create_statistic_graph(title, "seconds", pauses, min_times, max_times, avg_times,
                                 "#", width, height)
    save_graph(fig, name + ".png")
    plt.close(fig)


def generate_timing_threads_statistic_graph(title, name, threads, min_times, max_times,
                                            avg_times):
    labels = range(1, 1 + len(threads))
    fig = create_statistic_graph(title, "seconds", threads, min_times, max_times, avg_times,
                                 "# concurrent analysis")
    save_graph(fig, name + ".png")
    plt.close(fig)


def generate_component_analysis_timing_graph(durations):
    fig = create_component_analysis_timing_graph(durations)
    save_graph(fig, "test.png")
    plt.close(fig)
