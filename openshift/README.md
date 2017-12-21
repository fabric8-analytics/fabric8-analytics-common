# Openshift green field deployment of fabric8-analytics services

## Install required tools

Use your preferred package manager to install awk, aws-cli, psql, origin-clients, pwgen

on Fedora:
`sudo dnf install gawk awscli pwgen postgresql origin-clients`

Mac users will require to install gawk from brew.

## Configure fabric8-analytics services
All configuration for the deployment script resides in env.sh.
To configure your development deployment copy env-template.sh

`cp env-template.sh env.sh`

Update variables with your AWS,Openshift and Github credentials.

### Generate RDS pasword

To generate password you will require tool named pwgen.
`pwgen -1cs 32`

Use generated password to update RDS_PASSWORD value

### Run oc login

dev cluster uses a self-signed certificate.
We need to log in using the command line and accept the certificate.

`oc login $OC_URI -u $OC_USERNAME -p $OC_PASSWD`

## Deploy fabric8-analytics services
Just run the deploy script and enjoy!

`$./deploy.sh`

## Deploy your changes to dev-cluster

Assume you have opened a PR in one of the [fabric8-analytics](https://github.com/fabric8-analytics) repositories.
Once tests pass in the PR, [CentosCI](https://ci.centos.org) builds your image and adds a similar comment to the PR:

`Your image is available in the registry: docker pull registry.devshift.net/fabric8-analytics/worker-scaler:SNAPSHOT-PR-25`

To update your dev deployment you can use one the following ways:

- [oc edit](https://docs.openshift.com/container-platform/3.4/cli_reference/basic_cli_operations.html#edit) from command line
- editor in web interface: `Applications` -> `Deployments` -> select deployment -> `Actions` -> `Edit YAML`
- edit [deploy.sh](deploy.sh), add `"-p IMAGE_TAG=SNAPSHOT-PR-25"` (with correct tag) to corresponding `oc_process_apply` call at the end of the file and (re-)run `./deploy.sh`.

## E2E test

### Configure OSIO token

In your created env.sh set the RECOMMENDER_API_TOKEN.
Token is available on your profile page after clicking on Update profile button.

You will have to change email adress to one asssociated with your osio account [Quick Link](https://openshift.io/thrcka@redhat.com/_update)

### Run E2E test agaist your deployment

Environment variables are set by running the script.
`./run-e2e-test.sh`

[More information](https://github.com/fabric8-analytics/fabric8-analytics-common/tree/master/integration-tests)
