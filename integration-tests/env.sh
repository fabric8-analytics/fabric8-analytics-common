#!/usr/bin/env bash

THREE_SCALE_PREVIEW_USER_KEY="not-set"
F8A_API_URL="not-set"
F8A_JOB_API_URL="not-set"
OSIO_AUTH_SERVICE="not-set"
F8A_THREE_SCALE_PREVIEW_URL="not-set"
F8A_SERVICE_ID="not-set"
F8A_GREMLIN_URL="not-set"
F8A_GEMINI_API_URL="not-set"
RECOMMENDER_REFRESH_TOKEN="not-set"

#Optional
AWS_ACCESS_KEY_ID="not-set"
AWS_SECRET_ACCESS_KEY="not-set"
S3_REGION_NAME="not-set"

export TERM=xterm
TERM=${TERM:-xterm}

# set up terminal colors
NORMAL=$(tput sgr0)
RED=$(tput bold && tput setaf 1)
GREEN=$(tput bold && tput setaf 2)
YELLOW=$(tput bold && tput setaf 3)


if [ $AWS_ACCESS_KEY_ID == 'not-set' ]
then
    echo ""
    printf "%sPlease set all Environment Variables before proceeding.%s" "${RED}" "${NORMAL}"
    echo ""
    exit 1
fi

echo AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID >> ~/.profile
echo S3_REGION_NAME=$S3_REGION_NAME >> ~/.profile
echo AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY >> ~/.profile
echo THREE_SCALE_PREVIEW_USER_KEY=$THREE_SCALE_PREVIEW_USER_KEY >> ~/.profile
echo F8A_API_URL=$F8A_API_URL >> ~/.profile
echo F8A_JOB_API_URL=$F8A_JOB_API_URL >> ~/.profile
echo OSIO_AUTH_SERVICE=$OSIO_AUTH_SERVICE >> ~/.profile
echo F8A_THREE_SCALE_PREVIEW_URL=$F8A_THREE_SCALE_PREVIEW_URL >> ~/.profile
echo F8A_SERVICE_ID=$F8A_SERVICE_ID >> ~/.profile
echo F8A_GREMLIN_URL=$F8A_GREMLIN_URL >> ~/.profile
echo F8A_GEMINI_API_URL=$F8A_GEMINI_API_URL >> ~/.profile
echo RECOMMENDER_REFRESH_TOKEN=$RECOMMENDER_REFRESH_TOKEN >> ~/.profile

source ~/.profile

printf "%sSuccesss: Environment Variables set.%s" "${GREEN}" "${NORMAL}"
