## Generate ConfigMap

Simply run:

```
./generate-config.sh
```

Note you can use `PTH_ENV` environment variable to generate config for a specific deployment, for example:

```
PTH_ENV=STAGE ./generate-config.sh
```

The command above will generate config for staging deployment.


## Deploy ConfigMap

Once you have the config, you can deploy it:

```
oc apply -f config.yaml
```
