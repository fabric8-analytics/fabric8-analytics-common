## Running Whole Bayesian

### Requirements

Git, and possibly other packages, depending on how you want to run the system (see below).

### Red Hat internal network access

Several of the pre-built images, as well as some of the components used to rebuild those images,
are currently only available on the Red Hat internal network.

Running the below steps requires that the host and any Docker containers or Vagrant images run on
the host be able to access the Red Hat internal network.

### Usage
First, clone the repository and enter the newly created directory.

```
git clone git@github.com:redhat-developer/Bayesian.git
cd Bayesian/
```


### Running via docker-compose

Requirements:

* docker >= 1.10.0
* docker-compose >= 1.6.0
* Red Hat internal network access

Fedora 24 and 25 have docker-compose > 1.6 and docker > 1.10.0. You should be
able to run on Fedora 24/25 without any workarounds.

While Fedora 23 has docker-compose 1.6, it only has docker 1.9 due to an
incompatible change in the image storage format. This means docker-compose
in F23 won't handle the version 2 format used in `docker-compose.yml`.
Instructions on upgrading to Docker 1.10 in F23 can be found in
[this COPR repo](https://copr.fedorainfracloud.org/coprs/ncoghlan/docker-110/)
(created by one of the Bayesian devs, so devtools-bayesian can be used for any questions
about it)


You'll need to configure docker to use http instead of https for
docker-registry.usersys.redhat.com. To do this, add
`--insecure-registry docker-registry.usersys.redhat.com` to `OPTIONS` in
`/etc/sysconfig/docker` and restart the Docker daemon.

If you are using docker-machine with boot2docker add `--insecure-registry docker-registry.usersys.redhat.com` to `EXTRA_ARGS` in `/var/lib/boot2docker/profile` in the boot2docker image. As described [here](http://stackoverflow.com/questions/32808215/where-to-set-the-insecure-registry-flag-on-mac-os).

You'll also need to ensure Docker is configured to use the system certificate
store (this is the default behaviour, but it can also be configured to use a
custom store, which means it won't recognise the Red Hat internal CA)

Then run:

```
$ sudo docker-compose up
```

`docker-compose.yml` is written to mount `lib/cucoslib` and `server/bayesian`
from current directory as Python `cucoslib` and `bayesian` packages in the image,
so any changes made to the local checkout should be reflected in the
running image when using Docker Compose.

If you experience problems that may be explained by stale container images (e.g.
mismatches between checked out code and exception tracebacks), run:

```
$ sudo docker-compose build --pull
```

If you want Anitya to automatically scan for new releases, you need to use
both `docker-compose.yml` and `docker-compose.anitya-cron.yml` files explicitly:

```
$ sudo docker-compose -f docker-compose.yml -f docker-compose.anitya-cron.yml <up/pull/...>
```

#### Secrets

Some parts (GithubTask, DownstreamUsageTask, BlackDuckTask) need credentials for proper operation.
You can either drop a `secrets.yaml` (see [secrets repository](https://gitlab.cee.redhat.com/bayesian/secrets)) into `lib/hack/`
or provide environment variables to `worker` service in `docker-compose.yml`.
If both are provided, the environment variables take precedence over the `secrets.yaml` file.

#### Recommendation API

If you also want to run [Recommendation API](https://gitlab.cee.redhat.com/bayesian/Analytics/blob/master/README.adoc),
you first need initialize and fetch [Analytics repository](https://gitlab.cee.redhat.com/bayesian/Analytics)
as a git submodule and then you can run docker-compose with an extra configuration file:

```
$ git submodule init  # initialze submodule
$ git submodule update --remote  # fetch data
$ sudo docker-compose up
```

The Recommendation API will be accessible via [http://localhost:32100](http://localhost:32100).

#### Scaling

When running locally via docker-compose, you will likely not need to scale most of the system components. You may, however, want to run more workers, if you're running more analyses and want them finished faster. By default, only a single worker is run, but you can scale it to pretty much any number. Just run the whole system as described above and then in another terminal window execute:

```
$ sudo docker-compose scale worker=3
```

This will run additional 2 workers, giving you a total of 3 workers running. You can use this command repeatedly with different numbers to scale up and down as necessary.

For more information see [Scaling Celery workers using docker-compose](worker_scaling.md)

#### Indexing analyses in Elasticsearch
If you also want to periodically index new Bayesian analyses in Elasticsearch, run the `docker-compose` command as:

```
sudo docker-compose -f docker-compose.yml -f docker-compose.es_indexer.yml up
```

Note you will need to configure where the Elasticsearch server is running in `docker-compose.es_indexer.yml` config file.

### Running in Vagrant Box

Requirements:

* vagrant
* Red Hat internal network access

This repository also contains Vagrantfile which let's you easily run production-like environment. It's based on [projectatomic/adb](https://github.com/projectatomic/adb-atomic-developer-bundle) box.

```
sudo vagrant up
```

This command should bring up a VM with Kubernetes and whole Bayesian infrastructure running on top of it. If you do any changes to the code, you'll need to sync it

```
sudo vagrant rsync
```

and rebuild the images and re-deploy the application.

```
sudo UPDATE=1 vagrant provision
```

or

```
sudo vagrant ssh
/vagrant/orchestration/restart-coreapi.sh --update
```

`--update` option will only re-deploy coreapi and cucos-worker, not the whole infra.

Script `restart-coreapi.sh` will build `coreapi` and `cucos-worker` images by default. In case you want to pull them from the internal [Docker registry](docker-registry.usersys.redhat.com), you can do it with following command:

```
sudo PULL_BUILD=pull vagrant up
```

### Running on Kubernetes

This application is ready to run on top of Kubernetes orchestration. If you want to only try Bayesian, we suggest to use Vagrant (see the how-to above). If you want to deploy Bayesian to a VM, we suggest to use CentOS 7 and run following commands:

```
./orchestration/deploy.sh
./orchestration/restart-coreapi.sh
```

The script `deploy.sh` will install Kubernetes and all it's components, Cockpit, htop, disable SELinux (due to a bug with Kubes persistent storage) and set a password for `$USER` to be able to login through Cockpit.

The script `restart-coreapi.sh` will prepare images and deploy the app to Kubernetes. You can change the behaviour of script from building the images to pulling them by specifying `$PULL_BUILD` env variable like this:

```
export PULL_BUILD=pull
```

Kubernetes will create several directories in `/media`: `/media/worker-data`, `/media/rabbit-storage` and `/media/postgres-data` as shared and persistant storage.

There is also a script `kubernetes/getendpoints.sh` which prints out IPs and ports of Bayesian Frontend and Flower Web UI

### Running in OpenShift

TBD :)

### Accessing Services, Logs and Other Interesting Stuff

#### Services

When the whole application is started, there are several services you can access. When running through docker-compose, all of these services can be bound to `localhost`. When running with Vagrant or Kubernetes, use IP of the Vagrant box or virtual machine with Kubernetes respectively. Use these ports to get http access to following services:

1. Bayesian Server itself (see server-service.yaml) - port `32000`
2. Celery Flower (task queue monitor, see flower-service.yaml) - port `31000`
3. PGWeb (web UI for database, see pgweb-service.yaml) - port `31003`
4. Anitya (see anitya-service.yaml) - port `31005`
5. Cockpit (only for Kubernetes based setups) - port `9090`

You can also use `kubernetes/getendpoints.sh` script to see ports, assuming you're using Kubernetes.

Other internal services are:
* Anitya Cron and Anitya Postgres (see anitya-{cron,postgres}-controller.yaml)
* ElasticSearch Indexer (see indexer-controller.yaml)
* Pgbouncer (see pgbouncer-service.yaml)
* Postgres (see postgres-service.yaml)
* Worker (see worker-controller.yaml)

#### Logs

All services log to their stdout/stderr, which makes their logs viewable through Docker/Kubernetes:

* When using docker-compose, all logs are streamed to docker-compose output and you can view them there in realtime. If you want to see output of a single container only, use `docker logs -f <container>`, e.g. `docker logs -f coreapi-server` (the `-f` is optional and it switches on the "follow" mode).
* When using Kubernetes (no matter if through Vagrantbox or not), you have to:
  1. ssh to the machine where Kubernetes run
  2. Run `kubectl get pods` and see what pod you want to view logs for, e.g. something like `bc-server-ge57y`
  3. Run `kubectl logs -f bc-server-ge57y` (the `-f` is optional and it switches on the "follow" mode).
