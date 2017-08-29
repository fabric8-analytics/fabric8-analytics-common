#!/bin/bash

set -ex

if [ -e "jenkins-env" ]; then
    cat jenkins-env \
      | grep -E "(RECOMMENDER_API_TOKEN|JENKINS_URL|GIT_BRANCH|GIT_COMMIT|BUILD_NUMBER|ghprbSourceBranch|ghprbActualCommit|BUILD_URL|ghprbPullId)=" \
      | sed 's/^/export /g' \
      > ~/.jenkins-env
    source ~/.jenkins-env
fi

F8A_API_URL=${F8A_API_URL:-https://recommender.api.prod-preview.openshift.io}
F8A_JOB_API_URL=${F8A_JOB_API_URL:-http://bayesian-jobs-bayesian-preview.b6ff.rh-idev.openshiftapps.com}
F8A_ANITYA_API_URL=${F8A_ANITYA_API_URL:-not-used}

docker build -t f8a-e2e-tests .

docker run -t \
    -e F8A_API_URL=${F8A_API_URL} \
    -e F8A_JOB_API_URL=${F8A_JOB_API_URL} \
    -e F8A_ANITYA_API_URL=${F8A_ANITYA_API_URL} \
    ${RECOMMENDER_API_TOKEN:+-e RECOMMENDER_API_TOKEN=${RECOMMENDER_API_TOKEN}} \
    f8a-e2e-tests --tags=-jobs.requires_auth --no-color $@

