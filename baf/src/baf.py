"""The main module of the Bayesian API Fuzzer."""

from fastlog import log
from cliargs import cli_parser


def main():
    """Entry point to the Bayesian API Fuzzer."""
    log.setLevel(log.INFO)
    log.info("Setup")
    with log.indent():
        cli_arguments = cli_parser.parse_args()
        generate_html = cli_arguments.html
        log.info("HTML generator: " + ("enabled" if generate_html else "disabled"))


if __name__ == "__main__":
    # execute only if run as a script
    main()
