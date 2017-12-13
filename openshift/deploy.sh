#!/bin/bash -e
here=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

#Check for configuration file
if ! [ -f $here/env.sh ]
then
    echo 'Please create env.sh based on README.md'
    exit 1
fi

#Load configuration from env variables
source env.sh

#Check for required tools
if ! [ -x "$(command -v aws)" ]; then
    echo 'Error: aws is not installed.' >&2
    exit 1
fi

if ! [ -x "$(command -v awk)" ]; then
    echo 'Error: awk is not installed.' >&2
    exit 1
fi

if ! [ -x "$(command -v psql)" ]; then
    echo 'Error: psql is not installed.' >&2
    exit 1
fi

if ! [ -x "$(command -v oc)" ]; then
    echo 'Error: oc is not installed.' >&2
    exit 1
fi

#Check required env variables
if [ "${RDS_PASSWORD}" == "" ]; then
    echo 'You have to set RDS_PASSWORD'
    exit 1
fi

if [ "${RDS_INSTANCE_NAME}" == "" ]; then
    echo 'You have to set RDS_INSTANCE_NAME'
    exit 1
fi

if [ "${OC_USERNAME}" == "Not set" ]; then
    echo 'You have to set OC_USERNAME'
    exit 1
fi

if [ "${OC_PASSWD}" == "Not set" ]; then
    echo 'You have to set OC_PASSWD'
    exit 1
fi

if [ "${AWS_ACCESS_KEY_ID}" == "Not set" ]; then
    echo 'You have to set AWS_ACCESS_KEY_ID'
    exit 1
fi

if [ "${AWS_SECRET_ACCESS_KEY}" == "Not set" ]; then
    echo 'You have to set AWS_SECRET_ACCESS_KEY'
    exit 1
fi

function generate_and_deploy_config() {
    oc process -p DEPLOYMENT_PREFIX="${DEPLOYMENT_PREFIX}" \
    -p KEYCLOAK_URL="${KEYCLOAK_URL}" \
    -f ${here}/config-template.yaml > ${here}/config.yaml
    oc apply -f config.yaml
}

function deploy_secrets() {
    #All secrets must be base64 encoded
    oc process -f secrets-template.yaml -p AWS_ACCESS_KEY_ID="$(echo -n $AWS_ACCESS_KEY_ID | base64)" \
    -p AWS_SECRET_ACCESS_KEY="$(echo -n $AWS_SECRET_ACCESS_KEY | base64)" \
    -p GITHUB_API_TOKENS="$(echo -n $GITHUB_API_TOKENS | base64)" \
    -p GITHUB_OAUTH_CONSUMER_KEY="$(echo -n $GITHUB_OAUTH_CONSUMER_KEY | base64)" \
    -p GITHUB_OAUTH_CONSUMER_SECRET="$(echo -n $GITHUB_OAUTH_CONSUMER_SECRET | base64)" \
    -p FLASK_APP_SECRET_KEY="$(echo -n $FLASK_APP_SECRET_KEY | base64)" \
    -p RDS_ENDPOINT="$(echo -n $RDS_ENDPOINT | base64)" \
    -p RDS_PASSWORD="$(echo -n $RDS_PASSWORD | base64)" \
    > ${here}/secrets.yaml
    oc apply -f secrets.yaml
}

function oc_process_apply() {
    echo -e "\n Processing template - $1 ($2) \n"
    oc process -f $1 $2 | oc apply -f -
}

function openshift_login() {
    oc login $OC_URI -u $OC_USERNAME -p $OC_PASSWD --insecure-skip-tls-verify=true
    if oc get project ${OC_PROJECT}; then
        oc project ${OC_PROJECT}
        echo "Removing all openshift resources from selected project"
        oc delete all,cm,secrets --all
    else
        oc new-project ${$OC_PROJECT}
    fi
}

function tag_rds_instance() {
    aws rds add-tags-to-resource \
            --resource-name $RDS_ARN\
            --tags "Key=ENV,Value=${DEPLOYMENT_PREFIX}"
}

function get_rds_instance_info() {
    aws --output=table rds describe-db-instances --db-instance-identifier $RDS_INSTANCE_NAME 2>/dev/null
}

