"""Source file manipulation."""

import os


def parse_line_count(line):
    """Parse the information with line counts."""
    line = line.strip()
    line_count, filename = line.split(" ")
    # remove prefix that is not relevant much
    if filename.startswith("./"):
        filename = filename[len("./"):]
    return int(line_count), filename


def get_source_files(repository):
    """Find all source files in the selected repository."""
    command = ("pushd repositories/{repo} > /dev/null; " +
               "wc -l `find . -path ./venv -prune -o \( -name '*.py' -o -name '*.java' \) " +
               "-print` | head -n -1 > ../../{repo}.count; " +
               "popd > /dev/null").format(repo=repository)
    os.system(command)
    filenames = []
    line_counts = {}
    total_lines = 0
    count = 0

    with open("{repo}.count".format(repo=repository)) as fin:
        for line in fin:
            count += 1
            line_count, filename = parse_line_count(line)
            filenames.append(filename)
            line_counts[filename] = line_count
            total_lines += line_count

    return {"count": count,
            "filenames": filenames,
            "line_counts": line_counts,
            "total_lines": total_lines}
