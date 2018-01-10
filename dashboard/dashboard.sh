#!/bin/bash -x

function prepare_venv() {
	virtualenv -p python3 venv && source venv/bin/activate && python3 `which pip3` install -r requirements.txt
}

export F8A_API_URL_STAGE=http://bayesian-api-bayesian-preview.b6ff.rh-idev.openshiftapps.com
export F8A_API_URL_PROD=https://recommender.api.openshift.io

export F8A_JOB_API_URL_STAGE=http://bayesian-jobs-bayesian-preview.b6ff.rh-idev.openshiftapps.com
export F8A_JOB_API_URL_PROD=http://bayesian-jobs-bayesian-production.09b5.dsaas.openshiftapps.com

#export RECOMMENDER_API_TOKEN_STAGE=""
#export RECOMMENDER_API_TOKEN_PROD=""

#export JOB_API_TOKEN_STAGE=""
#export JOB_API_TOKEN_PROD=""

#export AWS_ACCESS_KEY_ID=""
#export AWS_SECRET_ACCESS_KEY=""
export S3_REGION_NAME="us-east-1"

function run_smoketests()
{
    cwd=`pwd`
    pushd ../integration-tests/
    export F8A_API_URL=$1
    export F8A_JOB_API_URL=$2
    ./runtest.sh --tags=smoketest > $cwd/$3
    echo $? > $cwd/$4
    popd
}

run_smoketests $F8A_API_URL_STAGE $F8A_JOB_API_URL_STAGE smoketests_stage.log smotests_stage.results
run_smoketests $F8A_API_URL_PROD $F8A_JOB_API_URL_PROD smoketests_prod.log smotests_prod.results

[ "$NOVENV" == "1" ] || prepare_venv || exit 1

python3 -B src/dashboard.py $@
