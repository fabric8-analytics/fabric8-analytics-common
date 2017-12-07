#!/bin/bash -e

here=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

#Load configuration from env variables
source env.sh

export F8A_API_URL="http://$(oc get route bayesian-api | awk '{print$2}' | grep -w "${OC_USERNAME}")"
export F8A_JOB_API_URL="http://$(oc get route bayesian-jobs | awk '{print$2}' | grep -w "${OC_USERNAME}")"
export F8A_ANITYA_API_URL="http://$(oc get route bayesian-api | awk '{print$2}' | grep -w "${OC_USERNAME}")"

#check for configuration
if [ "${F8A_API_URL}" == "Not set" ]; then
    echo 'You have to set F8A_API_URL'
    exit 1
fi

if [ "${F8A_JOB_API_URL}" == "Not set" ]; then
    echo 'You have to set F8A_JOB_API_URL'
    exit 1
fi

if [ "${F8A_ANITYA_API_URL}" == "Not set" ]; then
    echo 'You have to set F8A_ANITYA_API_URL'
    exit 1
fi

if [ "${RECOMMENDER_API_TOKEN}" == "Not set" ]; then
    echo 'You have to set RECOMMENDER_API_TOKEN'
    exit 1
fi

#run the tests
cd $here/../integration-tests/
./runtest.sh
cd $here
