"""Main module with performance tests interface."""

import json
import time
import datetime
import subprocess
import os.path
import sys
import queue
import threading
import pprint
import csv

from coreapi import *
from jobsapi import *
import benchmarks
import graph
from s3interface import *
import measurements
from duration import *

from cliargs import *

SEQUENCED_BENCHMARKS_DEFAULT_COUNT = 30
BREATHE_PAUSE = 5

STACK_ANALYSIS_JOB_NAMES = [
    'recommendation_v2',
    'stack_aggregator_v2',
    'GraphAggregatorTask'
]


def check_environment_variable(env_var_name):
    """Check if the given environment variable exists."""
    print("Checking: {e} environment variable existence".format(
        e=env_var_name))
    if os.environ.get(env_var_name) is None:
        print("Fatal: {e} environment variable has to be specified"
              .format(e=env_var_name))
        sys.exit(1)
    else:
        print("    ok")


def check_environment_variables():
    """Check if all required environment variables exist."""
    environment_variables = [
        "F8A_API_URL",
        "F8A_JOB_API_URL",
        "RECOMMENDER_API_TOKEN",
        "JOB_API_TOKEN",
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "S3_REGION_NAME"]
    for environment_variable in environment_variables:
        check_environment_variable(environment_variable)


def is_system_running(core_api, jobs_api):
    """Check the server and jobs API availability."""
    return (core_api.is_api_running() and
            jobs_api.is_api_running())


def check_system(core_api, jobs_api, s3):
    """Check if all system endpoints are available and that tokens are valid."""
    # try to access system endpoints
    print("Checking: core API and JOBS API endpoints")
    if not is_system_running(core_api, jobs_api):
        print("Fatal: tested system is not available")
        sys.exit(1)
    else:
        print("    ok")

    # check the authorization token for the core API
    print("Checking: authorization token for the core API")
    if core_api.check_auth_token_validity():
        print("    ok")
    else:
        sys.exit(1)

    # check the authorization token for the jobs API
    print("Checking: authorization token for the jobs API")
    if jobs_api.check_auth_token_validity():
        print("    ok")
    else:
        sys.exit(1)

    print("Checking: connection to the S3")
    # try to connect to AWS S3
    s3.connect()
    buckets = s3.read_all_buckets()
    if buckets is not None:
        print("    ok")
    else:
        print("Fatal: can not connect to S3 nor to read the data")
        sys.exit(1)


def run_core_api_sequenced_calls_benchmark(core_api, s3):
    """Start the benchmarks for the core API."""
    print("Core API sequenced calls benchmark")
    run_sequenced_benchmark(core_api, s3,
                            "Core API endpoint",
                            "core_api_sequenced_calls",
                            lambda api, s3, measurement_count, pause_time:
                                benchmarks.core_api_benchmark(api, measurement_count, pause_time),
                            [5, 2, 1.5, 1.0, 0.5, 0.0], 20)


def run_stack_analysis_sequenced_calls_benchmark(core_api, s3):
    """Start the benchmarks for stack analysis."""
    print("Stack analysis sequenced calls benchmark")
    run_sequenced_benchmark(core_api, s3,
                            "Stack analysis API endpoint",
                            "stack_analysis_sequenced_calls",
                            lambda api, s3, measurement_count, pause_time:
                                benchmarks.stack_analysis_benchmark(api, measurement_count,
                                                                    pause_time),
                            [1], SEQUENCED_BENCHMARKS_DEFAULT_COUNT,
                            compute_stack_analysis_jobs_durations=True)


def run_read_component_analysis_sequenced_calls_benchmark(core_api, s3):
    """Start the benchmarks for component analysis (server API)."""
    print("Component analysis sequenced calls benchmark")
    run_sequenced_benchmark(core_api, s3,
                            "Component analysis for known component",
                            "component_analysis_sequenced_calls_known_component",
                            lambda api, s3, measurement_count, pause_time:
                                benchmarks.component_analysis(api, s3,
                                                              measurement_count,
                                                              0, True, None, "pypi",
                                                              "clojure_py", "0.2.4"),
                            [1], SEQUENCED_BENCHMARKS_DEFAULT_COUNT)
    run_sequenced_benchmark(core_api, s3,
                            "Component analysis for unknown component",
                            "component_analysis_sequenced_calls_unknown_component",
                            lambda api, s3, measurement_count, pause_time:
                                benchmarks.component_analysis(api, s3,
                                                              measurement_count,
                                                              0, False, None, "pypi",
                                                              "non_existing_component", "9.8.7"),
                            [1], SEQUENCED_BENCHMARKS_DEFAULT_COUNT)


