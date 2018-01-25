### Description
These scripts help perform a load test. There are two ways in which a load is fired.

#### Invoking the load test
1. Use of [future-requests](https://pypi.python.org/pypi/requests-futures/0.9.0) to simulate almost simultaneous workload
    - Usage
        ```
        ./run_load_test.py <concurrent request count> <API URL>
        ```

2. Use of [locust](http://locust.io) framework to generate the load
    - Usage
        ```
        locust -f locust-test.py --host=<HOST URL>
        ```
        Invoke the load test from http://localhost:8089


#### Monitoring the load test
`monitor_load_test.sh` script monitors the database entry that gets created as part of the load test
- Usage
    ```
        ./monitor_load_test.sh <2 * concurrent request count>

    * Caution
    Do not run the monitor script against Staging or Production as it truncates the tables once the tests are performed.
    ```
