"""HTML generator."""
from mako.template import Template

import logging
log = logging.getLogger(__file__)
log.setLevel(logging.DEBUG)


def generate_index_page(results):
    """Generate the main (index) HTML page with dashboard content."""
    template = Template(filename="template/dashboard.html")
    generated_page = template.render(**results.__dict__)
    with open("dashboard.html", "w") as fout:
        fout.write(generated_page)


def generate_metrics_page(results):
    """Generate the metrics HTML page with dashboard content."""
    template = Template(filename="template/metrics.html")
    generated_page = template.render(**results.__dict__)
    with open("metrics.html", "w") as fout:
        fout.write(generated_page)


def generate_details_page_for_repository(repository, results,
                                         ignored_pylint_files, ignored_pydocstyle_files):
    """Generate the page with detailed information about code in the selected repository."""
    template = Template(filename="template/repo_details.html")
    data = {}
    data["repository"] = repository
    data["files"] = results.source_files[repository]["filenames"]
    data["line_counts"] = results.source_files[repository]["line_counts"]
    data["linter_checks"] = results.repo_linter_checks[repository]["files"]
    data["docstyle_checks"] = results.repo_docstyle_checks[repository]["files"]
    data["generated_on"] = results.generated_on
    data["ci_jobs"] = results.ci_jobs_links
    data["ignored_pylint_files"] = ignored_pylint_files
    data["ignored_pydocstyle_files"] = ignored_pydocstyle_files
    generated_page = template.render(**data)
    filename = "repository_{repository}.html".format(repository=repository)
    with open(filename, "w") as fout:
        fout.write(generated_page)


def generate_charts_page_for_repository(repository, results):
    """Generate the page with charts for the selected repository."""
    template = Template(filename="template/charts.html")
    data = {}
    data["repository"] = repository
    data["generated_on"] = results.generated_on
    generated_page = template.render(**data)
    filename = "charts_{repository}.html".format(repository=repository)
    with open(filename, "w") as fout:
        fout.write(generated_page)


def generate_details_pages(results, ignored_files_for_pylint, ignored_files_for_pydocstyle):
    """Generate all details pages."""
    for repository in results.repositories:
        log.warning(repository)
        generate_details_page_for_repository(repository, results,
                                             ignored_files_for_pylint.get(repository, []),
                                             ignored_files_for_pydocstyle.get(repository, []))
        generate_charts_page_for_repository(repository, results)


def generate_dashboard(results, ignored_files_for_pylint, ignored_files_for_pydocstyle):
    """Generate all pages with the dashboard and detailed information as well."""
    log.warning("Generating output")

    # with log.indent():
    log.warning("Index page")
    generate_index_page(results)
    log.critical("Index page generated")

    # with log.indent():
    log.warning("Metrics page")
    generate_metrics_page(results)
    log.critical("Metrics page generated")

    # with log.indent():
    log.warning("Details about repository")
    if results.code_quality_table_enabled:
        generate_details_pages(results, ignored_files_for_pylint, ignored_files_for_pydocstyle)
    log.critical("Details generated")
    log.critical("Output generated")
