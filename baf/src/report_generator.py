"""Report generator from BAF."""

import csv
import time
from fastlog import log
import xml.etree.cElementTree as ET
from mako.template import Template


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


def generate_timestamp():
    """Generate timestamp in human readable format."""
    return time.strftime('%Y-%m-%d %H:%M:%S')


def get_test_statistic(results):
    """Compute basic test statistic."""
    tests = len(results.tests)
    passed = len(list(r for r in results.tests if r["Success"]))
    failed = tests - passed

    if tests > 0:
        success_rate = "{0:.2f} %".format(100.0 * passed / tests)
    else:
        success_rate = "N/A"

    return tests, passed, failed, success_rate


def generate_html_report(tests, results, filename, cfg, total_time):
    """Generate HTML report with all BAF tests."""
    template = Template(filename="templates/results.html")

    statistic = {}
    all_tests, passed, failed, success_rate = get_test_statistic(results)
    statistic["tests"] = all_tests
    statistic["passed"] = passed
    statistic["failed"] = failed
    statistic["success_rate"] = success_rate
    statistic["total_time"] = "{0:.2f} s".format(total_time)

    data_for_template = {}
    data_for_template["configuration"] = cfg
    data_for_template["tests"] = tests
    data_for_template["results"] = results.tests
    data_for_template["generated_on"] = generate_timestamp()
    data_for_template["statistic"] = statistic
    data_for_template["header"] = cfg["header"]

    # generate HTML page using the provided data
    generated_page = template.render(**data_for_template)

    with open(filename, "w") as fout:
        fout.write(generated_page)


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
    root = ET.Element("test-results")

    for result in results.tests:
        test = result["Test"]
        status_code = str(result["Status code"]) or "N/A"
        payload = str(result["Payload"]) or "N/A"

        r = ET.SubElement(root, "result")
        ET.SubElement(r, "test-name").text = test["Name"]
        ET.SubElement(r, "endpoint").text = result["Url"]
        ET.SubElement(r, "method").text = test["Method"]
        ET.SubElement(r, "expected-status").text = test["Expected status"]
        ET.SubElement(r, "actual-status").text = status_code
        ET.SubElement(r, "test-result").text = result["Result"]
        ET.SubElement(r, "payload-result").text = payload

    tree = ET.ElementTree(root)
    tree.write(filename)


def generate_reports(tests, results, cfg, total_time):
    """Generate reports with all BAF tests."""
    log.info("Generate reports")
    with log.indent():
        # cfg contains information whether to generate HTML, CSV, TSV etc. outputs
        if cfg["generate_text"]:
            log.info("Text report")
            generate_text_report(results, cfg["generate_text"])
        if cfg["generate_html"]:
            log.info("HTML report")
            generate_html_report(tests, results, cfg["generate_html"], cfg, total_time)
        if cfg["generate_csv"]:
            log.info("CSV report")
            generate_csv_report(results, cfg["generate_csv"])
        if cfg["generate_tsv"]:
            log.info("TSV report")
            generate_tsv_report(results, cfg["generate_tsv"])
        if cfg["generate_xml"]:
            log.info("XML report")
            generate_xml_report(results, cfg["generate_xml"])
