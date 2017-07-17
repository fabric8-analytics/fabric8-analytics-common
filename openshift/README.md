# Deploying fabric8-analytics services

## Create a new project

`oc login` to your favourite OpenShift cluster and create a new project there:

```
oc new-project fabric8-analytics
```

## Deploy fabric8-analytics services

We use cloud-deployer tool, configured in [cloud-deploy/](cloud-deploy/), see also [cloud-deploy/README.md](cloud-deploy/README.md).

The cloud-deployer tool automatically generates and deploys correct ConfigMap for the deployment, but it's possible to [generate a ConfigMap](README-ConfigMap.md) manually and customize it.
