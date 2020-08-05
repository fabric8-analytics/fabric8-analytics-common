"""Source file manipulation."""

import os

import logging
log = logging.getLogger(__file__)
log.setLevel(logging.DEBUG) 



def parse_line_count(line):
    """Parse the information with line counts."""
    line = line.strip()
    line_count, filename = line.split(" ")
    # remove prefix that is not relevant much
    if filename.startswith("./"):
        filename = filename[len("./"):]
    return int(line_count), filename


def get_file_extension(filename):
    """Get the file extension for any fil ename."""
    extension = os.path.splitext(filename)[1]
    if extension.startswith("."):
        return extension[1:]
    else:
        return extension


def get_source_files(repository):
    """Find all source files in the selected repository."""
    log.critical("Getting source files")
    command = ("pushd repositories/{repo} > /dev/null; " +
               r"wc -l `find . -path ./venv -prune -o \( -name '*.py' -o -name '*.java' -o " +
               r"-name '*.ts' \) " +
               "-print` | head -n -1 > ../../{repo}.count; " +
               "popd > /dev/null").format(repo=repository)
    os.system(command)
    filenames = []
    line_counts = {}
    total_lines = 0
    count = 0
    extensions = set()
    files_per_extension = {}

    #with log.indent():
    with open("{repo}.count".format(repo=repository)) as fin:
        for line in fin:
                #with log.indent():
            log.critical(line)
            count += 1
            line_count, filename = parse_line_count(line)
            extension = get_file_extension(filename)

                # register possibly new extension
            extensions.add(extension)

                # update file count for such extension
            files_per_extension[extension] = files_per_extension.get(extension, 0) + 1

                # register file name + line count
            filenames.append(filename)
            line_counts[filename] = line_count
            total_lines += line_count

    log.critical("Files: {files}".format(files=count))
    log.critical("Lines: {lines}".format(lines=total_lines))

    log.critical("Done")

    return {"count": count,
            "filenames": filenames,
            "extensions": extensions,
            "files_per_extension": files_per_extension,
            "line_counts": line_counts,
            "total_lines": total_lines}
