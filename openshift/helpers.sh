
function is_set_or_fail() {
    local name=$1
    local value=$2

    if [ ! -v value ] || [ "${value}" == "not-set" ]; then
        echo "You have to set $name" >&2
        exit 1
    fi
}

function tool_is_installed() {
# Check if given command is available on this machine
    local cmd=$1

    if ! [ -x "$(command -v $cmd)" ]; then
        echo "Error: ${cmd} command is not available. Please install it. See README.md file for more information." >&2
        exit 1
    fi
}

function generate_and_deploy_config() {
    oc process -p DEPLOYMENT_PREFIX="${DEPLOYMENT_PREFIX}" \
    -p KEYCLOAK_URL="${KEYCLOAK_URL}" \
    -p AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" \
    -f "${here}/config-template.yaml" > "${here}/config.yaml"
    oc apply -f config.yaml
}

function deploy_secrets() {
    #All secrets must be base64 encoded
    oc process -p AWS_ACCESS_KEY_ID="$(echo -n "${AWS_ACCESS_KEY_ID}" | base64)" \
    -p AWS_SECRET_ACCESS_KEY="$(echo -n "${AWS_SECRET_ACCESS_KEY}" | base64)" \
    -p GITHUB_API_TOKENS="$(echo -n "${GITHUB_API_TOKENS}" | base64)" \
    -p GITHUB_OAUTH_CONSUMER_KEY="$(echo -n "${GITHUB_OAUTH_CONSUMER_KEY}" | base64)" \
    -p GITHUB_OAUTH_CONSUMER_SECRET="$(echo -n "${GITHUB_OAUTH_CONSUMER_SECRET}" | base64)" \
    -p FLASK_APP_SECRET_KEY="$(echo -n "${FLASK_APP_SECRET_KEY}" | base64)" \
    -p RDS_ENDPOINT="$(echo -n "${RDS_ENDPOINT}" | base64)" \
    -p RDS_PASSWORD="$(echo -n "${RDS_PASSWORD}" | base64)" \
    -f "${here}/secrets-template.yaml" > "${here}/secrets.yaml"
    oc apply -f secrets.yaml
}

function oc_process_apply() {
    echo -e "\\n Processing template - $1 ($2) \\n"
    # Don't quote $2 as we need it to split into individual arguments
    oc process -f "$1" $2 | oc apply -f -
}

function openshift_login() {
    oc login "${OC_URI}" -u "${OC_USERNAME}" -p "${OC_PASSWD}" --insecure-skip-tls-verify=true
}

function purge_aws_resources() {
    echo "Removing previously allocated AWS resources"
    # Purges $DEPLOYMENT_PREFIX prefixed SQS queues, S3 buckets and DynamoDB tables.
    python3 ./purge_AWS_resources.py
}

function remove_project_resources() {
    echo "Removing all openshift resources from selected project"
    oc delete all,cm,secrets --all
    if [ "$clean_aws_resources" == true ] ; then
        purge_aws_resources
    fi
}

function create_or_reuse_project() {
    if oc get project "${OC_PROJECT}"; then
        oc project "${OC_PROJECT}"
        remove_project_resources
    else
        oc new-project "${OC_PROJECT}"
    fi
}

function tag_rds_instance() {
    TAGS="Key=ENV,Value=${DEPLOYMENT_PREFIX}"
    echo "Tagging RDS instance with ${TAGS}"
    aws rds add-tags-to-resource \
            --resource-name "${RDS_ARN}" \
            --tags "${TAGS}"
}

function get_rds_instance_info() {
    aws --output=table rds describe-db-instances --db-instance-identifier "${RDS_INSTANCE_NAME}" 2>/dev/null
}

function allocate_aws_rds() {
    if ! get_rds_instance_info; then
        aws rds create-db-instance \
        --allocated-storage "${RDS_STORAGE}" \
        --db-instance-identifier "${RDS_INSTANCE_NAME}" \
        --db-instance-class "${RDS_INSTANCE_CLASS}" \
        --db-name "${RDS_DBNAME}" \
        --db-subnet-group-name "${RDS_SUBNET_GROUP_NAME}" \
        --engine postgres \
        --engine-version "9.6.1" \
        --master-username "${RDS_DBADMIN}" \
        --master-user-password "${RDS_PASSWORD}" \
        --publicly-accessible \
        --storage-type gp2
        #--storage-encrypted
        echo "Waiting (60s) for ${RDS_INSTANCE_NAME} to come online"
        sleep 60
        wait_for_rds_instance_info
    else
        echo "DB instance ${RDS_INSTANCE_NAME} already exists"
        wait_for_rds_instance_info
        if [ "$clean_aws_resources" == true ] ; then
            echo "recreating database"
            PGPASSWORD="${RDS_PASSWORD}" psql -d template1 -h "${RDS_ENDPOINT}" -U "${RDS_DBADMIN}" -c "drop database ${RDS_DBNAME}"
            PGPASSWORD="${RDS_PASSWORD}" psql -d template1 -h "${RDS_ENDPOINT}" -U "${RDS_DBADMIN}" -c "create database ${RDS_DBNAME}"
        fi
    fi
    tag_rds_instance
}

function wait_for_rds_instance_info() {
    while true; do
        echo "Trying to get RDS DB endpoint for ${RDS_INSTANCE_NAME} ..."

        RDS_ENDPOINT=$(get_rds_instance_info | grep -w Address | awk '{print $4}')
        RDS_ARN=$(get_rds_instance_info | grep -w DBInstanceArn | awk '{print $4}')

        if [ -z "${RDS_ENDPOINT}" ]; then
            echo "DB is still initializing, waiting 30 seconds and retrying ..."
            sleep 30
        else
            break
        fi
    done
}

