#!/bin/bash -ex

AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
S3_REGION_NAME=""
THREE_SCALE_PREVIEW_USER_KEY=""
F8A_API_URL=""
F8A_JOB_API_URL=""
OSIO_AUTH_SERVICE=""
F8A_THREE_SCALE_PREVIEW_URL=""
F8A_SERVICE_ID=""
F8A_GREMLIN_URL=""
F8A_GEMINI_API_URL=""
RECOMMENDER_REFRESH_TOKEN=""

if [ ! -f /var/run/docker.pid ]
then
    echo "!!! Docker service is probably not running !!!"
fi

function prepare_venv() {
	virtualenv -p python3 venv && source venv/bin/activate && python3 `which pip3` install -r requirements.txt
}

[ "$NOVENV" == "1" ] || prepare_venv || exit 1

export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
export S3_REGION_NAME=$S3_REGION_NAME
export THREE_SCALE_PREVIEW_USER_KEY=$THREE_SCALE_PREVIEW_USER_KEY
export F8A_API_URL=$F8A_API_URL
export F8A_JOB_API_URL=$F8A_JOB_API_URL
export OSIO_AUTH_SERVICE=$OSIO_AUTH_SERVICE
export F8A_THREE_SCALE_PREVIEW_URL=$F8A_THREE_SCALE_PREVIEW_URL
export F8A_SERVICE_ID=$F8A_SERVICE_ID
export F8A_GREMLIN_URL=$F8A_GREMLIN_URL
export F8A_GEMINI_API_URL=$F8A_GEMINI_API_URL
export RECOMMENDER_REFRESH_TOKEN=$RECOMMENDER_REFRESH_TOKEN

echo "Success: Environment Variables set"

PYTHONDONTWRITEBYTECODE=1 python3.4 `which behave` --tags=-skip --tags=-data-sanity -D dump_errors=true @feature_list.txt $@