def run_component_analysis_sequenced_calls_benchmark(jobs_api, s3):
    """Start the benchmarks for component analysis (jobs API)."""
    print("Component analysis sequenced calls benchmark")
    run_sequenced_benchmark(jobs_api, s3,
                            "Component analysis flow scheduling, same component",
                            "component_analysis_flow_scheduling_same_component",
                            lambda api, s3, measurement_count, pause_time:
                                benchmarks.component_analysis_flow_scheduling(api, s3,
                                                                              measurement_count,
                                                                              60, None, "pypi",
                                                                              "clojure_py",
                                                                              "0.2.4"))
    run_sequenced_benchmark(jobs_api, s3,
                            "Component analysis flow scheduling, different components",
                            "component_analysis_flow_scheduling_different_components",
                            lambda api, s3, measurement_count, pause_time:
                                benchmarks.component_analysis_flow_scheduling(api, s3,
                                                                              measurement_count,
                                                                              pause_time))


def run_analysis_concurrent_benchmark(api, s3, message, name_prefix, function_to_call,
                                      thread_counts=None):
    """Universal function to call any callback function in more threads and collect results."""
    thread_counts = thread_counts or [1, 2, 3, 4]
    print(message + " concurrent benchmark")
    measurement_count = 1

    summary_min_times = []
    summary_max_times = []
    summary_avg_times = []

    for thread_count in thread_counts:
        print("Concurrent threads: {c}".format(c=thread_count))
        min_times = []
        max_times = []
        avg_times = []

        threads = []
        q = queue.Queue()

        for thread_id in range(0, thread_count):
            t = threading.Thread(target=lambda api, s3, measurement_count, pause_time, q,
                                 thread_id:
                                 function_to_call(api, s3, measurement_count,
                                                  pause_time, q, thread_id),
                                 args=(api, s3, measurement_count, 0, q, thread_id))
            t.start()
            threads.append(t)

        print("---------------------------------")
        print("Waiting for all threads to finish")
        wait_for_all_threads(threads)
        print("Done")

        values = sum([q.get() for t in threads], [])
        print("values")
        print(len(values))
        print(values)
        print("----")
        title = "{n}, {t} concurrent threads".format(n=message,
                                                     t=thread_count)
        name = "{n}_{t}_threads".format(n=name_prefix, t=thread_count)
        graph.generate_wait_times_graph(title, name, values)

        min_times.append(min(values))
        max_times.append(max(values))
        avg_times.append(sum(values) / len(values))

        print("min_times:", min_times)
        print("max_times:", max_times)
        print("avg_times:", avg_times)

        summary_min_times.append(min(values))
        summary_max_times.append(max(values))
        summary_avg_times.append(sum(values) / len(values))

        generate_statistic_graph(name, thread_count, ["min/avg/max"],
                                 min_times, max_times, avg_times)
        print("Breathe (statistic graph)...")
        time.sleep(BREATHE_PAUSE)

    print(summary_min_times)
    print(summary_max_times)
    print(summary_avg_times)

    t = thread_counts
    graph.generate_timing_threads_statistic_graph("Duration for " + message,
                                                  "{p}".format(p=name_prefix),
                                                  t,
                                                  summary_min_times,
                                                  summary_max_times,
                                                  summary_avg_times)

    with open(name_prefix + ".csv", "w") as csvfile:
        csv_writer = csv.writer(csvfile)
        for i in range(0, len(thread_counts)):
            csv_writer.writerow([i, thread_counts[i],
                                 summary_min_times[i], summary_max_times[i], summary_avg_times[i]])


