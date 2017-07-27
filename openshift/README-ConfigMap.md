## Generate ConfigMap

Simply run:

```
./generate-config.sh
```

Note you can use `PTH_ENV` environment variable to generate config map for a specific deployment, for example:

```
PTH_ENV=STAGE ./generate-config.sh
```

The command above will generate config map for staging deployment.


## Deploy ConfigMap

Once you have the config map, you can deploy it:

```
oc apply -f config.yaml
```

