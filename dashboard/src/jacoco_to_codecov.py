"""Module to convert JaCoCo coverage report into the report compatible with Pycov utility."""

import csv


def format_coverage_line(text, statements, missed, coverage, missed_lines=False):
    """Format one line with code coverage report of one class or for a summary."""
    format_string = "{:80}   {:3d}  {:3d}   {:3d}%"
    if missed_lines:
        format_string += "   N/A"
    return format_string.format(text, statements, missed, coverage)


def compute_coverage(statements, covered):
    """Compute code coverage based on number of all statemts and number of covered statements."""
    return 100.0 * covered / statements


class JavaClassCoverageReport:
    """Class representing code coverage report for one Java class."""

    def __init__(self, record):
        """Initialize the object by using record read from the CSV file."""
        self.group = record[0]
        self.package = record[1]
        self.class_name = record[2]
        self.missed = int(record[7])
        self.covered = int(record[8])
        self.statements = self.covered + self.missed
        self.coverage = compute_coverage(self.statements, self.covered)

    def __str__(self):
        """Return readable text representation compatible with Pycov utility output."""
        pc = "{package}/{class_name}".format(package=self.package, class_name=self.class_name)
        return format_coverage_line(pc, self.statements, self.missed, int(self.coverage))


class ProjectCoverageReport:
    """Class to perform conversion from JaCoCo output to report compatible with Pycov utility."""

    def __init__(self, csv_input_file_name):
        """Initialize the object, store the name of input (CSV) file."""
        self.csv_input_file_name = csv_input_file_name

    @staticmethod
    def read_csv(csv_input_file_name, skip_first_line=False):
        """Read the given CSV file, parse it, and return as list of records."""
        output = []
        with open(csv_input_file_name, 'r') as fin:
            csv_content = csv.reader(fin, delimiter=',')
            if skip_first_line:
                next(csv_content, None)
            for row in csv_content:
                output.append(row)
        return output

    @staticmethod
    def write_horizontal_rule(fout):
        """Write horizontal rule into the output file."""
        fout.write("-" * 108)
        fout.write("\n")

    @staticmethod
    def write_coverage_report_header(fout):
        """Write header compatible with Pycov to the output file."""
        fout.write("{:80} {:5} {:4}  {:5}   {}\n".format(
            "Name", "Stmts", "Miss", "Cover", "Missing"))
        ProjectCoverageReport.write_horizontal_rule(fout)

    @staticmethod
    def write_coverage_report_summary(fout, statements, missed, coverage):
        """Write summary compatible with Pycov to the output file."""
        ProjectCoverageReport.write_horizontal_rule(fout)
        fout.write(format_coverage_line("TOTAL", statements, missed, int(coverage)))
        fout.write("\n")

    def read_java_classes(self):
        """Read and parse into about Java classes from JaCoCo results."""
        data = ProjectCoverageReport.read_csv(self.csv_input_file_name, True)
        return [JavaClassCoverageReport(record) for record in data]

    def convert_code_coverage_report(self, output_file_name):
        """Convert code coverage report that would be compatible with PyCov output."""
        java_classes = self.read_java_classes()
        statements, missed, coverage = ProjectCoverageReport.compute_total(java_classes)
        with open(output_file_name, "w") as fout:
            ProjectCoverageReport.write_coverage_report_header(fout)
            for java_class in java_classes:
                fout.write(str(java_class) + "\n")
            ProjectCoverageReport.write_coverage_report_summary(fout, statements, missed, coverage)

    @staticmethod
    def compute_total(records):
        """Compute total/summary from all Java class coverage reports."""
        statements = 0
        covered = 0
        missed = 0
        for record in records:
            statements += record.statements
            covered += record.covered
            missed += record.missed
        coverage = compute_coverage(statements, covered)
        return statements, missed, coverage


def main():
    """Just a test ATM."""
    p = ProjectCoverageReport("fabric8-analytics-jenkins-plugin.coverage.csv")
    p.convert_code_coverage_report("fabric8-analytics-jenkins-plugin.coverage.txt")


if __name__ == "__main__":
    # execute only if run as a script
    main()
