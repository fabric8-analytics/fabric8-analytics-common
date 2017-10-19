"""HTML generator."""
from mako.template import Template


def generate_dashboard(results):
    """Generate the HTML page with dashboard content."""
    print(results)
    template = Template(filename="template/dashboard.html")
    generated_page = template.render(**results.__dict__)
    with open("dashboard.html", "w") as fout:
        fout.write(generated_page)