def run_component_analysis_concurrent_calls_benchmark(jobs_api, s3):
    """Call component analysis in more threads and collect results."""
    print("Component analysis concurrent benchmark")
    measurement_count = 1
    min_thread_count = 1
    max_thread_count = 100

    summary_min_times = []
    summary_max_times = []
    summary_avg_times = []

    for thread_count in range(min_thread_count, 1 + max_thread_count):
        min_times = []
        max_times = []
        avg_times = []

        threads = []
        q = queue.Queue()

        for thread_id in range(0, thread_count):
            t = threading.Thread(target=lambda api, s3, measurement_count, pause_time, q,
                                 thread_id:
                                 benchmarks.component_analysis_thread(api, s3,
                                                                      measurement_count,
                                                                      pause_time, q, thread_id),
                                 args=(jobs_api, s3, measurement_count, 10, q, thread_id))
            t.start()
            threads.append(t)

        print("---------------------------------")
        print("Waiting for all threads to finish")
        wait_for_all_threads(threads)
        print("Done")

        values = sum([q.get() for t in threads], [])
        print("values")
        print(len(values))
        print(values)
        print("----")
        title = "Component analysis, {t} concurrent threads".format(
            t=thread_count)
        name = "jobs_flow_scheduling_{t}_threads".format(t=thread_count)
        graph.generate_wait_times_graph(title, name, values)

        min_times.append(min(values))
        max_times.append(max(values))
        avg_times.append(sum(values) / len(values))

        print("min_times:", min_times)
        print("max_times:", max_times)
        print("avg_times:", avg_times)

        summary_min_times.append(min(values))
        summary_max_times.append(max(values))
        summary_avg_times.append(sum(values) / len(values))

        generate_statistic_graph("component_analysis", thread_count, [10],
                                 min_times, max_times, avg_times)
        print("Breathe (statistic graph)...")
        time.sleep(BREATHE_PAUSE)

    print(summary_min_times)
    print(summary_max_times)
    print(summary_avg_times)
    t = range(min_thread_count, 1 + thread_count)
    graph.generate_timing_threads_statistic_graph("Duration for concurrent analysis",
                                                  "durations_{i}".format(i=thread_count), t,
                                                  summary_min_times,
                                                  summary_max_times,
                                                  summary_avg_times)


def wait_for_all_threads(threads):
    """Wait for all threads from given collection."""
    for t in threads:
        t.join()


def find_job_debug_data(job_name, tasks):
    """Find the stack analysis debug data for given job."""
    for task in tasks:
        if task["task_name"] == job_name:
            return task
    return None


def job_duration(job_name, debug):
    """Compute duration for given job."""
    tasks = debug.json()["tasks"]
    job_debug_data = find_job_debug_data(job_name, tasks)

    assert job_debug_data
    assert job_debug_data["error"] is False

    started_at = job_debug_data["started_at"]
    ended_at = job_debug_data["ended_at"]
    return Duration(started_at, ended_at).duration_seconds


def job_durations(job_name, debug_values):
    """Compute duration for given job and all stack analysis."""
    return [job_duration(job_name, debug_value) for debug_value in debug_values]


