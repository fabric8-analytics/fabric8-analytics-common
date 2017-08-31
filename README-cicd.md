# fabric8-analytics CI/CD how-to

## About fabric8-analytics CI/CD

CentOS CI builds and deploys all fabric8-analytics deployable units.
This how-to will show you how you can setup CI/CD in CentOS for a new project.

Prerequisites:
- Dockerfile
- OpenShift template

This guide assumes that you already have Dockerfile for your new project
and you're able to deploy the image to OpenShift (you already have the template).

If you're missing either of those, you can always take some inspiration from already deployed fabric8-analytics projects.
Especially when it comes to OpenShift templates, because they all look pretty much alike.


## Enabling CI/CD for a new project

### Have CI scripts in your repository

CI looks for certain scripts in your repository. These scripts are basically CI job definitions.
Common practice in CentOS CI is to have at least following two scripts in your repository:

* [cico_run_tests.sh](https://github.com/fabric8-analytics/fabric8-analytics-pgbouncer/blob/master/cico_run_tests.sh)

This script gets executed in CI on every pull request. The script should build the docker image (if necessary) run unit and first level integration tests.

* [cico_build_deploy.sh](https://github.com/fabric8-analytics/fabric8-analytics-pgbouncer/blob/master/cico_build_deploy.sh)

This script gets executed on every merge to master branch. This script should also build the docker image and run unit and integration tests.
If the tests passed, the script should push the docker image to the `push.registry.devshift.net` registry.


It's also common to have following auxiliary script in your repository:

* [cico_setup.sh](https://github.com/fabric8-analytics/fabric8-analytics-pgbouncer/blob/master/cico_setup.sh)

Machines in CentOS CI where all builds and tests run are always clean, i.e. there is no docker installed and etc.
The purpose of this script is to set up CI environment and provide various helper functions that can be used in both `cico_run_tests.sh` and `cico_build_deploy.sh` scripts.

* [Makefile](https://github.com/fabric8-analytics/fabric8-analytics-pgbouncer/blob/master/Makefile)

Optional, it can be used by developers outside CI environment. `cico_*` scripts expect that the environment is disposable, but developer's laptop is not.

It's usually a good idea to copy these scripts from an existing repo and simply adapt them for your needs.


### Configure CI/CD jobs in almighty/almighty-jobs

CentOS CI will only find out about your project if you configure a job for it via [almighty/almighty-jobs](https://github.com/almighty/almighty-jobs) GitHub repository.
Basic templates for fabric8-analytics projects already exists there, so if you're not doing anything special in your project,
then you can simply reuse following snippets:

For pull requests:
```yaml
        - '{ci_project}-{git_repo}-fabric8-analytics':    # template reference, keep intact
            git_organization: fabric8-analytics           # GitHub organization where your project lives
            git_repo: fabric8-analytics-data-model        # short name of the GitHub repository
            ci_project: 'devtools'                        # group in CI, keep intact
            ci_cmd: '/bin/bash cico_run_tests.sh'         # script to run on pull requests
            timeout: '20m'                                # how long to wait before giving up (reaching the time limit will fail the test/build)
```

For master branch builds:
```yaml
        - '{ci_project}-{git_repo}-f8a-build-master':     # template reference, keep intact
            git_organization: fabric8-analytics           # GitHub organization where your project lives
            git_repo: fabric8-analytics-data-model        # short name of the GitHub repository
            ci_project: 'devtools'                        # group in CI, keep intact
            ci_cmd: '/bin/bash cico_build_deploy.sh'      # script to run on merge to master
            saas_git: saas-analytics                      # short name of the GitHub repository for tracking deployments; always [saas-analytics](https://github.com/openshiftio/saas-analytics)
            deployment_units: 'data-importer'             # "name" element from the saas-analytics configuration file, e.g.: https://github.com/openshiftio/saas-analytics/blob/master/bay-services/data-importer.yaml#L4
            deployment_configs: 'bayesian-data-importer'  # name of the OpenShift deployment config, e.g.: https://github.com/fabric8-analytics/fabric8-analytics-data-model/blob/f058982e7b75dccf97b5adec9ea975530a1731fe/openshift/template.yaml#L29
            timeout: '20m'                                # how long to wait before giving up (reaching the time limit will fail the test/build)
```

If build was successful and first level tests passed on merge to master builds, then the new image will be automatically deployed
to staging environment and E2E tests will run against it.
If E2E tests fail, CI will automatically rollback the deployment to previous (working) version.

Simply adjust values, where necessary, and open a PR
([example](https://github.com/almighty/almighty-jobs/pull/271/commits/2fe60ee7e0881d026889da2b67313a71869b8c85)).

### Configuration in deployment tracking repository

A tool called [saasherder](https://github.com/openshiftio/saasherder) is responsible for all deployments to staging and production.
All projects need to have a deployment configuration file in
[openshiftio/saas-analytics](https://github.com/openshiftio/saas-analytics/tree/master/bay-services) repository.

It may look like this:

```yaml
services:
- hash: 0f6d2d8f2e388d4562a0a029ef9485249e529a9d
  hash_length: 7
  name: data-importer
  environments:                     # deployments can be configured differently in staging and production
  - name: production
    parameters:
      REPLICAS: 4
  - name: staging
    parameters:
      REPLICAS: 1
  path: /openshift/template.yaml    # path where to find OpenShift template in the repository
url: https://github.com/fabric8-analytics/fabric8-analytics-data-model/
```

See the [official docs](https://github.com/openshiftio/saasherder#service-yaml) for more information.

Note if you only want to deploy your project to staging for now, you can set `hash` to `none`.


### Configure webhooks in your repository

You are almost set now, the only thing missing is to configure webhooks in your GitHub repository.
Please refer to the [official CentOS CI documentation](https://wiki.centos.org/QaWiki/CI/GithubIntegration) for more information.


## Promoting to production

The version of a service which runs in production is controlled by the `hash` key in corresponding deployment config file
in [openshiftio/saas-analytics](https://github.com/openshiftio/saas-analytics/tree/master/bay-services) repository.

If you want to promote new build to production, simply open a PR
([example](https://github.com/openshiftio/saas-analytics/pull/67/commits/215f0f06998f3659d65f6962fb9aa2bcc2fe4db9))
and ping @msrb, @srikrishna, or Service Delivery people on Mattermost.
