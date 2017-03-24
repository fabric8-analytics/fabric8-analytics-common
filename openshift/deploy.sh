#!/usr/bin/bash -e


function oc_process_apply() {
  echo -e "\n Processing template - $1 ($2) \n"
  oc process -f $1 $2 | oc apply -f -
}

HERE=`dirname $0`

templates="anitya-template bayesian-core-template postgresql-extras-template gremlin-server-template data-model-importer-template analytics-template"
noaws_templates="anitya-postgresql-template broker-template postgresql-template"
( [ ! $AWS_NATIVE ] && [ ! $CLOUD_DEPLOY ] ) && templates="$templates $noaws_templates"


if [[ $PTH_ENV ]]; then
  DEPLOYMENT_PREFIX=$PTH_ENV
else
  DEPLOYMENT_PREFIX=$(oc whoami)
fi
S3_BUCKET_FOR_ANALYSES=${DEPLOYMENT_PREFIX}-${S3_BUCKET_FOR_ANALYSES:-bayesian-core-data}
DYNAMODB_PREFIX="${DYNAMODB_PREFIX:-${DEPLOYMENT_PREFIX}}"


for template in $templates
do
  template_file=${HERE}/${template}.yaml

  if [[ "${template}" == "bayesian-core-template" ]]; then
    args="-v DEPLOYMENT_PREFIX=${DEPLOYMENT_PREFIX} \
-v S3_BUCKET_FOR_ANALYSES=${S3_BUCKET_FOR_ANALYSES} \
${BAYESIAN_API_HOSTNAME:+-v BAYESIAN_API_HOSTNAME=${BAYESIAN_API_HOSTNAME}} \
"
  elif [[ "${template}" == "gremlin-server-template" ]]; then
    # gremlin template needs to be processed twice
    args="-v DYNAMODB_PREFIX=${DYNAMODB_PREFIX} -v MEMORY_LIMIT=2048Mi"
    oc_process_apply "$template_file" "$args"
    args="-v DYNAMODB_PREFIX=${DYNAMODB_PREFIX} -v CHANNELIZER=http -v REST_VALUE=1"
  elif [[ "${template}" == "data-model-importer-template" ]]; then
    args="-v S3_BUCKET_FOR_ANALYSES=${S3_BUCKET_FOR_ANALYSES}"
  elif [[ "${template}" == "analytics-template" ]]; then
    args="-v DEPLOYMENT_PREFIX=${DEPLOYMENT_PREFIX}"
  else
    args=""
  fi

  oc_process_apply "$template_file" "$args"
done

