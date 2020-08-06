"""Code quality label generator."""

from fastlog import log

import svgwrite

MARKS = ['A+++', 'A++', 'A+', 'A', 'B', 'C', 'D', 'E', 'F']


def color(marks, index):
    """Compute color for given mark index."""
    steps_of_color = int(256 / len(marks) * 2) - 1
    index_of_yellow_label = int(len(marks) / 2)

    if index < index_of_yellow_label:
        r = abs(0 - index) * steps_of_color
        g = 255
        return 'fill:rgb({} {} {});'.format(r, g, 0)

    elif index > index_of_yellow_label:
        g = 255 - abs(index_of_yellow_label - index) * steps_of_color
        r = 255
        return 'fill:rgb({} {} {});'.format(r, g, 0)
    return 'fill:rgb({} {} {});'.format(255, 255, 0)  # yellow label


def generate_labels(height, width, marks, index, container_px=0, container_py=0):
    """Generate code quality label(s)."""
    steps_of_width = width / (2 * len(marks))  # first label has half of width
    steps_of_height = height / (2 * len(marks) - 1)
    height_of_labels = steps_of_height - height / 100

    container = Element([(container_px, container_py)], 'container', '')

    for i in range(0, len(marks)):
        points = [
            [0, 0 + i * steps_of_height],
            [width / 4 + i * steps_of_width, 0 + i * steps_of_height],
            [width / 4 + i * steps_of_width + width / 33,
             height_of_labels / 2 + i * steps_of_height],
            [width / 4 + i * steps_of_width, height_of_labels + i * steps_of_height],
            [0, height_of_labels + i * steps_of_height],
            [0, 0 + i * steps_of_height]
        ]
        print(points)

        polygon = Element(points, 'polygon',
                          style=color(marks, i) + 'stroke:black;stroke-width:2;')

        text = Element([(width / 20, height_of_labels / 2 + i * steps_of_height + 5)], 'text', '',
                       text=marks[i])
        container.add(polygon)
        container.add(text)

    pointer = [
        [width / 4 + index * steps_of_width + width / 33 * 3, steps_of_height * index],
        [width / 4 + index * steps_of_width + width / 33 * 2,
         steps_of_height * index + height_of_labels / 2],
        [width / 4 + index * steps_of_width + width / 33 * 3,
         steps_of_height * index + height_of_labels],
        [width, steps_of_height * index + height_of_labels],
        [width, steps_of_height * index]
    ]

    pointer = Element(pointer, 'polygon', style='fill:black;')

    container.add(pointer)

    container.add(Element(
        [(
            width / 4 + index * steps_of_width + width / 33 * 2 + (
                    width - width / 4 + index * steps_of_width + width / 33) / 25,
            steps_of_height * index + height_of_labels / 2 + 5
        )], 'text', 'white', text=marks[index]
    )
    )

    ymax = height_of_labels + (len(marks) - 1) * steps_of_height
    return container, ymax


class RootElement:
    """Root element of a drawing."""

    id = 0

    def __init__(self, x=1000, y=1000, constructor=svgwrite.Drawing, filename='labels.svg'):
        """Initialize drawing's root element."""
        self.constructor = constructor
        self.x = x
        self.y = y
        self.points = [(x, y)]

        self.elements = []
        self.type = 'svg'
        self.filename = filename
        self.id = 1 + RootElement.id
        RootElement.id += 1

    def __getitem__(self, item):
        """Get the element on n-th index."""
        return self.elements[item]

    def append(self, element):
        """Append new element."""
        self.elements.append(element)

    def add(self, element):
        """Add new element."""
        self.append(element)
        element.parent_element = self

    def build(self):
        """Build the drawing."""
        dwg = self.constructor(self.filename, ("{}pt".format(self.y), "{}pt".format(self.y)))

        for element in self.elements:
            element.build(dwg)
        dwg.save()

    def __str__(self):
        """Return string representation of the object."""
        return 'id: {} size: {} elements: {}'.format(self.id, self.points, self.elements)


