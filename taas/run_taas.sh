#!/bin/bash -ex

export NOVENV=0
function prepare_venv() {
    virtualenv -p python3 venv && source venv/bin/activate && python3 "$(which pip3)" install -r requirements.txt
}

[ "$NOVENV" == "1" ] || prepare_venv || exit 1

export F8A_API_URL=http://bayesian-api-bayesian-preview.b6ff.rh-idev.openshiftapps.com
export F8A_JOB_API_URL=http://bayesian-jobs-bayesian-preview.b6ff.rh-idev.openshiftapps.com

DIR=$(pwd)
echo $DIR
pushd ../integration-tests/
PYTHONDONTWRITEBYTECODE=1 python3 "${DIR}"/taas.py "${DIR}"/enabled_tests.txt
popd
