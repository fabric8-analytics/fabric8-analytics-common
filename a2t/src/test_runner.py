"""Implementation of benchmarks.

Copyright (c) 2019 Red Hat Inc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys

from random import randint
from fastlog import log
from time import time
from queue import Queue
from threading import Thread

from report_generator import generate_csv_report
from component_generator import ComponentGenerator
from setup import parse_tags


# directory containing test results
RESULT_DIRECTORY = "test_results"


def check_number_of_results(queue_size, component_analysis_count, stack_analysis_count):
    """Check if we really got the same number of results as expected.

    When the server respond by any HTTP error code (4xx, 5xx), the results
    are NOT stored in the queue. This means that number of results stored
    in the queue might be less than number of threads set up by user via
    CLI parameters in certain situations. This function check this situation.
    """
    log.info("queue size: {size}".format(size=queue_size))

    expected = component_analysis_count + 2 * stack_analysis_count
    if queue_size != expected:
        log.warning("Warning: {expected} results expected, but only {got} is presented".format(
            expected=expected, got=queue_size))
        log.warning("This means that {n} analysis ends with error or exception".format(
            n=expected - queue_size))


def prepare_component_generators(python_payload, maven_payload, npm_payload):
    """Prepare all required component generators for selected payload types."""
    component_generator = ComponentGenerator()
    g_python = component_generator.generator_for_ecosystem("pypi")
    g_maven = component_generator.generator_for_ecosystem("maven")
    g_npm = component_generator.generator_for_ecosystem("npm")
    generators = []

    if python_payload:
        generators.append(g_python)
    if maven_payload:
        generators.append(g_maven)
    if npm_payload:
        generators.append(g_npm)

    return generators


def initialize_generators(generators):
    """Initialize the generators randomly so we don't start from the 1st item."""
    for i in range(randint(10, 100)):
        for g in generators:
            next(g)


def component_analysis_benchmark(queue, threads, component_analysis, thread_count,
                                 python_payload, maven_payload, npm_payload):
    """Component analysis benchmark."""
    generators = prepare_component_generators(python_payload, maven_payload, npm_payload)

    initialize_generators(generators)

    for t in range(thread_count):
        g = generators[randint(0, len(generators) - 1)]
        ecosystem, component, version = next(g)
        with log.indent():
            log.info("Component analysis for E/P/V {} {} {}".format(ecosystem, component, version))
        t = Thread(target=component_analysis.start,
                   args=(t, ecosystem, component, version, queue))
        t.start()
        threads.append(t)
        # skip some items
        for i in range(randint(5, 25)):
            next(g)


def stack_analysis_benchmark(queue, threads, stack_analysis, thread_count,
                             python_payload, maven_payload, npm_payload):
    """Stack analysis benchmark."""
    # TODO: read automagically from the filelist
    manifests = (
        ("maven", "clojure_1_6_0.xml"),
        ("maven", "clojure_1_7_0.xml"),
        ("maven", "clojure_1_8_0.xml"),
        ("maven", "clojure_junit.xml"),
        ("pypi", "click_6_star.txt"),
        ("pypi", "array_split.txt"),
        ("pypi", "fastlog_urllib_requests.txt"),
        ("pypi", "requests_latest.txt"),
        ("pypi", "numpy_latest.txt"),
        ("pypi", "flask_latest.txt"),
        ("pypi", "scipy_latest.txt"),
        ("pypi", "pygame_latest.txt"),
        ("pypi", "pyglet_latest.txt"),
        ("pypi", "dash_latest.txt"),
        ("pypi", "pudb_latest.txt"),
        ("pypi", "pytest_latest.txt"),
        ("pypi", "numpy_1_11_0.txt"),
        ("pypi", "numpy_1_12_0.txt"),
        ("pypi", "numpy_1_16_2.txt"),
        ("pypi", "numpy_1_16_3.txt"),
        ("pypi", "numpy_scipy.txt"),
        ("pypi", "pytest_2_0_0.txt"),
        ("pypi", "pytest_2_0_1.txt"),
        ("pypi", "pytest_3_2_2.txt"),
        ("pypi", "requests_2_20_0.txt"),
        ("pypi", "requests_2_20_1.txt"),
        ("pypi", "requests_2_21_0.txt"),
        ("pypi", "scipy_1_1_0.txt"),
        ("pypi", "scipy_1_2_0.txt"),
        ("pypi", "scipy_1_2_1.txt"),
        ("npm", "array.json"),
        ("npm", "dependency_array.json"),
        ("npm", "dependency_emitter_component.json"),
        ("npm", "dependency_jquery.json"),
        ("npm", "dependency_jquery_react.json"),
        ("npm", "dependency_lodash.json"),
        ("npm", "dependency_lodash_react_jquery.json"),
        ("npm", "dependency_react.json"),
        ("npm", "dependency_to_function.json"),
        ("npm", "dependency_to_function_vue_array.json"),
        ("npm", "dependency_underscore.json"),
        ("npm", "dependency_underscore_react_jquery.json"),
        ("npm", "dependency_vue.json"),
        ("npm", "dependency_vue_to_function.json"),
        ("npm", "empty.json"),
        ("npm", "jquery.json"),
        ("npm", "lodash.json"),
        ("npm", "mocha.json"),
        ("npm", "no_requirements.json"),
        ("npm", "underscore.json"),
        ("npm", "wisp.json"),
    )

    for t in range(thread_count):
        manifest_idx = randint(0, len(manifests) - 1)
        manifest = manifests[manifest_idx]

        with log.indent():
            log.info("Stack analysis")
        ecosystem = manifest[0]
        manifest_file = manifest[1]
        t = Thread(target=stack_analysis.start,
                   args=(t, ecosystem, manifest_file, queue))
        t.start()
        threads.append(t)


