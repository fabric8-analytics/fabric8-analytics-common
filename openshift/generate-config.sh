#!/usr/bin/bash -e

here=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

if [[ $PTH_ENV ]]; then
  DEPLOYMENT_PREFIX=$PTH_ENV
else
  DEPLOYMENT_PREFIX=$(oc whoami)
fi

oc process -v DEPLOYMENT_PREFIX=${DEPLOYMENT_PREFIX} -f ${here}/config-template.yaml > ${here}/config.yaml

