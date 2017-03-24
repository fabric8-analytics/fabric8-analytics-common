#!/bin/bash

# We use $PTH_ENV in ../deploy.sh
source conf

${CLOUD_DEPLOYER_PATH}/deploy.sh --conf conf --services services --secrets-template secrets-template.yaml --secrets-deploy ../secrets-deploy.sh --system-deploy ../deploy.sh
