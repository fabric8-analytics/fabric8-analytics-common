#!/bin/bash -ex

function prepare_venv() {
	virtualenv -p python3 venv && source venv/bin/activate && python3 `which pip3` install -r requirements.txt
}

[ "$NOVENV" == "1" ] || prepare_venv || exit 1

define_args="-D dump_errors=true \
${BAYESIAN_API_SERVICE_HOST:+-D coreapi_host=${BAYESIAN_API_SERVICE_HOST}} \
${BAYESIAN_API_SERVICE_PORT:+-D coreapi_port=${BAYESIAN_API_SERVICE_PORT}} \
${BAYESIAN_ANITYA_SERVICE_HOST:+-D anitya_host=${BAYESIAN_ANITYA_SERVICE_HOST}} \
${BAYESIAN_ANITYA_SERVICE_PORT:+-D anitya_port=${BAYESIAN_ANITYA_SERVICE_PORT}}"

PYTHONDONTWRITEBYTECODE=1 python3 `which behave` --tags=-skip $define_args @feature_list.txt $@
