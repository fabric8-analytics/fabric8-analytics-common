#!/bin/bash -e

SECRETS_FILE=`dirname $0`/secrets-template.yaml

while [[ $# -gt 1 ]]; do
  key="$1"
  case $key in
    -s|--secrets-file)
      SECRETS_FILE=$2
      shift
      ;;
    *)
      echo "Unknown option $key, exiting"
      exit 1
  esac
  shift
done


oc process -f ${SECRETS_FILE} | oc apply -f -
