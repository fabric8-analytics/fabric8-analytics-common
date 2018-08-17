"""Helper functions to run external tools like Pylint, docstyle checker etc."""

import os
from fastlog import log


def run_pylint(repository):
    """Run Pylint checker against the selected repository."""
    with log.indent():
        log.info("Running Pylint for the repository " + repository)
        command = ("pushd repositories/{repo} >> /dev/null;" +
                   "./run-linter.sh > ../../{repo}.linter.txt;" +
                   "popd >> /dev/null").format(repo=repository)
        os.system(command)
        log.success("Done")


def run_docstyle_check(repository):
    """Run PyDocsStyle checker against the selected repository."""
    with log.indent():
        log.info("Running DocStyle checker for the repository " + repository)
        command = ("pushd repositories/{repo} >> /dev/null;" +
                   "./check-docstyle.sh > ../../{repo}.pydocstyle.txt;" +
                   "popd >> /dev/null").format(
            repo=repository)
        os.system(command)
        log.success("Done")


def run_cyclomatic_complexity_tool(repository):
    """Run Cyclomatic Complexity tool against the selected repository."""
    with log.indent():
        log.info("Running cyclomatic complexity checker for the repository " + repository)
        for i in range(ord('A'), 1 + ord('F')):
            rank = chr(i)
            command = ("pushd repositories/{repo} >> /dev/null;" +
                       "radon cc -a -s -n {rank} -i venv . |ansi2html.py > " +
                       "../../{repo}.cc.{rank}.html;" +
                       "popd >> /dev/null").format(repo=repository, rank=rank)
            os.system(command)

        command = ("pushd repositories/{repo} >> /dev/null;" +
                   "radon cc -s -j -i venv . > ../../{repo}.cc.json;" +
                   "popd >> /dev/null").format(repo=repository)
        os.system(command)
        log.success("Done")


def run_maintainability_index(repository):
    """Run Maintainability Index tool against the selected repository."""
    with log.indent():
        log.info("Running maintainability index checker for the repository " + repository)
        for i in range(ord('A'), 1 + ord('C')):
            rank = chr(i)
            command = ("pushd repositories/{repo} >> /dev/null;" +
                       "radon mi -s -n {rank} -i venv . | ansi2html.py " +
                       "> ../../{repo}.mi.{rank}.html;" +
                       "popd >> /dev/null").format(repo=repository, rank=rank)
            os.system(command)

        command = ("pushd repositories/{repo} >> /dev/null;" +
                   "radon mi -s -j -i venv . > ../../{repo}.mi.json;popd >> /dev/null"). \
            format(repo=repository)
        os.system(command)
        log.success("Done")


def run_dead_code_detector(repository):
    """Run dead code detector tool against the selected repository."""
    with log.indent():
        log.info("Running dead code detector for the repository " + repository)
        command = ("pushd repositories/{repo} >> /dev/null;" +
                   "./detect-dead-code.sh > ../../{repo}.dead_code.txt;" +
                   "popd >> /dev/null").format(repo=repository)
        os.system(command)
        log.success("Done")


def run_common_errors_detector(repository):
    """Run common issues detector tool against the selected repository."""
    with log.indent():
        log.info("Running common issues detector for the repository " + repository)
        command = ("pushd repositories/{repo} >> /dev/null;" +
                   "./detect-common-errors.sh > ../../{repo}.common_errors.txt;" +
                   "popd >> /dev/null").format(repo=repository)
        os.system(command)
        log.success("Done")