def wait_for_all_threads(threads):
    """Wait for all threads to finish."""
    log.info("Waiting for all threads to finish")
    for t in threads:
        t.join()
    log.success("Done")


def run_test(cfg, test, i, component_analysis, stack_analysis):
    """Run one selected test."""
    test_name = test["Name"]
    log.info("Starting test #{n} with name '{desc}'".format(n=i, desc=test_name))
    with log.indent():
        start = time()

        threads = []
        queue = Queue()

        with log.indent():
            component_analysis_count = int(test["Component analysis"])
            stack_analysis_count = int(test["Stack analysis"])
            python_payload = test["Python payload"] in ("Yes", "yes")
            maven_payload = test["Maven payload"] in ("Yes", "yes")
            npm_payload = test["NPM payload"] in ("Yes", "yes")

            component_analysis_benchmark(queue, threads, component_analysis,
                                         component_analysis_count,
                                         python_payload, maven_payload, npm_payload)
            stack_analysis_benchmark(queue, threads, stack_analysis,
                                     stack_analysis_count,
                                     python_payload, maven_payload, npm_payload)

        wait_for_all_threads(threads)
        queue_size = queue.qsize()
        check_number_of_results(queue_size, component_analysis_count, stack_analysis_count)

        end = time()
        # TODO: use better approach to join paths
        filename = RESULT_DIRECTORY + "/" + test_name.replace(" ", "_") + ".csv"
        log.info("Generating test report into file '{filename}'".format(filename=filename))
        generate_csv_report(queue, test, start, end, end - start, filename)


def run_all_loaded_tests(cfg, tests, component_analysis, stack_analysis):
    """Run all tests read from CSV file."""
    i = 1
    for test in tests:
        run_test(cfg, test, i, component_analysis, stack_analysis)
        i += 1


def run_tests_with_tags(cfg, tests, tags, component_analysis, stack_analysis):
    """Run tests read from CSV file that are marged by any of tags provided in tags parameter."""
    i = 1
    for test in tests:
        test_tags = parse_tags(test["Tags"])
        test_name = test["Name"]
        if tags <= test_tags:
            run_test(cfg, test, i, component_analysis, stack_analysis)
            i += 1
        else:
            log.info("Skipping test #{n} with name '{desc}'".format(n=i, desc=test_name))


def no_tests(tests):
    """Predicate for number of tests."""
    return not tests or len(tests) == 0


def start_tests(cfg, tests, tags, component_analysis, stack_analysis):
    """Start all tests using the already loaded configuration."""
    log.info("Run tests")
    with log.indent():
        if no_tests(tests):
            log.error("No tests loaded!")
            sys.exit(-1)
        if len(tests) == 1:
            log.success("Loaded 1 test")
        else:
            log.success("Loaded {n} tests".format(n=len(tests)))
        if not tags:
            run_all_loaded_tests(cfg, tests, component_analysis, stack_analysis)
        else:
            run_tests_with_tags(cfg, tests, tags, component_analysis, stack_analysis)
