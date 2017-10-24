import json
import time
import datetime
import subprocess
import os.path
import sys
import queue
import threading

from coreapi import *
from jobsapi import *
import benchmarks
import graph
from s3interface import *

from cliargs import *


def check_environment_variable(env_var_name):
    print("Checking: {e} environment variable existence".format(
        e=env_var_name))
    if os.environ.get(env_var_name) is None:
        print("Fatal: {e} environment variable has to be specified"
              .format(e=env_var_name))
        sys.exit(1)
    else:
        print("    ok")


def check_environment_variables():
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
    return core_api.is_api_running() and \
           jobs_api.is_api_running()


def check_system(core_api, jobs_api, s3):
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
    print("Core API sequenced calls benchmark")
    run_sequenced_benchmark(core_api, s3,
                            "Core API endpoint",
                            "core_api_sequenced_calls",
                            lambda api, s3, measurement_count, pause_time:
                                benchmarks.core_api_benchmark(api, measurement_count, pause_time))


def run_component_analysis_sequenced_calls_benchmark(jobs_api, s3):
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


def run_component_analysis_concurrent_calls_benchmark(jobs_api, s3):
    print("Component analysis concurrent benchmark")
    measurement_count = 1
    min_thread_count = 2
    max_thread_count = 5

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
        title = "Component analysis, {t} concurrent threads".format(
            t=thread_count)
        name = "jobs_flow_scheduling_{t}_threads".format(t=thread_count)
        graph.generate_wait_times_graph(title, name, values)

        min_times.append(min(values))
        max_times.append(max(values))
        avg_times.append(sum(values) / len(values))

        print(min_times)
        print(max_times)
        print(avg_times)
        generate_statistic_graph(thread_count, [10], min_times, max_times, avg_times)
        print("Breathe (statistic graph)...")
        time.sleep(20)


def wait_for_all_threads(threads):
    for t in threads:
        t.join()


def run_sequenced_benchmark(api, s3, title_prefix, name_prefix, function,
                            pauses=[10], measurement_count=10):

    min_times = []
    max_times = []
    avg_times = []

    for pause in pauses:
        title = "{t}, {s} seconds between calls".format(t=title_prefix, s=pause)
        print("  " + title)
        name = "{n}_{s}_pause_time".format(n=name_prefix, s=pause)
        values = function(api, s3, measurement_count, pause)
        graph.generate_wait_times_graph(title, name, values)
        time.sleep(30)

        min_times.append(min(values))
        max_times.append(max(values))
        avg_times.append(sum(values) / len(values))

    print(min_times)
    print(max_times)
    print(avg_times)
    title = "{t}: min. max. and avg times".format(t=title_prefix)
    name = "{n}_min_max_avg_times".format(n=name_prefix)
    graph.generate_timing_statistic_graph(title, name,
                                          pauses, min_times, max_times, avg_times)
    pass


def run_concurrent_benchmark(core_api, function_to_call):
    measurement_count = 10
    min_thread_count = 5
    max_thread_count = 10
    pauses = [2.0, 1.5, 1.0, 0.5, 0]  # 2, 1, 0.5, 0]
    pauses = [2, 0.5, 0, ]

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
            name = "core_api_concurrent_{t}_threads_{s}_pause_time".format(t=thread_count, s=pause)
            graph.generate_wait_times_graph(title, name, values)

            min_times.append(min(values))
            max_times.append(max(values))
            avg_times.append(sum(values) / len(values))

            print("Breathe...")
            time.sleep(20)

        print(min_times)
        print(max_times)
        print(avg_times)
        generate_statistic_graph(thread_count, pauses, min_times, max_times, avg_times)
        print("Breathe (statistic graph)...")
        time.sleep(20)


def run_core_api_concurrent_benchmark(core_api):
    print("Core API concurrent benchmark")
    run_concurrent_benchmark(core_api, benchmarks.core_api_benchmark_thread)


def run_benchmarks(core_api, jobs_api, s3):
    run_core_api_sequenced_calls_benchmark(core_api, s3)
    run_core_api_concurrent_benchmark(core_api)
    run_component_analysis_sequenced_calls_benchmark(jobs_api, s3)
    run_component_analysis_concurrent_calls_benchmark(jobs_api, s3)


def generate_statistic_graph(thread_count, pauses, min_times, max_times, avg_times):
    title = "core API endpoint: min, max, and avg times for {t} concurrent threads".format(
        t=thread_count)
    name = "core_api_concurrent_{t}_threads_min_max_avg_times".format(t=thread_count)
    graph.generate_timing_statistic_graph(title, name, pauses, min_times, max_times, avg_times)
    pass


def main():
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

    run_benchmarks(core_api, jobs_api, s3)


if __name__ == "__main__":
    # execute only if run as a script
    main()
