# Deploying Bayesian for dev cluster

* Create a new project

```
oc new-project bayesian
```

* Generate ConfigMap

```
./generate-config.sh
```

Note you can use `PTH_ENV` environment variable to generate config for a specific deployment, for example:

```
PTH_ENV=STAGE ./generate-config.sh
```

The command above will generate config for staging deployment.

Once you have the config, you can deploy it:

```
oc apply -f config.yaml
```

* Deploy all the templates

We use cloud-deployer tool, configured in [cloud-deploy/](cloud-deploy/), see also [cloud-deploy/README.md](cloud-deploy/README.md)

Then talk to application by getting the service or route endpoints using ```oc get services``` or ```oc get routes```.
