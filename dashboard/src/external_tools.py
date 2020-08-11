"""Helper functions to run external tools like Pylint, docstyle checker etc."""

import os
import os.path
import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__file__)


def path_to_qa_file(repository, filename):
    """Find the directory where the given QA file is stored."""
    # currently, only two directories needs to be checked:
    # 1) repository root directory
    # 2) the QA subdirectory
    in_root_dir = os.path.isfile("repositories/{repo}/{filename}".format(
                                 repo=repository, filename=filename))
    in_qa_dir = os.path.isfile("repositories/{repo}/qa/{filename}".format(
                                 repo=repository, filename=filename))
    if in_root_dir:
        return "./{filename}".format(filename=filename)
    elif in_qa_dir:
        return "./qa/{filename}".format(filename=filename)
    else:
        # passthru
        return "./{filename}".format(filename=filename)


def run_pylint(repository):
    """Run Pylint checker against the selected repository."""
    # with log.indent():
    log.debug("Running Pylint for the repository " + repository)
    script = path_to_qa_file(repository, "run-linter.sh")
    command = ("pushd repositories/{repo} >> /dev/null;" +
               "{script} > ../../{repo}.linter.txt;" +
               "rm -rf venv;"
               "sleep 3;"
               "popd >> /dev/null").format(repo=repository, script=script)
    os.system(command)
    log.debug("Done")


def run_docstyle_check(repository):
    """Run PyDocsStyle checker against the selected repository."""
    # with log.indent():
    log.debug("Running DocStyle checker for the repository " + repository)
    script = path_to_qa_file(repository, "check-docstyle.sh")
    command = ("pushd repositories/{repo} >> /dev/null;" +
               "{script} > ../../{repo}.pydocstyle.txt;" +
               "sleep 3;"
               "popd >> /dev/null").format(
        repo=repository, script=script)
    os.system(command)
    log.debug("Done")


def run_cyclomatic_complexity_tool(repository):
    """Run Cyclomatic Complexity tool against the selected repository."""
    # with log.indent():
    log.debug("Running cyclomatic complexity checker for the repository " + repository)
    for i in range(ord('A'), 1 + ord('F')):
        rank = chr(i)
        command = ("pushd repositories/{repo} >> /dev/null;" +
                   "radon cc -a -s -n {rank} -i venv . |ansi2html > " +
                   "../../{repo}.cc.{rank}.html;" +
                   "popd >> /dev/null").format(repo=repository, rank=rank)
        os.system(command)

    command = ("pushd repositories/{repo} >> /dev/null;" +
               "radon cc -s -j -i venv . > ../../{repo}.cc.json;" +
               "popd >> /dev/null").format(repo=repository)
    os.system(command)
    log.debug("Done")


def run_maintainability_index(repository):
    """Run Maintainability Index tool against the selected repository."""
    # with log.indent():
    log.debug("Running maintainability index checker for the repository " + repository)
    for i in range(ord('A'), 1 + ord('C')):
        rank = chr(i)
        command = ("pushd repositories/{repo} >> /dev/null;" +
                   "radon mi -s -n {rank} -i venv . | ansi2html " +
                   "> ../../{repo}.mi.{rank}.html;" +
                   "popd >> /dev/null").format(repo=repository, rank=rank)
        os.system(command)

    command = ("pushd repositories/{repo} >> /dev/null;" +
               "radon mi -s -j -i venv . > ../../{repo}.mi.json;popd >> /dev/null"). \
        format(repo=repository)
    os.system(command)
    log.debug("Done")


def run_dead_code_detector(repository):
    """Run dead code detector tool against the selected repository."""
    # with log.indent():
    log.debug("Running dead code detector for the repository " + repository)
    script = path_to_qa_file(repository, "detect-dead-code.sh")
    command = ("pushd repositories/{repo} >> /dev/null;" +
               "rm -rf venv;{script} > ../../{repo}.dead_code.txt;" +
               "sleep 3;"
               "popd >> /dev/null").format(repo=repository, script=script)
    os.system(command)
    log.debug("Done")


def run_common_errors_detector(repository):
    """Run common issues detector tool against the selected repository."""
    # with log.indent():
    log.debug("Running common issues detector for the repository " + repository)
    script = path_to_qa_file(repository, "detect-common-errors.sh")
    command = ("pushd repositories/{repo} >> /dev/null;" +
               "{script} > ../../{repo}.common_errors.txt;" +
               "sleep 3;"
               "popd >> /dev/null").format(repo=repository, script=script)
    os.system(command)
    log.debug("Done")