class Element(RootElement):
    """An element of drawing."""

    def __init__(self, points, type_of_element, style, relative=True, text=None,
                 parent_element=None):
        """Initialize element of drawing."""
        self.type = type_of_element
        self.elements = []
        self.parent_element = parent_element
        self.points = points
        # print(points)
        self.relative = relative
        self.style = style
        self.text = text
        RootElement.id += 1
        self.id = RootElement.id
        # print(self.id)

    def compute_xmin_ymin(self):
        """Compute minimum x and y coordinates."""
        xmin = self.parent_element.points[0][0]
        ymin = self.parent_element.points[0][0]

        for x, y in self.parent_element.points:
            # print(xmin)
            # print(x)
            if xmin > x:
                xmin = x
            if ymin > y:
                ymin = y
        return xmin, ymin

    def count_real_x_y(self):
        """Count the x and y coordinates."""
        if not self.relative:
            return
        if self.parent_element.type == 'svg':
            xmin = 0
            ymin = 0
        else:
            xmin, ymin = self.compute_xmin_ymin()
        # print(self.points)
        points = [(x + xmin, y + ymin) for x, y in self.points]
        self.points = points

    def build_elements(self, dwg):
        """Build all elements."""
        for element in self.elements:
            # print(element)
            element.build(dwg)

    def build(self, dwg):
        """Build the elemend on drawing."""
        self.count_real_x_y()
        if self.type != 'container' or self.type == 'table':

            if self.type == 'polygon':
                new_el = svgwrite.shapes.Polygon(points=self.points, style=self.style)

            elif self.type == 'text':
                new_el = svgwrite.text.Text(self.text, (self.points[0][0], self.points[0][1]),
                                            fill=self.style)

            dwg.add(new_el)

        self.build_elements(dwg)

    def __len__(self):
        """Count all elements."""
        return len(self.elements)


class Table(Element):
    """Table with code quality metrics."""

    def __init__(self, points, length_of_row, length_of_column, padding=5, stroke_width=2,
                 parent_element=None, relative=True):
        """Initialize the table."""
        self.elements = []  # rows
        self.points = points
        self.length_of_row = length_of_row
        self.length_of_column = length_of_column
        self.padding = padding
        self.type = 'table'
        self.stroke_width = stroke_width
        self.parent_element = parent_element
        self.relative = relative
        self.type_of_element = 'table'
        self.id = 1 + RootElement.id
        RootElement.id += 1

    def build(self, dwg):
        """Build the table on drawing."""
        self.count_real_x_y()
        print(self.points)

        counter = 0
        for parameter, score in self.elements.items():  # todo add atribute font-size
            parameter = svgwrite.text.Text(parameter,
                                           (self.points[0][0] + 0.1 * self.length_of_column,
                                            self.points[0][1] +
                                            (0.5 + counter) * self.length_of_row + 5
                                            )
                                           )

            score = svgwrite.text.Text(score,
                                       (self.points[0][0] + 1.1 * self.length_of_column,
                                        self.points[0][1] + (0.5 + counter) * self.length_of_row + 5
                                        )
                                       )

            x = self.points[0][0]
            y = self.points[0][1]
            points = [
                (x, y + counter * self.length_of_row),
                (x + self.length_of_column, y + counter * self.length_of_row),
                (x + self.length_of_column, y + (counter + 1) * self.length_of_row),
                (x, y + (counter + 1) * self.length_of_row),
                (x, y + counter * self.length_of_row)
            ]
            first_column = svgwrite.shapes.Polygon(
                points, style='fill:none; stroke:black;stroke-width:{};'.format(self.stroke_width))

            points = [  # todo write list comprehnsion
                (x + self.length_of_column, y + counter * self.length_of_row),
                (x + self.length_of_column * 2, y + counter * self.length_of_row),
                (x + self.length_of_column * 2, y + (counter + 1) * self.length_of_row),
                (x + self.length_of_column, y + (counter + 1) * self.length_of_row),
                (x + self.length_of_column, y + counter * self.length_of_row)
            ]

            second_column = svgwrite.shapes.Polygon(
                points, style='fill:none; stroke:black;stroke-width:{};'.format(self.stroke_width))

            dwg.add(parameter)
            dwg.add(score)
            dwg.add(first_column)
            dwg.add(second_column)
            counter += 1


def percentage_to_mark(percentage):
    """Transform percentage values to mark label."""
    thresholds = {
        99: 'A+++',
        95: 'A++',
        90: 'A+',
        80: 'B',
        70: 'C',
        60: 'D',
        50: 'E',
        40: 'F'
    }
    for threshold, mark in thresholds.items():
        if percentage >= threshold:
            return mark
    return 'F'


def weight_pp(perc):
    """Compute the weighted percentage. The gravity is near 0%."""
    if perc > 75.0:
        return perc
    elif perc > 50.0:
        return perc * 0.75
    else:
        return perc * 0.5


def perc(part, total):
    """Compute percentage."""
    return weight_pp(100.0 * part / total)


def calculate_overall_percentage(pp):
    """Calculate overall percentage."""
    print(pp)
    return sum(pp) / len(pp)


