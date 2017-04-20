#!/usr/bin/bash -e

if [[ $PTH_ENV ]]; then
  DEPLOYMENT_PREFIX=$PTH_ENV
else
  DEPLOYMENT_PREFIX=$(oc whoami)
fi

oc process -v DEPLOYMENT_PREFIX=${DEPLOYMENT_PREFIX} -f config-template.yaml > config.yaml

