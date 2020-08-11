#!/bin/bash -x

./clone_or_pull_all_repos.sh
function prepare_venv() {
	# we want tests to run on python3.6
	printf 'checking alias `python3.6` ... ' >&2
	PYTHON=$(which python3.6 2> /dev/null)
	if [ "$?" -ne "0" ]; then
		printf "${YELLOW} NOT FOUND ${NORMAL}\n" >&2

		printf 'checking alias `python3` ... ' >&2
		PYTHON=$(which python3 2> /dev/null)

		let ec=$?
		[ "$ec" -ne "0" ] && printf "${RED} NOT FOUND ${NORMAL}\n" && return $ec
	fi

	printf "${GREEN} OK ${NORMAL}\n" >&2

	${PYTHON} -m venv "venv" && source venv/bin/activate && pip install -r requirements.txt
	# ${PYTHON} -m venv "venv" && source venv/bin/activate
        #${VIRTUALENV} -p python3 venv && source venv/bin/activate && python3 `which pip3` install pycodestyle
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
#export S3_REGION_NAME="us-east-1"
export AUTH_DOMAIN="go-ready-blockchain.firebaseapp.com"
export DATABASEURL="https://go-ready-blockchain.firebaseio.com"
export STORAGE_BUCKET="go-ready-blockchain.appspot.com"

function run_smoketests()
{
    cwd=`pwd`
    pushd ../integration-tests/
    export F8A_API_URL=$1
    export F8A_JOB_API_URL=$2
    export F8A_ANITYA_API_URL=not_used
    ./runtest.sh --tags=smoketest > $cwd/$3
    echo $? > $cwd/$4
    popd
}

#run_smoketests $F8A_API_URL_STAGE $F8A_JOB_API_URL_STAGE smoketests_stage.log smoketests_stage.results
#run_smoketests $F8A_API_URL_PROD $F8A_JOB_API_URL_PROD smoketests_prod.log smoketests_prod.results

[ "$NOVENV" == "1" ] || prepare_venv || exit 1


python3 -B src/dashboard.py $@