function allocate_aws_rds() {
    if ! get_rds_instance_info; then
        aws rds create-db-instance \
        --allocated-storage $RDS_STORAGE \
        --db-instance-identifier $RDS_INSTANCE_NAME \
        --db-instance-class $RDS_INSTANCE_CLASS \
        --db-name $RDS_DBNAME \
        --db-subnet-group-name  "${RDS_SUBNET_GROUP_NAME}" \
        --engine postgres \
        --engine-version "9.6.1" \
        --master-username $RDS_DBADMIN \
        --master-user-password $RDS_PASSWORD \
        --publicly-accessible \
        --storage-type gp2
        #--storage-encrypted
        echo "Waiting (60s) for $RDS_INSTANCE_NAME to come online"
        sleep 60
        wait_for_rds_instance_info
    else
        echo "DB instance $RDS_INSTANCE_NAME already exists, recreating database"
        wait_for_rds_instance_info
        PGPASSWORD=$RDS_PASSWORD psql -d template1 -h $RDS_ENDPOINT -U $RDS_DBADMIN -c "drop database $RDS_DBNAME"
        PGPASSWORD=$RDS_PASSWORD psql -d template1 -h $RDS_ENDPOINT -U $RDS_DBADMIN -c "create database $RDS_DBNAME"
    fi
    tag_rds_instance
}

function wait_for_rds_instance_info() {
    while true; do
        echo "Trying to get RDS DB endpoint for $RDS_INSTANCE_NAME ..."

        export RDS_ENDPOINT=$(get_rds_instance_info | grep -w Address | awk '{print $RDS_DBNAME}' | tr -d '|"' | sed 's/Address//g')
        export RDS_ARN=$(get_rds_instance_info | grep -w DBInstanceArn | awk '{print $4}')

        if [ -z "${RDS_ENDPOINT}" ]; then
            echo "DB is still initializing, waiting 30 seconds and retrying ..."
            sleep 30
        else
            break
        fi
    done
}

templates_dir="${here}/templates"
templates="fabric8-analytics-jobs fabric8-analytics-server fabric8-analytics-data-model
fabric8-analytics-worker fabric8-analytics-pgbouncer gremlin-docker anitya-docker
fabric8-analytics-scaler fabric8-analytics-firehose-fetcher
fabric8-analytics-license-analysis fabric8-analytics-stack-analysis fabric8-analytics-stack-report-ui"

openshift_login
allocate_aws_rds
generate_and_deploy_config
deploy_secrets

#Get templates for fabric8-analytics projects
for template in ${templates}
do
    curl -sS https://raw.githubusercontent.com/fabric8-analytics/${template}/master/openshift/template.yaml > ${templates_dir}/${template#fabric8-analytics-}.yaml
done

oc_process_apply ${templates_dir}/pgbouncer.yaml
oc_process_apply ${templates_dir}/gremlin-docker.yaml "-p CHANNELIZER=http -p REST_VALUE=1 -p IMAGE_TAG=latest"
oc_process_apply ${templates_dir}/anitya-docker.yaml
oc_process_apply ${templates_dir}/data-model.yaml
oc_process_apply ${templates_dir}/worker.yaml "-p WORKER_ADMINISTRATION_REGION=ingestion -p WORKER_EXCLUDE_QUEUES=GraphImporterTask"
oc_process_apply ${templates_dir}/worker.yaml "-p WORKER_ADMINISTRATION_REGION=ingestion -p WORKER_INCLUDE_QUEUES=GraphImporterTask -p WORKER_NAME_SUFFIX=-graph-import"
oc_process_apply ${templates_dir}/worker.yaml "-p WORKER_ADMINISTRATION_REGION=api -p WORKER_RUN_DB_MIGRATIONS=1 -p WORKER_EXCLUDE_QUEUES=GraphImporterTask"
oc_process_apply ${templates_dir}/worker.yaml "-p WORKER_ADMINISTRATION_REGION=api -p WORKER_INCLUDE_QUEUES=GraphImporterTask -p WORKER_NAME_SUFFIX=-graph-import"
oc_process_apply ${templates_dir}/server.yaml
oc_process_apply ${templates_dir}/jobs.yaml "-p AUTH_ORGANIZATION=fabric8-analytics"
oc_process_apply ${templates_dir}/scaler.yaml "-p DC_NAME=bayesian-worker-ingestion -p SQS_QUEUE_NAME=ingestion_bayesianFlow_v0 -p MAX_REPLICAS=8 -p DEFAULT_REPLICAS=2"
oc_process_apply ${templates_dir}/scaler.yaml "-p DC_NAME=bayesian-worker-api -p SQS_QUEUE_NAME=api_bayesianFlow_v0 -p MAX_REPLICAS=4 -p DEFAULT_REPLICAS=2"
oc_process_apply ${templates_dir}/firehose-fetcher.yaml
oc_process_apply ${templates_dir}/stack-analysis.yaml "-p KRONOS_SCORING_REGION=maven"
oc_process_apply ${templates_dir}/stack-analysis.yaml "-p KRONOS_SCORING_REGION=pypi"
oc_process_apply ${templates_dir}/license-analysis.yaml
oc_process_apply ${templates_dir}/stack-report-ui.yaml
