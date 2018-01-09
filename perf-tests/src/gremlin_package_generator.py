"""Class that generates ecosystem+package and ecosystem+package+version tuples."""


class GremlinPackageGenerator:
    """Class that generates ecosystem+package and ecosystem+package+version tuples."""

    PACKAGES = {
        "npm": {
            "sequence": ["3.0.0"]
        },
        "maven": {
            "io.vertx:vertx-core": ["3.4.0"]
        },
        "pypi": {
            "clojure_py": ["0.2.0", "0.2.1", "0.2.2", "0.2.3", "0.2.4"],
            "ansicolors": ["1.0", "1.0.1", "1.0.2", "1.1.5", "1.1.6", "1.1.7",
                           "1.1.8"],
        }
    }

    @staticmethod
    def generate_ecosystem_package(ecosystem, packages):
        """Generate sequence of tuples containing ecosystem+package name pairs."""
        for package in packages:
            yield (ecosystem, package)

    @staticmethod
    def generate_ecosystem_package_version(ecosystem, packages):
        """Generate sequence of triples containing ecosystem+package name pairs."""
        for package, versions in packages.items():
            for version in versions:
                yield (ecosystem, package, version)

    @staticmethod
    def package_generator():
        """Provide generator for package specifications across all ecosystems."""
        # the inner for-loop generates a finite sequence of all valid
        # ecosystem+package combinations, but we need infinite sequence.
        # Thence we use outer infinite loop here
        while True:
            for ecosystem, packages in GremlinPackageGenerator.PACKAGES.items():
                yield from GremlinPackageGenerator.generate_ecosystem_package(ecosystem, packages)

    @staticmethod
    def package_version_generator():
        """Provide generator for package+version specifications across all ecosystems."""
        # the inner for-loop generates a finite sequence of all valid
        # ecosystem+package+version combinations, but we need infinite sequence.
        # Thence we use outer infinite loop here
        while True:
            for ecosystem, packages in GremlinPackageGenerator.PACKAGES.items():
                yield from GremlinPackageGenerator.generate_ecosystem_package_version(ecosystem,
                                                                                      packages)

    @staticmethod
    def package_generator_for_ecosystem(ecosystem='pypi'):
        """Provide generator for package specifications for selected ecosystem."""
        packages = GremlinPackageGenerator.PACKAGES[ecosystem]
        # the inner for-loop generates a finite sequence of all valid
        # ecosystem+package combinations, but we need infinite sequence.
        # Thence we use outer infinite loop here
        while True:
            yield from GremlinPackageGenerator.generate_ecosystem_package(ecosystem, packages)

    @staticmethod
    def package_version_generator_for_ecosystem(ecosystem='pypi'):
        """Provide generator for package+version specifications for selected ecosystem."""
        packages = GremlinPackageGenerator.PACKAGES[ecosystem]
        # the inner for-loop generates a finite sequence of all valid
        # ecosystem+package+version combinations, but we need infinite sequence.
        # Thence we use outer infinite loop here
        while True:
            yield from GremlinPackageGenerator.generate_ecosystem_package_version(ecosystem,
                                                                                  packages)


# just a bunch of simple checks, not to be used in the dashboard itself
if __name__ == "__main__":
    gremlin_url = \
        "http://bayesian-gremlin-http-preview-b6ff-bayesian-preview.b6ff.rh-idev.openshiftapps.com"

    g = GremlinPackageGenerator.package_generator()
    for _ in range(10):
        print(next(g))

    print()

    g = GremlinPackageGenerator.package_version_generator()
    for _ in range(10):
        print(next(g))

    print()

    g = GremlinPackageGenerator.package_generator_for_ecosystem("pypi")
    for _ in range(10):
        print(next(g))

    print()

    g = GremlinPackageGenerator.package_version_generator_for_ecosystem("pypi")
    for _ in range(10):
        print(next(g))
