# Openshift green field deployment of fabric8-analytics services

Config map and secrets are generated from the configuration stored in environment variables.

## Configure fabric8-analytics services
All configuration for the deployment script resides in env.sh.
Create file env.sh inside this directory with following contents.
This script is ignored by git so feel free to change it locally.

`export OC_URI='dev.rdu2c.fabric8.io:8443'`

`export OC_USERNAME='Not set'`

`export OC_PASSWD='Not set'`

`export OC_PROJECT=$(whoami)'-greenfield-test'`

`export AWS_ACCESS_KEY_ID='Not set'`

`export AWS_SECRET_ACCESS_KEY='Not set'`

`export GITHUB_API_TOKENS='Not set'`

`export GITHUB_OAUTH_CONSUMER_KEY='Not set'`

`export GITHUB_OAUTH_CONSUMER_SECRET='Not set'`

`export FLASK_APP_SECRET_KEY='Not set'`

`export RDS_ENDPOINT=''`

`export RDS_INSTANCE_NAME="$OC_USERNAME-bayesiandb"`

`export RDS_INSTANCE_CLASS='db.t2.micro'`

`export RDS_DBNAME='postgres'`

`export RDS_DBADMIN='coreapi'`

`export RDS_STORAGE=5`

`export RDS_PASSWORD='somethingclever'`

`export RDS_SUBNET_GROUP_NAME='dv peering az'`

## Deploy fabric8-analytics services
Just run the deploy script and enjoy!

`$./deploy.sh`
