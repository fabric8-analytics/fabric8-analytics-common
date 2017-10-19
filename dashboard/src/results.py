"""Results gathered by the Dashboard to be published."""


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

    def __repr__(self):
        """Return textual representation of all results."""
        template = "Stage: {stage}\nProduction: {production}\n" + \
                   "Repo stats: {rs}\nRepo linter checks: {rl}\n Repo docstyle checks: {rd}"
        return template.format(stage=self.stage,
                               production=self.production,
                               rs=self.repo_statistics,
                               rl=self.repo_linter_checks,
                               rd=self.repo_docstyle_checks)
