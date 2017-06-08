#!/usr/bin/bash -e

function oc_process_apply() {
  echo -e "\n Processing template - $1 ($2) \n"
  oc process -f $1 $2 | oc apply -f -
}

here=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
templates_dir="${here}/templates"
f8a_templates="jobs server data-model worker pgbouncer recommender"
other_templates="gremlin-docker anitya-docker"

# generate and apply the ConfigMap
. ${here}/generate-config.sh
oc apply -f ${here}/config.yaml

# get templates from fabric8-analytics GH organization
for template in $f8a_templates
do
  curl -sS https://raw.githubusercontent.com/fabric8-analytics/fabric8-analytics-${template}/master/openshift/template.yaml > ${templates_dir}/${template}.yaml
done

for template in $other_templates
do
  curl -sS https://raw.githubusercontent.com/fabric8-analytics/${template}/master/openshift/template.yaml > ${templates_dir}/${template}.yaml
done

# get gremlin template
curl -sS  https://raw.githubusercontent.com/containscafeine/data-model/master/gremlin/openshift/template.yaml> ${templates_dir}/gremlin.yaml
# get anitya template
curl -sS https://raw.githubusercontent.com/bkabrda/anitya-docker/master/openshift/template.yaml > ${templates_dir}/anitya.yaml

oc_process_apply ${templates_dir}/pgbouncer.yaml
oc_process_apply ${templates_dir}/gremlin-docker.yaml "-v CHANNELIZER=http -v REST_VALUE=1"
oc_process_apply ${templates_dir}/anitya-docker.yaml
oc_process_apply ${templates_dir}/recommender.yaml
oc_process_apply ${templates_dir}/data-model.yaml
oc_process_apply ${templates_dir}/worker.yaml "-v WORKER_ADMINISTRATION_REGION=ingestion"
oc_process_apply ${templates_dir}/worker.yaml "-v WORKER_ADMINISTRATION_REGION=api"
oc_process_apply ${templates_dir}/server.yaml
oc_process_apply ${templates_dir}/jobs.yaml

