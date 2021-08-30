#!/bin/bash -ex

export F8A_API_URL=${F8A_API_URL:-https://recommender.api.prod-preview.openshift.io}
export F8A_JOB_API_URL=${F8A_JOB_API_URL:-http://bayesian-jobs-bayesian-preview.b6ff.rh-idev.openshiftapps.com}
export F8A_API_V2_URL=${F8A_API_V2_URL:-https://f8a-analytics-preview-2445582058137.staging.gw.apicast.io}
export F8A_GREMLIN_URL=${F8A_GREMLIN_URL:-http://bayesian-gremlin-http-preview-b6ff-bayesian-preview.b6ff.rh-idev.openshiftapps.com}
export F8A_3SCALE_URL=${F8A_3SCALE_URL:-https://3scale-connect.api.prod-preview.openshift.io/}
export F8A_THREE_SCALE_PREVIEW_URL=${F8A_THREE_SCALE_PREVIEW_URL:-https://f8a-analytics-preview-2445582058137.production.gw.apicast.io}
export F8A_BACKBONE_API_URL=${F8A_BACKBONE_API_URL:-http://f8a-server-backbone-bayesian-preview.b6ff.rh-idev.openshiftapps.com/}
export F8A_SERVICE_ID=${F8A_SERVICE_ID:-2555417755633}
export F8A_GEMINI_API_URL=${F8A_GEMINI_API_URL:-https://gemini.api.prod-preview.openshift.io/}
export F8A_LICENSE_SERVICE_URL=${F8A_LICENSE_SERVICE_URL:-https://license-analysis.api.prod-preview.openshift.io}
export OSIO_AUTH_SERVICE=${OSIO_AUTH_SERVICE:-https://auth.prod-preview.openshift.io}
export MANIFESTS_BUCKET_URL=${MANIFESTS_BUCKET_URL:-https://public-dynamic-manifests.s3.amazonaws.com/}
export THREE_SCALE_PREVIEW_USER_KEY=${THREE_SCALE_PREVIEW_USER_KEY}
export REGISTERED_USER_UUID=${REGISTERED_USER_UUID}
export SNYK_TOKEN=${SNYK_TOKEN}

PYTHONDONTWRITEBYTECODE=1 python3 `which behave` --tags=-skip --tags=-data-sanity --tags=-jobs.requires_auth --tags=-requires.openshift.console.access --no-color -D dump_errors=true @feature_list.txt $@