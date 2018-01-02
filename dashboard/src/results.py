"""Results gathered by the Dashboard to be published."""

import time


class Results():
    """Class representing results gathered by the Dashboard to be published."""

    def __init__(self):
        """Prepare empty result structure."""
        self.stage = {}
        self.production = {}
        self.repositories = {}
        self.repo_statistics = {}
        self.repo_linter_checks = {}
        self.repo_docstyle_checks = {}
        self.repo_prefix = "https://github.com/fabric8-analytics/"
        self.source_files = {}
        self.overall_status = {}
        self.remarks = {}
        self.perf_tests_results = {}
        self.perf_tests_statistic = {}
        self.perf_tests_measurement_selectors = ["max", "avg", "sum"]
        self.perf_tests_measurement_titles = ["Max.time", "Avg.time", "Total time"]
        self.f = lambda number: '{0:.2f}'.format(number)  # function to format floating point number
        self.sla = {}
        self.smoke_tests_results = {}
        self.generated_on = time.strftime('%Y-%m-%d %H:%M:%S')
        self.ci_jobs = {}

    def __repr__(self):
        """Return textual representation of all results."""
        template = "Stage: {stage}\nProduction: {production}\n" + \
                   "Repo stats: {rs}\nRepo linter checks: {rl}\nRepo docstyle checks: {rd}\n" + \
                   "CI jobs: {ci}"
        return template.format(stage=self.stage,
                               production=self.production,
                               rs=self.repo_statistics,
                               rl=self.repo_linter_checks,
                               rd=self.repo_docstyle_checks,
                               ci=self.ci_jobs)
