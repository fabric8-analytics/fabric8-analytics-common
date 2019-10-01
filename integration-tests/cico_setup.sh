#!/bin/bash -ex


load_jenkins_vars() {
    if [ -e "jenkins-env" ]; then
        cat jenkins-env \
          | grep -E "(F8A_API_URL|OSIO_AUTH_SERVICE|F8A_JOB_API_URL|F8A_GREMLIN_URL|F8A_THREE_SCALE_PREVIEW_URL|F8A_3SCALE_URL|F8A_BACKBONE_API_URL|F8A_SERVICE_ID|F8A_GEMINI_API_URL|F8A_LICENSE_SERVICE_URL|RECOMMENDER_API_TOKEN|RECOMMENDER_REFRESH_TOKEN|THREE_SCALE_PREVIEW_USER_KEY|JENKINS_URL|GIT_BRANCH|GIT_COMMIT|BUILD_NUMBER|ghprbSourceBranch|ghprbActualCommit|BUILD_URL|ghprbPullId)=" \
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
F8A_THREE_SCALE_PREVIEW_URL=${F8A_THREE_SCALE_PREVIEW_URL:-https://f8a-analytics-preview-2445582058137.production.gw.apicast.io}
F8A_BACKBONE_API_URL=${F8A_BACKBONE_API_URL:-http://f8a-server-backbone-bayesian-preview.b6ff.rh-idev.openshiftapps.com/}
F8A_SERVICE_ID=${F8A_SERVICE_ID:-2555417755633}
F8A_GEMINI_API_URL=${F8A_GEMINI_API_URL:-https://gemini.api.prod-preview.openshift.io/}
F8A_LICENSE_SERVICE_URL=${F8A_LICENSE_SERVICE_URL:-https://license-analysis.api.prod-preview.openshift.io}
OSIO_AUTH_SERVICE=${OSIO_AUTH_SERVICE:-https://auth.prod-preview.openshift.io}
MANIFESTS_BUCKET_URL=${MANIFESTS_BUCKET_URL:-https://public-dynamic-manifests.s3.amazonaws.com/}
