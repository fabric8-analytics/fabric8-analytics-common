"""HTML generator."""
from mako.template import Template


def generate_index_page(results):
    """Generate the main (index) HTML page with dashboard content."""
    template = Template(filename="template/dashboard.html")
    generated_page = template.render(**results.__dict__)
    with open("dashboard.html", "w") as fout:
        fout.write(generated_page)


def generate_details_page_for_repository(repository, results):
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
    generated_page = template.render(**data)
    filename = "repository_{repository}.html".format(repository=repository)
    with open(filename, "w") as fout:
        fout.write(generated_page)


def generate_dashboard(results):
    """Generate all pages with the dashboard and detailed information as well."""
    generate_index_page(results)
    if results.code_quality_table_enabled:
        for repository in results.repositories:
            generate_details_page_for_repository(repository, results)
