# Developing fabric8-analytics

This section is for those interested in contributing to the development of
fabric8-analytics. Please read through our [glossary](../docs/glossary.md) in
case you are not sure about terms used in the docs.

## Running a Local Instance

### Getting All Repos

### Requirements

Git, and possibly other packages, depending on how you want to run the system
(see below).

### Getting the Code

First of all, clone the `common` repo (this one). This includes all
the configuration for running the whole system as well as some helper
scripts and docs.

In order to have a good local development experience, the code repositories
are mounted inside containers, so that changes can be observed live or after
container restart (without image rebuilds).

In order to achieve that, all the individual fabric8-analytics repos have to be
checked out. The helper script `setup.sh` is here to do that. Run `setup.sh -h`
and follow the instructions (most of the time, you'll be fine with running
`setup.sh` with no arguments).

### Running via docker-compose

Requirements:

* docker >= 1.10.0
* docker-compose >= 1.6.0

Fedora 24, 25 and 26 have docker-compose > 1.6 and docker > 1.10.0. You should be
able to run on Fedora 24/25/26 without any workarounds.

You'll need to configure docker to use http instead of https for
docker-registry.usersys.redhat.com. To do this, add
`--insecure-registry docker-registry.usersys.redhat.com` to `OPTIONS` in
`/etc/sysconfig/docker` and restart the Docker daemon.

If you are using docker-machine with boot2docker add
`--insecure-registry docker-registry.usersys.redhat.com` to `EXTRA_ARGS`
in `/var/lib/boot2docker/profile` in the boot2docker image. As described
[here](http://stackoverflow.com/questions/32808215/where-to-set-the-insecure-registry-flag-on-mac-os).

You'll also need to ensure Docker is configured to use the system certificate
store (this is the default behaviour, but it can also be configured to use a
custom store, which means it won't recognise the Red Hat internal CA)

Then run:

```
$ sudo docker-compose up
```

To get the system up.

If the following error message is displayed (Fedora 25 installation):
`got an unexpected keyword argument 'user_agent'`
you would need to upgrade the docker-py library by the following command:

```
$ sudo pip install --upgrade 'docker-py>=1.9.0'
```

If you want a good development setup (source code mounted inside the
containers, ability to rebuild images using docker-compose), use:

```
$ sudo ./docker-compose.sh up
```

`docker-compose.sh` will effectively mount source code from checked out
fabric8-analytics sub-projects into the containers, so any changes made to the local
checkout will be reflected in the running container. Note, that some
containers (e.g. server) will pick this up interactively, others (e.g. worker)
will need a restart to pick the new code up.

```
$ sudo ./docker-compose.sh build --pull
```

If you want Anitya to automatically scan for new releases, you need to use
both `docker-compose.yml` and `docker-compose.anitya-cron.yml` files explicitly:

```
$ sudo docker-compose -f docker-compose.yml -f docker-compose.anitya-cron.yml <up/pull/...>
```

or

```
$ sudo ./docker-compose.sh -f docker-compose.yml -f docker-compose.anitya-cron.yml <up/pull/...>
```

#### Secrets

Some parts (GithubTask, DownstreamUsageTask, BlackDuckTask) need credentials
for proper operation. You can either drop a `secrets.yaml` into `worker/hack`.
Sample secrets file is generated when running `setup.sh` script.

Another options is to provide environment variables to `worker` service
in `docker-compose.yml`. If both are provided, the environment variables take
precedence over the `secrets.yaml` file.

#### Scaling

When running locally via docker-compose, you will likely not need to scale
most of the system components. You may, however, want to run more workers,
if you're running more analyses and want them finished faster. By default,
only a single worker is run, but you can scale it to pretty much any number.
Just run the whole system as described above and then in another terminal
window execute:

```
$ sudo docker-compose scale worker-api=2 worker-ingestion=2
```

This will run additional 2 workers, giving you a total of 4 workers running.
You can use this command repeatedly with different numbers to scale up and
down as necessary.

For more information see [Scaling Celery workers using docker-compose](worker_scaling.md)

### Running in OpenShift

TBD :)

### Accessing Services, Logs and Other Interesting Stuff

#### Services

When the whole application is started, there are several services you can
access. When running through docker-compose, all of these services will be
bound to `localhost`. When running with OpenShift, TODO

1. fabric8-analytics Server itself (see server-service.yaml) - port `32000`
2. fabric8-analytics Jobs API - port `34000`
3. Celery Flower (task queue monitor, see flower-service.yaml) - port `31000`
   Celery Flower is only run if you run with `-f docker-compose.debug.yml`
4. PGWeb (web UI for database, see pgweb-service.yaml) - port `31003`
   PGWeb is only run if you run with `-f docker-compose.debug.yml`
5. Anitya (see anitya-service.yaml) - port `31005`
6. Minio S3 - port `33000`

#### Logs

All services log to their stdout/stderr, which makes their logs viewable
through Docker:

* When using docker-compose, all logs are streamed to docker-compose output
and you can view them there in real-time. If you want to see output of a single
container only, use `docker logs -f <container>`, e.g.
`docker logs -f coreapi-server` (the `-f` is optional and it switches on
the "follow" mode).

## Integration tests

Refer to the [integration testing README](../integration-tests/README.md)
