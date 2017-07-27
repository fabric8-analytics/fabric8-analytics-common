#!/bin/bash

${CLOUD_DEPLOYER_PATH}/deploy.sh --conf conf --services services --secrets-template secrets-template-aws.yaml --secrets-deploy ./dont-deploy.sh --system-deploy ./dont-deploy.sh

