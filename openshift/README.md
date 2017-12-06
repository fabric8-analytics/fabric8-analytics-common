# Openshift green field deployment of fabric8-analytics services

## Install required tools

Use your preferred package manager to install awk, aws-cli, psql, origin-clients, pwgen

## Configure fabric8-analytics services
All configuration for the deployment script resides in env.sh.
To configure your developemnt deployment copy env-template.sh

`cp env-template.sh env.sh`

Update variables with your AWS,Openshift and Github credentials.

### Generate RDS pasword

To generate password you will require tool named pwgen.
`pwgen -1cs 32`

Use generated password to update RDS_PASSWORD value

## Deploy fabric8-analytics services
Just run the deploy script and enjoy!

`$./deploy.sh

## Deploy your changes to dev-cluster
To deploy your changes, open a PR from your fork to the upstream repository. 
CentosCI will build your image and comment on the PR with an image name and tag.
Your image is available in the registry: docker pull registry.devshift.net/fabric8-analytics/worker-scaler:SNAPSHOT-PR-25

To update your dev deployment use [oc edit](https://docs.openshift.com/container-platform/3.4/cli_reference/basic_cli_operations.html#edit) from the command line or editor in web interface.