def format_mark_percentage(mark, pp):
    """Format mark and percentage."""
    if mark == "N/A":
        return "N/A"
    else:
        return "{mark}  ({pp}%)".format(mark=mark, pp=int(pp))


def generate_quality_label_for_repository(repository, results):
    """Generate quality label for selected repository."""
    # some repositories don't have any Python code, so we don't have proper metrics for them ATM
    if not results.repo_linter_checks[repository]["display_results"]:
        return

    # raw input data
    files = len(results.source_files[repository]["line_counts"])
    linter = len(results.repo_linter_checks[repository]["files"])
    docstyle = len(results.repo_docstyle_checks[repository]["files"])

    if results.unit_test_coverage[repository] is not None:
        test_coverage = results.unit_test_coverage[repository]["coverage"]
    else:
        test_coverage = None

    common_issues = results.common_errors[repository]["failed"]
    dead_code = results.dead_code[repository]["failed"]
    cyclomatic_complexity = results.repo_cyclomatic_complexity[repository]
    maintainability_index = results.repo_maintainability_index[repository]

    # percentages and marks
    linter_perc = perc(linter, files)
    linter_mark = percentage_to_mark(linter_perc)

    docstyle_perc = perc(docstyle, files)
    docstyle_mark = percentage_to_mark(docstyle_perc)

    if test_coverage is not None:
        test_coverage_perc = weight_pp(int(test_coverage))
        test_coverage_mark = percentage_to_mark(test_coverage_perc)
    else:
        test_coverage_perc = "N/A"
        test_coverage_mark = "N/A"

    common_issues_perc = perc(files - common_issues, files)
    common_issues_mark = percentage_to_mark(common_issues_perc)

    dead_code_perc = perc(files - dead_code, files)
    dead_code_mark = percentage_to_mark(dead_code_perc)

    # we need to compute just the ranks from 'A' to 'F', not the overall status
    del cyclomatic_complexity["status"]
    cc_sum = sum(cyclomatic_complexity.values())
    cc_perc = perc(cyclomatic_complexity["A"], cc_sum)
    cc_mark = percentage_to_mark(cc_perc)

    # we need to compute just the ranks from 'A' to 'C', not the overall status
    del maintainability_index["status"]
    mi_sum = sum(maintainability_index.values())
    mi_perc = perc(maintainability_index["A"], mi_sum)
    mi_mark = percentage_to_mark(mi_perc)

    if test_coverage is not None:
        overall_perc = calculate_overall_percentage([linter_perc, docstyle_perc, test_coverage_perc,
                                                     common_issues_perc, dead_code_perc,
                                                     cc_perc, mi_perc])
    else:
        overall_perc = calculate_overall_percentage([linter_perc, docstyle_perc,
                                                     common_issues_perc, dead_code_perc,
                                                     cc_perc, mi_perc])

    overall_mark = percentage_to_mark(overall_perc)
    overall_mark_index = MARKS.index(overall_mark)

    drawing = RootElement(filename=repository + ".svg")
    container, ymax = generate_labels(500, 500, MARKS, overall_mark_index, 50, 50)

    table = Table([(0, ymax + 50)], 50, 250)
    table.elements = {'Score': str(int(overall_perc)) + " / 100",
                      'Overall': overall_mark,
                      'Coverage': format_mark_percentage(test_coverage_mark, test_coverage_perc),
                      'Common issues': format_mark_percentage(common_issues_mark,
                                                              common_issues_perc),
                      'Dead code': format_mark_percentage(dead_code_mark, dead_code_perc),
                      'Linter': format_mark_percentage(linter_mark, linter_perc),
                      'Documentation': format_mark_percentage(docstyle_mark, docstyle_perc),
                      'Code complexity': format_mark_percentage(cc_mark, cc_perc),
                      'Maintainability index': format_mark_percentage(mi_mark, mi_perc)}

    container.add(table)
    drawing.add(container)
    drawing.build()


def generate_quality_labels(results):
    """Generate quality labels for all repositories."""
    with log.indent():
        log.info("Generate quality labels")
        for repository in results.repositories:
            log.info(repository)
            generate_quality_label_for_repository(repository, results)
        log.success("Quality labels generated")


def main():
    """Entry point to the code quality label generator."""
    drawing = RootElement(filename="xyz.svg")
    container, ymax = generate_labels(500, 500, MARKS, 8, 50, 50)

    table = Table([(0, ymax + 50)], 50, 250)  # length_of_columns should be half of width
    table.elements = {'test': 'test', 'score': '59', 'foobar': 99}
    container.add(table)
    drawing.add(container)
    drawing.build()


if __name__ == "__main__":
    # execute only if run as a script
    main()