def run_sequenced_benchmark(api, s3, title_prefix, name_prefix, function,
                            pauses=None, measurement_count=SEQUENCED_BENCHMARKS_DEFAULT_COUNT,
                            compute_stack_analysis_jobs_durations=False):
    """Start benchmarks by calling selected function sequentially."""
    pauses = pauses or [10]
    print("pauses: {p}".format(p=pauses))
    print("measurement_count: {c}".format(c=measurement_count))

    # for the stack analysis we are able to compute statistic for each job
    if compute_stack_analysis_jobs_durations:
        stack_analysis_jobs_durations = {}
        stack_analysis_jobs_durations_min_times = {}
        stack_analysis_jobs_durations_max_times = {}
        stack_analysis_jobs_durations_avg_times = {}
        for job_name in STACK_ANALYSIS_JOB_NAMES:
            stack_analysis_jobs_durations[job_name] = []
            stack_analysis_jobs_durations_min_times[job_name] = []
            stack_analysis_jobs_durations_max_times[job_name] = []
            stack_analysis_jobs_durations_avg_times[job_name] = []

    measurements = []
    min_times = []
    max_times = []
    avg_times = []

    for pause in pauses:
        if len(pauses) > 1:
            title = "{t}, {s} seconds between calls".format(t=title_prefix, s=pause)
            name = "{n}_{s}_pause_time".format(n=name_prefix, s=pause)
        else:
            title = "{t}".format(t=title_prefix)
            name = "{n}".format(n=name_prefix)
        print("  " + title)
        values, debug = function(api, s3, measurement_count, pause)
        graph.generate_wait_times_graph(title, name, values)
        print("Breathe (statistic graph)...")
        time.sleep(BREATHE_PAUSE)

        min_times.append(min(values))
        max_times.append(max(values))
        avg_times.append(sum(values) / len(values))
        measurements.extend(values)

        if compute_stack_analysis_jobs_durations:
            for job_name in STACK_ANALYSIS_JOB_NAMES:
                durations = job_durations(job_name, debug)
                # all durations for specific jobs need to be stored here
                stack_analysis_jobs_durations[job_name].extend(durations)
                # compute statistic
                cnt = len(durations)
                stack_analysis_jobs_durations_min_times[job_name].append(min(durations))
                stack_analysis_jobs_durations_max_times[job_name].append(max(durations))
                stack_analysis_jobs_durations_avg_times[job_name].append(sum(durations) / cnt)

    print(min_times)
    print(max_times)
    print(avg_times)

    if compute_stack_analysis_jobs_durations:
        print("stack analysis jobs")
        for job_name in STACK_ANALYSIS_JOB_NAMES:
            print("    {j}".format(j=job_name))
            print("        durations: {t}".format(t=stack_analysis_jobs_durations[job_name]))
            print("        min: {t}".format(t=stack_analysis_jobs_durations_min_times[job_name]))
            print("        max: {t}".format(t=stack_analysis_jobs_durations_max_times[job_name]))
            print("        avg: {t}".format(t=stack_analysis_jobs_durations_avg_times[job_name]))

    title = "{t}: min. max. and avg times".format(t=title_prefix)
    min_max_avg_name = "{n}_min_max_avg_times".format(n=name_prefix)
    graph.generate_timing_statistic_graph(title, min_max_avg_name,
                                          pauses, min_times, max_times, avg_times)

    with open(name + ".csv", "w") as csvfile:
        csv_writer = csv.writer(csvfile)
        if compute_stack_analysis_jobs_durations:
            first_row = ["Overall"]
            first_row.extend(STACK_ANALYSIS_JOB_NAMES)
            csv_writer.writerow(first_row)
            for i in range(0, len(measurements)):
                row = []
                row.append(measurements[i])
                s = stack_analysis_jobs_durations
                for job_name in STACK_ANALYSIS_JOB_NAMES:
                    row.append(s[job_name][i])
                csv_writer.writerow(row)
        else:
            for m in measurements:
                csv_writer.writerow([m])


def run_api_concurrent_benchmark(core_api, function_to_call, name_prefix):
    """Call given API endpoint concurrently."""
    measurement_count = 1
    min_thread_count = 1
    max_thread_count = 2
    pauses = [2.0, 1.5, 1.0, 0.5, 0]  # 2, 1, 0.5, 0]
    pauses = [0.0, ]

    summary_min_times = []
    summary_max_times = []
    summary_avg_times = []

    for thread_count in range(min_thread_count, 1 + max_thread_count):
        min_times = []
        max_times = []
        avg_times = []

        for pause in pauses:
            threads = []
            q = queue.Queue()

            for thread_id in range(0, thread_count):
                t = threading.Thread(target=function_to_call,
                                     args=(core_api, measurement_count, pause, q, thread_id))
                t.start()
                threads.append(t)

            wait_for_all_threads(threads)

            values = sum([q.get() for t in threads], [])
            title = "core API endpoint, {t} concurrent threads, {s} seconds between calls".format(
                t=thread_count, s=pause)
            name = "{p}_concurrent_{t}_threads_{s}_pause_time".format(p=name_prefix,
                                                                      t=thread_count,
                                                                      s=pause)
            graph.generate_wait_times_graph(title, name, values)

            min_times.append(min(values))
            max_times.append(max(values))
            avg_times.append(sum(values) / len(values))

            print("Breathe...")
            time.sleep(BREATHE_PAUSE)

        print(min_times)
        print(max_times)
        print(avg_times)

        summary_min_times.append(min(values))
        summary_max_times.append(max(values))
        summary_avg_times.append(sum(values) / len(values))

        generate_statistic_graph(name_prefix, thread_count, pauses,
                                 min_times, max_times, avg_times)
        print("Breathe (statistic graph)...")
        time.sleep(BREATHE_PAUSE)

    print(summary_min_times)
    print(summary_max_times)
    print(summary_avg_times)
    t = range(min_thread_count, 1 + thread_count)
    graph.generate_timing_threads_statistic_graph("Duration for concurrent API calls",
                                                  "{p}_{t}".format(p=name_prefix, t=thread_count),
                                                  t,
                                                  summary_min_times,
                                                  summary_max_times,
                                                  summary_avg_times)


