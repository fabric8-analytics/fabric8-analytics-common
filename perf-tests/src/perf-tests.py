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


def check_system(core_api, jobs_api):
    print("Checking: core API and JOBS API endpoints")
    if not is_system_running(core_api, jobs_api):
        print("Fatal: tested system is not available")
        sys.exit(1)
    else:
        print("    ok")


def run_core_api_sequenced_calls_benchmark(core_api):
    print("Core API sequenced calls benchmark")
    run_sequenced_benchmark(core_api,
                            "Core API endpoint",
                            "core_api_sequenced_calls",
                            lambda api, measurement_count, pause_time:
                                benchmarks.core_api_benchmark(api, measurement_count, pause_time))


def wait_for_all_threads(threads):
        for t in threads:
            t.join()


def run_sequenced_benchmark(core_api, title_prefix, name_prefix, function):
    pauses = [1, 0.5, 0]
    # pauses = [10, 5, 1, 0.5, 0]

    min_times = []
    max_times = []
    avg_times = []

    for pause in pauses:
        title = "{t}, {s} seconds between calls".format(t=title_prefix, s=pause)
        print("  " + title)
        name = "{n}_{s}_pause_time".format(n=name_prefix, s=pause)
        values = function(core_api, 1, pause)
        graph.generate_wait_times_graph(title, name, values)
        time.sleep(10)

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


def run_benchmarks(core_api, jobs_api):
    run_core_api_sequenced_calls_benchmark(core_api)
    run_core_api_concurrent_benchmark(core_api)


def generate_statistic_graph(thread_count, pauses, min_times, max_times, avg_times):
    title = "core API endpoint: min, max, and avg times for {t} concurrent threads".format(
        t=thread_count)
    name = "core_api_concurrent_{t}_threads_min_max_avg_times".format(t=thread_count)
    graph.generate_timing_statistic_graph(title, name, pauses, min_times, max_times, avg_times)
    pass


def main():
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

    check_system(core_api, jobs_api)


    run_benchmarks(core_api, jobs_api)
    pass


if __name__ == "__main__":
    # execute only if run as a script
    main()
