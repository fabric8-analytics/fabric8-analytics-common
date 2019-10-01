# Standard operating procedures for the Analytics platform

## Issues in end to end tests

### Message "Note: integration tests are running localy via docker-compose"

- it means that some environment variable(s) are not set up properly
- make sure that the `F8A_API_URL` is set
- make sure that the `F8A_JOB_API_URL` is set

### Message "Note: integration tests are running against existing deployment"

- all environment variables, including `F8A_API_URL` are set and e2e tests check the remote APIs

### Message "Note: {e} environment variable is specified, but tests are still run locally"

- some of environment variables `F8A_API_URL`, `F8A_JOB_API_URL` or `F8A_GEMINI_API_URL` is setup, but not all
- it might mean that you need to run end to end tests against remote APIs, but in reality tests are run locally
- make sure that the `F8A_API_URL` is set
- make sure that the `F8A_JOB_API_URL` is set

### Message "Warning: the {name} environment variable is not set. Most tests that require authorization will probably fail"

- make sure the `RECOMMENDER_REFRESH_TOKEN` or `RECOMMENDER_API_TOKEN` is set (but no both)
- make sure the `JOB_API_TOKEN` is set in case you need to run jobs API tests (deprecated right now)



## Issues on CI

### CI jobs failure with message "The requested operation failed as no inventory is available"

Full message looks like this:

```
+ true
++ cico node get -f value -c ip_address -c comment
The requested operation failed as no inventory is available.
+ cico_output=
Build step 'Execute shell' marked build as failure
Setting status of afca674a4bf1d03ba432d62f108541130905954c to FAILURE with url https://ci.centos.org/job/devtools-e2e-fabric8-analytics/1348/ and message: 'Build finished. '
Using context: ci.centos.org PR build (fabric8-analytics)
Finished: FAILURE
```

- this is temporary issue caused by insufficient number of nodes on CI
- rerun the job after some time by adding `[test]` message to the pull request

### CI jobs failure with messages "cico node get' failed, trying again in Ns (x/y)"

Typical error message is repeated several times:

```
'cico node get' failed, trying again in 60s (1/15)
+ n=2
+ sleep 60
+ true
++ cico node get -f value -c ip_address -c comment
The requested operation failed as no inventory is available.
```

- this is temporary issue caused by insufficient number of nodes on CI
- rerun the job after some time by adding `[test]` message to the pull request