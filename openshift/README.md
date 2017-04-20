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
```
# you can create/modify secrets in cloud-deploy/secrects-template.yaml and rerun this any time
./secrets-deploy.sh --secrets-file cloud-deploy/secrets-template.yaml
./deploy.sh
```

If you plan to use native Amazon services like SQS or Postgres, run:
```
AWS_NATIVE=1 ./deploy.sh
```

Then talk to application by getting the service or route endpoints using ```oc get services``` or ```oc get routes```.
