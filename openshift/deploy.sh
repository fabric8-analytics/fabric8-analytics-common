#!/usr/bin/bash -e

# Note this script assumes that config maps and secrets are already deployed

function oc_process_apply() {
  echo -e "\n Processing template - $1 ($2) \n"
  oc process -f $1 $2 | oc apply -f -
}

here=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
templates_dir="${here}/templates"
templates="fabric8-analytics-jobs fabric8-analytics-server fabric8-analytics-data-model fabric8-analytics-worker fabric8-analytics-pgbouncer fabric8-analytics-recommender gremlin-docker anitya-docker"

# Get templates for fabric8-analytics projects
for template in ${templates}
do
  curl -sS https://raw.githubusercontent.com/fabric8-analytics/${template}/master/openshift/template.yaml > ${templates_dir}/${template#fabric8-analytics-}.yaml
done

oc_process_apply ${templates_dir}/pgbouncer.yaml
oc_process_apply ${templates_dir}/gremlin-docker.yaml "-p CHANNELIZER=http -p REST_VALUE=1 -p IMAGE_TAG=latest"
oc_process_apply ${templates_dir}/anitya-docker.yaml
oc_process_apply ${templates_dir}/recommender.yaml
oc_process_apply ${templates_dir}/data-model.yaml
oc_process_apply ${templates_dir}/worker.yaml "-p WORKER_ADMINISTRATION_REGION=ingestion"
oc_process_apply ${templates_dir}/worker.yaml "-p WORKER_ADMINISTRATION_REGION=api"
oc_process_apply ${templates_dir}/server.yaml
oc_process_apply ${templates_dir}/jobs.yaml

