# Integration Tests for Bayesian Core API

This repository contains integration tests for the fabric8-analytics services.

The tests can be run against existing deployment, or locally via docker-compose.

Following environment variables can be used to test specific deployments:

`F8A_API_URL` - API server URL
`F8A_JOB_API_URL` - jobs service URL

By default the system running on localhost will be tested.

It starts and stops Bayesian multiple times, so is not currently containerised
itself - you need to suitably configure a Python environment on the host
system, and the user running the integration tests currently needs to be a
member of the `docker` group (allowing execution of `docker-compose`
without `sudo`). For further information on how to setup and use Docker as
a non-root user, read the detailed steps described
[here](https://docs.docker.com/engine/installation/linux/linux-postinstall/).

## Creating new tests

Feature tests are written using [behave](http://pythonhosted.org/behave/). To
add new feature tests, simply edit an existing `<name>.feature` file in
`features/` (or create a new one) and fill in missing steps in
`features/steps/common.py` (or create a new step file, where appropriate).

### Currently defined features

* [Smoke tests](features/smoketest.feature): Smoke tests for checking if main
  API endpoints are available and work as expected
* [Server API](features/server_api.feature): API tests for the server module
* [Jobs API](features/jobs_api.feature): API tests for the jobs module
* [Stack analysis v2](features/stack_analyses_v2.feature): API tests for the
  stack analysis endpoint `/api/v2/stack-analyses/`
* [Component analysis](features/components.feature): API tests for the
  component analysis endpoints under `/api/v1/component-analyses/`
* [Selfcheck](features/selfcheck.feature): Some checks if the test steps are
  working correctly

### Older tests that have to be updated

* [Stack analysis](features/stackanalysis.feature): API tests for the
  stack analysis endpoint `/api/v1/stack-analyses/`
* [Known ecosystems](features/ecosystems.feature): API tests for the
  known ecosystems endpoint `/api/v1/ecosystems/`
* [Known packages](features/packages.feature): API tests for the
  per-ecosystem known packages endpoints under `/api/v1/packages/`
* [Known versions](features/versions.feature): API tests for the
  per-package known versions endpoints under `/api/v1/versions/`

### Adding new feature files

When adding a new feature file, also add it to
[feature_list.txt](feature_list.txt), as that determines the set of
features executed by the [runtest.sh](runtest.sh) script.

### Currently defined test steps

Documentation for the module with test steps is automatically generated into
the file [common.html](https://fabric8-analytics.github.io/common.html). The
available test steps are not currently documented yet, so refer to either the
existing scenario definitions for usage examples, or else the step definitions
in [features/steps/common.py](features/steps/common.py) and the adjacent step
files.

### Adding new test step files

No additional changes are needed when adding a new test step file, as `behave`
will automatically check all Python files in the `steps` directory for
step definitions.

Note that a single step definition can be shared amongst multiple steps
by stacking decorators. For example::

    @when('I wait {num:d} seconds')
    @then('I wait {num:d} seconds')
    def pause_scenario_execution(context, num):
        time.sleep(num)

Allows client pauses to be inserted into both `Then` and `When` clauses
when defining a test scenario.


### Writing new test steps

The `behave` hooks in [features/environment.py](features/environment.py)
and some of the common step definitions add a number of useful attributes
and methods to the `behave` context.

The available methods include:

* `is_running()`: indicates whether or not the core API service is running
* `start_system()`: Start the API service in its default configuration using
  Docker Compose
* `teardown_system()`: Shut down the API service and remove all related
  container volumes
* `restart_system()`: Tears down and restarts the API service in its default
  configuration
* `run_command_in_service`: see [features/environment.py](features/environment.py)
* `exec_command_in_container`: see [features/environment.py](features/environment.py)

The available attributes include:

* `response`: a [requests.Response]() instance containing the most recent
  response retrieved from the server API (steps making requests to the API
  should set this, steps checking responses from the server should query it)
* `resource_manager`: a [contextlib.ExitStack](https://docs.python.org/3/library/contextlib.html#contextlib.ExitStack)
  instance for registering resources to be cleaned up at the end up of the
  current test scenario
* `docker_compose_path`: a list of Docker compose files defining the 
  `default configuration` when running under Docker Compose

Due to the context lifecycle policies defined by `behave` any changes to these
attributes in step definitions only remain in effect until the end of the
current scenario.


## Host environment

The host environment must be configured with `docker-compose`, the `behave`
behaviour driven development testing framework, and a few other dependencies
for particular behavioural checks.

This can be handled as either a user level component installation::

    $ pip install --user -r requirements.txt

Or else by setting up a Python virtual environment (either Python 2 or 3) and
installing the necessary components::

    $ pip install -r requirements.txt


## Test execution

The test suite is executed as follows::

    $ ./runtest.sh <arguments>

Arguments passed to the test runner are passed through to the underlying
`behave` invocation, so consult the `behave` docs for the full list of
available flags.

Other custom configuration settings available:

  * `-D dump_logs=true` (optional, default is not to print container logs) -
    requests display of container logs via `docker-compose logs` when at the
    end of each test scenario
  * `-D dump_errors=true` (optional, default is not to print container logs) -
    as for `dump_logs`, but only dumps the logs for scenarios that fail.
  * `-D tail_logs=50` (optional, default is to print 50 lines) - specifies the
    number of log lines to print for each container when dumping container
    logs. Implies `dump_errors=true` if neither `dump_logs` nor `dump_errors`
    is specified
  * `-D coreapi_server_image=bayesian/bayesian-api`
    (optional, default is `bayesian/bayesian-api`) - name of Bayesian core API server image
  * `-D coreapi_worker_image=bayesian/cucos-worker` (optional, default is `bayesian/cucos-worker`) - name of Bayesian
    Worker image
  * `-D coreapi_url=http://1.2.3.4:32000` (optional, default is `http://localhost:32000`)
  * `-D breath_time=10` (optional, default is `5`) - time to wait before testing

**Important: running with non-default image settings will force-retag the given
images as `bayesian/bayesian-api` and `bayesian/worker` so `docker-compose`
can find them. This may affect subsequent `docker` and `docker-compose` calls**

Some of the tests may be quite slow, you can skip them by passing
`--tags=-slow` option to `behave`.


## Packages that needs to be imported into database

The following packages needs to be imported into the database for successful test run

### NPM ecosystem

```
sequence
array-differ
array-flatten
array-map
array-parallel
array-reduce
array-slice
array-union
array-uniq
array-unique
lodash
lodash.assign
lodash.assignin
lodash._baseuniq
lodash.bind
lodash.camelcase
lodash.clonedeep
lodash.create
lodash._createset
lodash.debounce
lodash.defaults
lodash.filter
lodash.findindex
lodash.flatten
lodash.foreach
lodash.isplainobject
lodash.mapvalues
lodash.memoize
lodash.mergewith
lodash.once
lodash.pick
lodash._reescape
lodash._reevaluate
lodash._reinterpolate
lodash.reject
lodash._root
lodash.some
lodash.tail
lodash.template
lodash.union
lodash.without
npm
underscore
```

### PyPi ecosystem

```
clojure_py
requests
scrapy
Pillow
SQLAlchemy
Twisted
mechanize
pywinauto
click
scikit-learn
coverage
cycler
numpy
mock
nose
scipy
matplotlib
nltk
pandas
parsimonious
httpie
six
wheel
pygments
setuptools
```

### Maven ecosystem

```
io.vertx:vertx-core
io.vertx:vertx-web
io.vertx:vertx-jdbc-client
io.vertx:vertx-rx-java
io.vertx:vertx-web-client
io.vertx:vertx-web-templ-freemarker
io.vertx:vertx-web-templ-handlebars
io.vertx:vertx-web
org.springframework:spring-websocket
org.springframework:spring-messaging
org.springframework.boot:spring-boot-starter-web
org.springframework.boot:spring-boot-starter
org.springframework:spring-websocket
org.springframework:spring-messaging
```

## TODO

- make it possible to run the integration tests from a venv even when docker
  access requires sudo
