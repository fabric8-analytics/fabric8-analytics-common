"""Report generator from BAF."""

import csv


def generate_text_report(results, filename):
    """Generate text report with all BAF tests."""
    with open(filename, "w", encoding="utf8") as fout:
        template = "{:60s} {:75s} {:6s} {:20s} {:20s} {:20s} {:s}"
        output = template.format("Test name", "Endpoint", "Method",
                                 "Expected status", "Actual status", "Test result", "Payload")
        print(output, file=fout)
        for result in results.tests:
            test = result["Test"]
            status_code = str(result["Status code"]) or "N/A"
            payload = str(result["Payload"]) or "N/A"
            output = template.format(test["Name"], result["Url"], test["Method"],
                                     test["Expected status"], status_code, result["Result"],
                                     payload)
            print(output, file=fout)


def generate_html_report(results, filename):
    """Generate HTML report with all BAF tests."""
    print(filename)


def generate_csv_report(results, filename):
    """Generate CSV report with all BAF tests."""
    with open(filename, 'w', encoding='utf8') as fout:
        csv_writer = csv.writer(fout)
        csv_writer.writerow(["Test name", "Endpoint", "Method",
                             "Expected status", "Actual status", "Test result", "Payload"])
        for result in results.tests:
            test = result["Test"]
            status_code = str(result["Status code"]) or "N/A"
            payload = str(result["Payload"]) or "N/A"
            csv_writer.writerow([test["Name"], result["Url"], test["Method"],
                                 test["Expected status"], status_code, result["Result"],
                                 payload])


def generate_tsv_report(results, filename):
    """Generate TSV report with all BAF tests."""
    with open(filename, 'w', encoding='utf8', newline='') as fout:
        csv_writer = csv.writer(fout, delimiter='\t', lineterminator='\n')
        csv_writer.writerow(["Test name", "Endpoint", "Method",
                             "Expected status", "Actual status", "Test result", "Payload"])
        for result in results.tests:
            test = result["Test"]
            status_code = str(result["Status code"]) or "N/A"
            payload = str(result["Payload"]) or "N/A"
            csv_writer.writerow([test["Name"], result["Url"], test["Method"],
                                 test["Expected status"], status_code, result["Result"],
                                 payload])


def generate_xml_report(results, filename):
    """Generate XML report with all BAF tests."""
    print(filename)


def generate_reports(results, cfg):
    """Generate reports with all BAF tests."""
    # cfg contain information whether to generate HTML, CSV, TSV etc. outputs
    if cfg["generate_text"]:
        generate_text_report(results, cfg["generate_text"])
    if cfg["generate_html"]:
        generate_html_report(results, cfg["generate_html"])
    if cfg["generate_csv"]:
        generate_csv_report(results, cfg["generate_csv"])
    if cfg["generate_tsv"]:
        generate_tsv_report(results, cfg["generate_tsv"])
    if cfg["generate_xml"]:
        generate_xml_report(results, cfg["generate_xml"])
