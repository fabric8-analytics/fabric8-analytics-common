# Deploying Bayesian for dev cluster

* Create a new project

```
oc new-project bayesian
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
