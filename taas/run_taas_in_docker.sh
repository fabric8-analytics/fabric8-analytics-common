#!/bin/bash -ex

export F8A_API_URL=http://bayesian-api-bayesian-preview.b6ff.rh-idev.openshiftapps.com
export F8A_JOB_API_URL=http://bayesian-jobs-bayesian-preview.b6ff.rh-idev.openshiftapps.com

DIR=$(pwd)
echo $DIR
pushd ../integration-tests/
PYTHONDONTWRITEBYTECODE=1 python3 "${DIR}"/taas.py "${DIR}"/enabled_tests.txt
popd
