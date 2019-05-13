"""Functions to export all measurements and metrics into CSV files."""
import csv
import datetime


def export_dashboard_api_into_csv(results, repositories):
    """Export Dashboard API into CSV and append it to previous results."""
    record = [
        datetime.date.today().strftime("%Y-%m-%d"),
        int(results.stage["core_api_available"]),
        int(results.stage["jobs_api_available"]),
        int(results.stage["core_api_auth_token"]),
        int(results.stage["jobs_api_auth_token"]),
        int(results.production["core_api_available"]),
        int(results.production["jobs_api_available"]),
        int(results.production["core_api_auth_token"]),
        int(results.production["jobs_api_auth_token"])
    ]

    for repository in repositories:
        record.append(results.source_files[repository]["count"])
        record.append(results.source_files[repository]["total_lines"])
        record.append(results.repo_linter_checks[repository]["total"])
        record.append(results.repo_linter_checks[repository]["passed"])
        record.append(results.repo_linter_checks[repository]["failed"])
        record.append(results.repo_docstyle_checks[repository]["total"])
        record.append(results.repo_docstyle_checks[repository]["passed"])
        record.append(results.repo_docstyle_checks[repository]["failed"])

    with open('dashboard_api.csv', 'a') as fout:
        writer = csv.writer(fout)
        writer.writerow(record)


def export_code_coverage_into_csv(results, repositories):
    """Export code coverage report into CSV."""
    with open('coverage.csv', 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow(("Repository",
                         "Statements", "Missed", "Coverage",
                         "Threshold", "Pass?"))
        for repository in repositories:
            coverage = results.unit_test_coverage[repository]
            if coverage is not None:
                cov = coverage.get("coverage")
                cov_pass = int(cov) >= 90
                writer.writerow((repository,
                                 coverage["statements"], coverage["missed"],
                                 str(cov) + "%" or "N/A",
                                 "90%",
                                 "yes" if cov_pass else "no"
                                 ))
            else:
                writer.writerow((repository,
                                 "N/A", "N/A", "N/A",
                                 "90%",
                                 "no"))


def export_dashboard_into_csv(results, repositories):
    """Export dashboard data report into CSV."""
    with open('dashboard.csv', 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow(("Repository",
                         "Source files", "",
                         "Linter results", "", "",
                         "Pydocstyle results", "", "",
                         "Code coverage", "", "",
                         "Dead code", "Common issues",
                         "Cyclomatic complexity", "", "", "", "", "", "",
                         "Maintainability index", "", "", "",
                         "Overall status"))
        writer.writerow(("",
                         "Files", "Total lines",
                         "Pass", "Fail", "Pass %",
                         "Pass", "Fail", "Pass %",
                         "Statements", "Missed", "Coverage",
                         "", "",
                         "A", "B", "C", "D", "E", "F", "OK?",
                         "A", "B", "C", "OK?",
                         ""))
        for repository in repositories:
            source_files = results.source_files[repository]
            linter = results.repo_linter_checks[repository]
            docstyle = results.repo_docstyle_checks[repository]
            coverage = results.unit_test_coverage[repository]
            if coverage is None:
                cov_statements = "N/A"
                cov_missed = "N/A"
                cov_covered = "N/A"
            else:
                cov_statements = coverage["statements"]
                cov_missed = coverage["missed"]
                cov_covered = str(coverage.get("coverage")) + "%"
            dead_code = results.dead_code[repository]
            common_errors = results.common_errors[repository]
            cc = results.repo_cyclomatic_complexity[repository]
            mi = results.repo_maintainability_index[repository]

            writer.writerow((repository,
                             source_files["count"], source_files["total_lines"],
                             linter["passed"], linter["failed"],
                             str(linter["passed%"]) + "%",
                             docstyle["passed"], docstyle["failed"],
                             str(docstyle["passed%"]) + "%",
                             cov_statements, cov_missed, cov_covered,
                             dead_code["failed"], common_errors["failed"],
                             cc["A"], cc["B"], cc["C"], cc["D"], cc["E"], cc["F"],
                             "yes" if cc["status"] else "no",
                             mi["A"], mi["B"], mi["C"],
                             "yes" if mi["status"] else "no",
                             "ok" if results.overall_status[repository] else "failure(s) found"
                             ))


def export_into_csv(results, repositories):
    """Export the results into CSV file."""
    export_dashboard_api_into_csv(results, repositories)
    export_code_coverage_into_csv(results, repositories)
    export_dashboard_into_csv(results, repositories)
