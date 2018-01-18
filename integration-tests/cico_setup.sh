#!/bin/bash -ex


load_jenkins_vars() {
    if [ -e "jenkins-env" ]; then
        cat jenkins-env \
          | grep -E "(F8A_API_URL|RECOMMENDER_API_TOKEN|JENKINS_URL|GIT_BRANCH|GIT_COMMIT|BUILD_NUMBER|ghprbSourceBranch|ghprbActualCommit|BUILD_URL|ghprbPullId)=" \
          | sed 's/^/export /g' \
          > ~/.jenkins-env
        source ~/.jenkins-env
    fi
    echo "Jenkins URL: $JENKINS_URL"
    echo "Build URL: $BUILD_URL"
}

prep() {
    yum -y update
    yum -y install docker git
    systemctl start docker
}

load_jenkins_vars
prep

F8A_API_URL=${F8A_API_URL:-https://recommender.api.prod-preview.openshift.io}
F8A_JOB_API_URL=${F8A_JOB_API_URL:-http://bayesian-jobs-bayesian-preview.b6ff.rh-idev.openshiftapps.com}
F8A_GREMLIN_URL=${F8A_GREMLIN_URL:-http://bayesian-gremlin-http-preview-b6ff-bayesian-preview.b6ff.rh-idev.openshiftapps.com}
F8A_3SCALE_URL=${F8A_3SCALE_URL:-https://3scale-connect.api.prod-preview.openshift.io/}
F8A_BACKBONE_API_URL=${F8A_BACKBONE_API_URL:-http://f8a-server-backbone-bayesian-preview.b6ff.rh-idev.openshiftapps.com/}
F8A_SERVICE_ID=${F8A_SERVICE_ID:-2555417746645}
