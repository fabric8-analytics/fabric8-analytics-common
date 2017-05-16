#!/bin/bash

# We use $PTH_ENV in ../deploy.sh
source conf

# We need to deploy these secrets first
curl -O https://gitlab.cee.redhat.com/bayesian/secrets/raw/master/secrets-template.yaml
../secrets-deploy.sh --secrets-file secrets-template.yaml

${CLOUD_DEPLOYER_PATH}/deploy.sh --conf conf --services services --secrets-template secrets-template-aws.yaml --secrets-deploy ../secrets-deploy.sh --system-deploy ../deploy.sh

