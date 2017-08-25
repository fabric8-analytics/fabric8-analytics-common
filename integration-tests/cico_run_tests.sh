#!/bin/bash

set -ex

F8A_API_URL=${F8A_API_URL:-https://recommender.api.prod-preview.openshift.io}
F8A_JOB_API_URL=${F8A_JOB_API_URL:-http://bayesian-jobs-bayesian-preview.b6ff.rh-idev.openshiftapps.com}
F8A_ANITYA_API_URL=${F8A_ANITYA_API_URL:-not-used}
RECOMMENDER_API_TOKEN=${RECOMMENDER_API_TOKEN:-not-set-in-e2e-tests}

docker build -t f8a-e2e-tests .

docker run -t \
    -e F8A_API_URL=${F8A_API_URL} \
    -e F8A_JOB_API_URL=${F8A_JOB_API_URL} \
    -e F8A_ANITYA_API_URL=${F8A_ANITYA_API_URL} \
    -e RECOMMENDER_API_TOKEN=${RECOMMENDER_API_TOKEN} \
    f8a-e2e-tests --tags=-jobs.requires_auth --no-color $@