def run_core_api_concurrent_benchmark(core_api):
    """Start the benchmarks for the core API."""
    print("Core API concurrent benchmark")
    run_api_concurrent_benchmark(core_api, benchmarks.core_api_benchmark_thread, "core_api")


def run_benchmarks(core_api, jobs_api, s3, run_stack_analysis, run_component_analysis,
                   run_parallel_tests):
    """Start the selected benchmarks."""
    if run_stack_analysis:
        run_stack_analysis_sequenced_calls_benchmark(core_api, s3)
    if run_component_analysis:
        run_read_component_analysis_sequenced_calls_benchmark(core_api, s3)
    if run_parallel_tests:
        if run_stack_analysis:
            run_analysis_concurrent_benchmark(core_api, s3, "Stack analysis",
                                              "stack_analysis_parallel_calls",
                                              benchmarks.stack_analysis_thread,
                                              [1, 2, 5, 10, 15, 20])
        if run_component_analysis:
            run_analysis_concurrent_benchmark(core_api, s3, "Component analysis known component",
                                              "component_analysis_parallel_calls_known_component",
                                              benchmarks.
                                              component_analysis_read_thread_known_component,
                                              [1, 2, 5, 10, 15, 20])

            run_analysis_concurrent_benchmark(core_api, s3, "Component analysis unknown component",
                                              "component_analysis_parallel_calls_unknown_component",
                                              benchmarks.
                                              component_analysis_read_thread_unknown_component,
                                              [1, 2, 5, 10, 15, 20])


def run_benchmarks_sla(core_api, jobs_api, s3):
    """Run all benchmarks required for SLA."""
    run_read_component_analysis_sequenced_calls_benchmark(core_api, s3)
    run_stack_analysis_sequenced_calls_benchmark(core_api, s3)

    run_analysis_concurrent_benchmark(core_api, s3, "Component analysis known component",
                                      "component_analysis_parallel_calls_known_component",
                                      benchmarks.component_analysis_read_thread_known_component,
                                      range(1, 5))

    run_analysis_concurrent_benchmark(core_api, s3, "Component analysis unknown component",
                                      "component_analysis_parallel_calls_unknown_component",
                                      benchmarks.component_analysis_read_thread_unknown_component,
                                      range(1, 5))

    run_analysis_concurrent_benchmark(core_api, s3, "Stack analysis", "stack_analysis",
                                      "stack_analysis_parallel_calls",
                                      benchmarks.stack_analysis_thread, range(1, 5))


def generate_statistic_graph(name_prefix, thread_count, x_axis_labels, min_times, max_times,
                             avg_times):
    """Generate statistic graph with min, average, and max times."""
    title = "core API endpoint: min, max, and avg times for {t} concurrent threads".format(
        t=thread_count)
    name = "{p}_concurrent_{t}_threads_min_max_avg_times".format(p=name_prefix, t=thread_count)
    graph.generate_timing_statistic_graph(title, name, x_axis_labels,
                                          min_times, max_times, avg_times, 640, 480)


def main():
    """Entry point to the performance tests."""
    cli_arguments = cli_parser.parse_args()
    check_environment_variables()

    coreapi_url = os.environ.get('F8A_API_URL', None)
    jobs_api_url = os.environ.get('F8A_JOB_API_URL', None)

    recommender_api_token = os.environ.get('RECOMMENDER_API_TOKEN')
    job_api_token = os.environ.get('JOB_API_TOKEN')

    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    s3_region_name = os.environ.get('S3_REGION_NAME')
    deployment_prefix = os.environ.get('DEPLOYMENT_PREFIX', 'STAGE')

    core_api = CoreApi(coreapi_url, recommender_api_token)
    jobs_api = JobsApi(jobs_api_url, job_api_token)
    s3 = S3Interface(aws_access_key_id, aws_secret_access_key, s3_region_name, deployment_prefix)

    check_system(core_api, jobs_api, s3)

    if cli_arguments.sla:
        run_benchmarks_sla(core_api, jobs_api, s3)
    else:
        run_benchmarks(core_api, jobs_api, s3,
                       cli_arguments.stack_analysis_benchmark,
                       cli_arguments.component_analysis_benchmark,
                       cli_arguments.parallel)


if __name__ == "__main__":
    # execute only if run as a script
    main()
