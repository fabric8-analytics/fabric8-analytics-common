#!/bin/bash -ex

function prepare_venv() {
	virtualenv -p python3 venv && source venv/bin/activate && python3 `which pip3` install -r requirements.txt
}

export F8A_API_URL_STAGE=https://recommender.api.prod-preview.openshift.io
export F8A_API_URL_PROD=https://recommender.api.openshift.io

export F8A_SERVER_API_URL=$F8A_API_URL_STAGE

export OSIO_AUTH_SERVICE=https://auth.prod-preview.openshift.io

export RECOMMENDER_REFRESH_TOKEN="please fill in"

[ "$NOVENV" == "1" ] || prepare_venv || exit 1

python3 -B src/a2t.py "$@"
