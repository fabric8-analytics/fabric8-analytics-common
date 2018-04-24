"""Results gathered by the Dashboard to be published."""

import time
from collections import defaultdict


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
        self.repo_cyclomatic_complexity = {}
        self.repo_maintainability_index = {}
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
        self.smoke_tests_total_builds = 0
        self.smoke_tests_success_builds = 0
        self.smoke_tests_links = None
        self.smoke_tests_statuses = None
        self.generated_on = time.strftime('%Y-%m-%d %H:%M:%S')
        self.ci_jobs_links = defaultdict(dict)
        self.ci_jobs_statuses = defaultdict(dict)
        self.sprint = None
        self.sprint_plan_url = None
        self.teams = {}
        self.issues_list_url = {}
        self.unit_test_coverage = {}

    def __repr__(self):
        """Return textual representation of all results."""
        template = "Stage: {stage}\nProduction: {production}\n" + \
                   "Repo stats: {rs}\nRepo linter checks: {rl}\nRepo docstyle checks: {rd}\n" + \
                   "Smoke tests results: {smoke_tests_results}\n" + \
                   "Smoke tests links: {smoke_tests_links}\n" + \
                   "Smoke tests statuses: {smoke_tests_statuses}\n" + \
                   "CI jobs links: {ci_jobs_links}\n" + \
                   "CI jobs status: {ci_jobs_stats}\n" + \
                   "Unit test coverage: {unit_test_coverage}\n"
        return template.format(stage=self.stage,
                               production=self.production,
                               rs=self.repo_statistics,
                               rl=self.repo_linter_checks,
                               rd=self.repo_docstyle_checks,
                               smoke_tests_results=self.smoke_tests_results,
                               smoke_tests_links=self.smoke_tests_links,
                               smoke_tests_statuses=self.smoke_tests_statuses,
                               ci_jobs_links=self.ci_jobs_links.__repr__(),
                               ci_jobs_stats=self.ci_jobs_statuses.__repr__(),
                               unit_test_coverage=self.unit_test_coverage)
