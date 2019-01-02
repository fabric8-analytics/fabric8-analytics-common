"""Report generator from BAF."""


def generate_text_report(results):
    """Generate text report with all BAF tests."""
    template = "{:60s} {:75s} {:6s} {:20s} {:20s} {:20s} {:s}"
    output = template.format("Test name", "Endpoint", "Method",
                             "Expected status", "Actual status", "Test result", "Payload")
    for result in results.tests:
        test = result["Test"]
        status_code = str(result["Status code"]) or "N/A"
        payload = str(result["Payload"]) or "N/A"
        output = template.format(test["Name"], result["Url"], test["Method"],
                                 test["Expected status"], status_code, result["Result"],
                                 payload)
        print(output)


def generate_reports(results, cfg):
    """Generate reports with all BAF tests."""
    generate_text_report(results)
    # cfg contain information whether to generate HTML and/or CSV outputs
    print(cfg)
