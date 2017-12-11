#!/bin/bash

set -ex

. cico_setup.sh

docker build -t f8a-e2e-tests .

docker run -t \
    -e F8A_API_URL=${F8A_API_URL} \
    -e F8A_JOB_API_URL=${F8A_JOB_API_URL} \
    -e F8A_ANITYA_API_URL=${F8A_ANITYA_API_URL} \
    -e F8A_GREMLIN_URL=${F8A_GREMLIN_URL} \
    -e F8A_3SCALE_URL=${F8A_3SCALE_URL} \
    ${RECOMMENDER_API_TOKEN:+-e RECOMMENDER_API_TOKEN=${RECOMMENDER_API_TOKEN}} \
    f8a-e2e-tests --tags=-jobs.requires_auth --no-color $@

