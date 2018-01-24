#!/bin/bash -e

# Remove fabric8-analytics project from Openshift along with allocated AWS resources.

# This script can eventually be merged with deploy.sh

here=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

source helpers.sh

#Check for configuration file
if ! [ -f "${here}/env.sh" ]
then
    echo '`env.sh` configuration file is missing. You can create one from the template:'
    echo 'cp env-template.sh env.sh'
    echo
    echo 'Modify the `env.sh` configuration file as necessary. See README.md file for more information.'
    exit 1
fi

#Check if required commands are available
tool_is_installed aws
tool_is_installed awk
tool_is_installed psql
tool_is_installed oc

#Load configuration from env variables
source env.sh

#Check if required env variables are set
is_set_or_fail RDS_PASSWORD "${RDS_PASSWORD}"
is_set_or_fail RDS_INSTANCE_NAME "${RDS_INSTANCE_NAME}"
is_set_or_fail OC_USERNAME "${OC_USERNAME}"
is_set_or_fail OC_PASSWD "${OC_PASSWD}"
is_set_or_fail AWS_ACCESS_KEY_ID "${AWS_ACCESS_KEY_ID}"
is_set_or_fail AWS_SECRET_ACCESS_KEY "${AWS_SECRET_ACCESS_KEY}"

openshift_login
delete_project_and_aws_resources
