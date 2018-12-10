#!/bin/bash -ex

function prepare_venv() {
	virtualenv -p python3 venv && source venv/bin/activate && python3 `which pip3` install -r requirements.txt
}

export F8A_API_URL_STAGE=http://bayesian-api-bayesian-preview.b6ff.rh-idev.openshiftapps.com
export F8A_API_URL_PROD=https://recommender.api.openshift.io

export F8A_JOB_API_URL_STAGE=http://bayesian-jobs-bayesian-preview.b6ff.rh-idev.openshiftapps.com
export F8A_JOB_API_URL_PROD=http://bayesian-jobs-bayesian-production.09b5.dsaas.openshiftapps.com

[ "$NOVENV" == "1" ] || prepare_venv || exit 1

python3 -B src/baf.py $@
