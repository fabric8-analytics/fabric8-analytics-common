"""Code coverage page generator."""

from mako.template import Template
import time

from repositories import Repositories
from source_files import get_source_files
from unit_tests import read_unit_test_coverage_for_week
from config import Config

from fastlog import log


class Results():
    """Class representing results gathered by the cc to be published."""

    def __init__(self):
        """Prepare empty result structure."""
        self.repositories = {}
        self.repo_prefix = "https://github.com/fabric8-analytics/"
        self.source_files = {}
        self.improvement = {}
        self.threshold = {}
        self.threshold_pass = {}
        self.coverage_pp = {}
        self.coverage_delta_perc = {}
        self.f = lambda number: '{0:.2f}'.format(number)  # function to format floating point number
        self.generated_on = time.strftime('%Y-%m-%d %H:%M:%S')
        self.unit_test_coverage = {}

    def __repr__(self):
        """Return textual representation of all results."""
        template = "Unit test coverage: {unit_test_coverage}\n"
        return template.format(unit_test_coverage=self.unit_test_coverage)


def generate_coverage_page(results, page_name):
    """Generate the code coverage HTML page with measured content."""
    template = Template(filename="template/{template}".format(template=page_name))
    generated_page = template.render(**results.__dict__)
    with open(page_name, "w") as fout:
        fout.write(generated_page)


def generate_coverage_pages(results):
    """Generate the code coverage HTML pages with measured content."""
    generate_coverage_page(results, "coverage.html")
    generate_coverage_page(results, "coverage2txt.html")


def log_improvements(repositories, results):
    """Log improvements in repositories."""
    with log.indent():
        for repository in repositories:
            log.info("{repository} : {improvement}".format(
                repository=repository, improvement=results.improvement[repository]))


def prepare_data_for_repositories(repositories, results, config):
    """Accumulate results."""
    results.repositories = repositories
    for repository in repositories:
        log.info(repository)
        with log.indent():
            results.source_files[repository] = get_source_files(repository)
            results.unit_test_coverage[repository] = []
            for week in range(0, 2):
                log.info("Week " + str(week))
                with log.indent():
                    coverage = read_unit_test_coverage_for_week(repository, week)
                    results.unit_test_coverage[repository].append(coverage)

            update_improvement(results, repository)
            update_coverage_delta(results, repository)
            update_coverage_threshold_pass(results, repository, config)
    log.info("Improvements")
    log_improvements(repositories, results)


def update_coverage_threshold_pass(results, repository, config):
    """Update the 'coverage threshold' message."""
    threshold = config.get_code_coverage_threshold_for_project(repository)
    coverage = read_unit_test_coverage_for_week(repository, 1)
    threshold_pass = None

    if coverage:
        coverage_value = coverage.get("coverage")
        if threshold is not None and coverage_value is not None:
            threshold_pass = int(coverage_value) >= threshold

    results.threshold[repository] = threshold
    results.threshold_pass[repository] = threshold_pass


def update_improvement(results, repository):
    """Update the 'improvement' message."""
    results.improvement[repository] = ""
    try:
        week0 = float(results.unit_test_coverage[repository][0].get("coverage"))
        week1 = float(results.unit_test_coverage[repository][1].get("coverage"))
        log.info("Improvement: {week0} -> {week1}".format(week0=week0, week1=week1))
        if week0 == week1:
            result = "same"
        elif week0 > week1:
            result = "worse"
        else:
            result = "better"
        results.improvement[repository] = result
    except Exception:
        pass


def update_coverage_delta(results, repository):
    """Update the pp and %."""
    results.coverage_pp[repository] = ""
    results.coverage_delta_perc[repository] = ""
    try:
        pp, percent = calculate_pp_coverage(results, repository)
        results.coverage_pp[repository] = int(pp)
        results.coverage_delta_perc[repository] = int(percent)
    except Exception:
        pass


def calculate_pp_coverage(results, repository):
    """Calculate the pp coverage for the selected repository."""
    week0 = float(results.unit_test_coverage[repository][0].get("coverage"))
    week1 = float(results.unit_test_coverage[repository][1].get("coverage"))
    if week0 == week1:
        return 0, 0
    elif week0 > week1:
        delta = week0 - week1
        return delta, 100.0 * delta / week1
    else:
        delta = week1 - week0
        if week0 == 0:
            return delta, 100.0
        else:
            return delta, 100.0 * delta / week0


def main():
    """Entry point to the CC reporter."""
    log.setLevel(log.INFO)

    log.info("Config")
    with log.indent():
        config = Config()
        results = Results()
        repositories = Repositories(config)
    log.success("Done")

    log.info("Prepare data for repositories")
    with log.indent():
        prepare_data_for_repositories(repositories.repolist, results, config)
    log.success("Done")

    log.info("Generate coverage pages")
    with log.indent():
        generate_coverage_pages(results)
    log.success("Done")


if __name__ == "__main__":
    # execute only if run as a script
    main()
