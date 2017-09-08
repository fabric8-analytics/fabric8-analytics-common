import time


def measure(function_to_call, check_function, measurement_count, pause_time, thread_id, s3=None):
    measurements = []
    for i in range(measurement_count):
        t1 = time.clock()
        if s3 is None:
            retval = function_to_call(i)
        else:
            retval = function_to_call(i, s3)

        print("Return value: ", retval)
        assert check_function(retval)
        t2 = time.clock()
        delta = t2 - t1
        if thread_id is not None:
            print("    thread: #{t}    call {i}/{m}    {delta}".format(t=thread_id,
                                                                       i=i + 1,
                                                                       delta=delta,
                                                                       m=measurement_count))
        else:
            print("    #{i}    {delta}".format(i=i + 1, delta=delta))
        measurements.append(delta)
        time.sleep(pause_time)
    return measurements


def core_api_benchmark(core_api, measurement_count, pause_time, thread_id=None):
    return measure(lambda i: core_api.get(),
                   lambda retval: retval.status_code == 200, measurement_count, pause_time,
                   thread_id)


def jobs_api_benchmark(jobs_api, measurement_count, pause_time, thread_id=None):
    return measure(lambda i: jobs_api.get(),
                   lambda retval: retval.status_code == 200, measurement_count, pause_time,
                   thread_id)


def stack_analysis_benchmark(core_api, measurement_count, pause_time, thread_id=None):
    return measure(lambda i: core_api.stack_analysis(),
                   lambda retval: retval.status_code == 200, measurement_count, pause_time,
                   thread_id)


def core_api_benchmark_thread(core_api, measurement_count, pause_time, q, thread_id):
    measurements = core_api_benchmark(core_api, measurement_count, pause_time, thread_id)
    q.put(measurements)
