#!/usr/bin/bash -e

#Load configuration from env variables
source env.sh

function generate_and_deploy_config() {
  bash generate-config.sh  # will create config.yaml file
  oc process -p DEPLOYMENT_PREFIX=$OC_PROJECT -p KEYCLOAK_URL=$KEYCLOAK_URL -f ${here}/config-template.yaml > ${here}/config.yaml
  oc apply -f config.yaml
}
function deploy_secrets() {
  oc process -f secrets-template.yaml -p AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -p AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
                                      -p GITHUB_API_TOKENS=$GITHUB_API_TOKENS -p GITHUB_OAUTH_CONSUMER_KEY=$GITHUB_OAUTH_CONSUMER_KEY \
                                      -p GITHUB_OAUTH_CONSUMER_SECRET=$GITHUB_OAUTH_CONSUMER_SECRET -p FLASK_APP_SECRET_KEY=$FLASK_APP_SECRET_KEY \
                                      -p RDS_ENDPOINT=$RDS_ENDPOINT -p RDS_PASSWORD=$RDS_PASSWORD > ${here}/secrets.yaml
  oc apply -f secrets.yaml
}
function oc_process_apply() {
  echo -e "\n Processing template - $1 ($2) \n"
  oc process -f $1 $2 | oc apply -f -
}

function openshift_login() {
  if oc login $OC_URI -u $OC_USERNAME -p $OC_PASSWD | grep -q $OC_PROJECT
  then
    oc project $OC_PROJECT
  else
    oc new-project $OC_PROJECT
  fi
}

here=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
templates_dir="${here}/templates"
templates="fabric8-analytics-jobs fabric8-analytics-server fabric8-analytics-data-model 
           fabric8-analytics-worker fabric8-analytics-pgbouncer fabric8-analytics-recommender 
           gremlin-docker anitya-docker fabric8-analytics-scaler fabric8-analytics-firehose-fetcher
           fabric8-analytics-license-analysis fabric8-analytics-stack-analysis"

openshift_login
generate_and_deploy_config
deploy_secrets

# Get templates for fabric8-analytics projects
for template in ${templates}
do
  curl -sS https://raw.githubusercontent.com/fabric8-analytics/${template}/master/openshift/template.yaml > ${templates_dir}/${template#fabric8-analytics-}.yaml
done

oc_process_apply ${templates_dir}/pgbouncer.yaml
oc_process_apply ${templates_dir}/gremlin-docker.yaml "-p CHANNELIZER=http -p REST_VALUE=1 -p IMAGE_TAG=latest"
oc_process_apply ${templates_dir}/anitya-docker.yaml
oc_process_apply ${templates_dir}/recommender.yaml
oc_process_apply ${templates_dir}/data-model.yaml
oc_process_apply ${templates_dir}/worker.yaml "-p WORKER_ADMINISTRATION_REGION=ingestion -p WORKER_EXCLUDE_QUEUES=GraphImporterTask"
oc_process_apply ${templates_dir}/worker.yaml "-p WORKER_ADMINISTRATION_REGION=ingestion -p WORKER_INCLUDE_QUEUES=GraphImporterTask -p WORKER_NAME_SUFFIX=-graph-import"
oc_process_apply ${templates_dir}/worker.yaml "-p WORKER_ADMINISTRATION_REGION=api -p WORKER_RUN_DB_MIGRATIONS=1 -p WORKER_EXCLUDE_QUEUES=GraphImporterTask"
oc_process_apply ${templates_dir}/worker.yaml "-p WORKER_ADMINISTRATION_REGION=api -p WORKER_INCLUDE_QUEUES=GraphImporterTask -p WORKER_NAME_SUFFIX=-graph-import"
oc_process_apply ${templates_dir}/server.yaml
oc_process_apply ${templates_dir}/jobs.yaml
oc_process_apply ${templates_dir}/scaler.yaml
oc_process_apply ${templates_dir}/firehose-fetcher.yaml
oc_process_apply ${templates_dir}/stack-analysis.yaml "-p KRONOS_SCORING_REGION=maven"
oc_process_apply ${templates_dir}/stack-analysis.yaml "-p KRONOS_SCORING_REGION=pipy"

