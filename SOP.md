# Standard operating procedures for the Analytics platform

## Issues in end to end tests

## Issues on CI

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
