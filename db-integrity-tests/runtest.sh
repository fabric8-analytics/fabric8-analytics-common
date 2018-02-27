#!/bin/bash -ex

# following environment variables must be set correctly in order for tests to be run
export F8A_GREMLIN_URL=""

export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export S3_REGION_NAME=""
export DEPLOYMENT_PREFIX=""

function prepare_venv() {
	virtualenv -p python3 venv && source venv/bin/activate && python3 `which pip3` install -r requirements.txt
}

[ "$NOVENV" == "1" ] || prepare_venv || exit 1

python3 -B src/main.py $@
