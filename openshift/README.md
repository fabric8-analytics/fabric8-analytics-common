# Deploying fabric8-analytics services

## Create a new project

`oc login` to your favorite OpenShift cluster and create a new project there:

```
oc new-project fabric8-analytics
```

## Deploy fabric8-analytics services

Generate and deploy [config map](./README-ConfigMap.md) first:

```
./generate-config.sh  # will create config.yaml file
oc apply -f config.yaml
```

Deploy secrets:

```
oc process -f secrets-template.yaml -v AWS_ACCESS_KEY_ID='..' -v AWS_SECRET_ACCESS_KEY='...' -v GITHUB_API_TOKENS='...' -v GITHUB_OAUTH_CONSUMER_KEY='...' -v GITHUB_OAUTH_CONSUMER_SECRET='...' -v FLASK_APP_SECRET_KEY='...' RDS_ENDPOINT='...' RDS_PASSWORD='...' | oc apply -f -
```

Note all secrets need to be base64 encoded:

```
echo -n 'my-secret-key' | base64 -w 0
```

See also:
* [how to allocate AWS resources](aws/README.md)
