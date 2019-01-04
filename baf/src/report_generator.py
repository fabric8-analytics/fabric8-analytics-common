"""Report generator from BAF."""

import csv
import xml.etree.cElementTree as ET


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
    root = ET.Element("html")
    head = ET.SubElement(root, "head")
    body = ET.SubElement(root, "body")
    ET.SubElement(body, "h1").text = "Test results"
    table = ET.SubElement(body, "table")
    table.attrib["border"] = "1"

    tr = ET.SubElement(table, "tr")

    ET.SubElement(tr, "th").text = "Test name"
    ET.SubElement(tr, "th").text = "URL"
    ET.SubElement(tr, "th").text = "Method"
    ET.SubElement(tr, "th").text = "Expected status"
    ET.SubElement(tr, "th").text = "Actual status"
    ET.SubElement(tr, "th").text = "Result"
    ET.SubElement(tr, "th").text = "Payload"

    for result in results.tests:
        test = result["Test"]
        status_code = str(result["Status code"]) or "N/A"
        payload = str(result["Payload"]) or "N/A"

        tr = ET.SubElement(table, "tr")

        ET.SubElement(tr, "td").text = test["Name"]
        ET.SubElement(tr, "td").text = result["Url"]
        ET.SubElement(tr, "td").text = test["Method"]
        ET.SubElement(tr, "td").text = test["Expected status"]
        ET.SubElement(tr, "td").text = status_code
        ET.SubElement(tr, "td").text = result["Result"]
        ET.SubElement(tr, "td").text = payload

    tree = ET.ElementTree(root)
    tree.write(filename, method="html")


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
