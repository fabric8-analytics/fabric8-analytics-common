"""Source file manipulation."""

import os

from fastlog import log


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
    log.info("Getting source files")
    command = ("pushd repositories/{repo} > /dev/null; " +
               r"wc -l `find . -path ./venv -prune -o \( -name '*.py' -o -name '*.java' \) " +
               "-print` | head -n -1 > ../../{repo}.count; " +
               "popd > /dev/null").format(repo=repository)
    os.system(command)
    filenames = []
    line_counts = {}
    total_lines = 0
    count = 0

    with log.indent():
        with open("{repo}.count".format(repo=repository)) as fin:
            for line in fin:
                with log.indent():
                    log.debug(line)
                count += 1
                line_count, filename = parse_line_count(line)
                filenames.append(filename)
                line_counts[filename] = line_count
                total_lines += line_count

        log.debug("Files: {files}".format(files=count))
        log.debug("Lines: {lines}".format(lines=total_lines))

    log.success("Done")

    return {"count": count,
            "filenames": filenames,
            "line_counts": line_counts,
            "total_lines": total_lines}
