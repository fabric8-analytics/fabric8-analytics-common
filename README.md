# Project Bayesian

## Overview

Bayesian is a new strategic initiative to help developers with the consumption of application components such as packages and containers. For more project information see:

* our [Mojo Page](https://mojo.redhat.com/groups/project-bayesian)
* the [Bayesian PDD](https://docs.google.com/document/d/1wBHfBrlIRodqCZQ1lDie1v9YwmEvSfC8vwzVD3lKhfs/edit) describing the scenarios we are targeting
* our [Trello Board](https://trello.com/b/6m5tjYhy/team-bayesian) what we are currently working on
* our mailing list [devtools-bayesian](https://post-office.corp.redhat.com/mailman/listinfo/devtools-bayesian) and our [mattermost channel](https://chat.openshift.io/rh-devtools/channels/bayesian)

## Project status

As of September 2016 we have a list of scenarios we are targeting and now iterate towards them. For this we are looking for feedback. Please consider using Bayesian via SonarQube or our API. 

The project is an _very_ early alpha stage. So please expect many short commings, downtimes and rough edges. But with your feedback we will strive for the better.

# Using Bayesian

At this point we offer two ways of interacting with Baysian: A widget in SonarQube and an API:

## [SonarQube](http://ose-vm1.lab.eng.blr.redhat.com:9000/)

SonarQube is our first developer facing integration point. We have a test instance running in a [test-lab](http://ose-vm1.lab.eng.blr.redhat.com:9000/). 

For an indepth example working with SonarQube see the [examples repo](https://gitlab.cee.redhat.com/bayesian/examples).

Note: A special plugin needs to be used for scanning Maven projects, find out [how to use it](sonarqube-widget/scanning_maven_projects.md).

## [API](http://ose-vm1.lab.eng.blr.redhat.com:32000/api/v1)

To get up and running with the API please refer to our [getting started guide](docs/getting_started.md). And refer to the [docs/api](docs/api) for a more detailed explanation and a [API
specification](docs/api/raml/) in
[RAML format](https://github.com/raml-org/raml-spec/blob/master/versions/raml-08/raml-08.md).

For an indepth example using the API see the [examples repo](https://gitlab.cee.redhat.com/bayesian/examples).

## Triggering analyses from Jenkins

It is possible to trigger Bayesian analyses from Jenkins. Please refer to the [documentation](sonarqube-widget/running_from_jenkins.md) for details.

---
---
---

# Developing Bayesian

This section is for those interessted in contributing to the development of Bayesian. Please read through our [glossary](docs/glossary.md) in case you are not sure about terms used in the docs.

## Running a Local Instance

### Getting All Repos

In order to have a good local development experience, the code repositories
are mounted inside containers, so that changes can be observed live or after
container restart (without image rebuilds).

In order to achieve that, all the individual Bayesian repos have to be
checked out. The helper script `setup.sh` is here to do that. Run `setup.sh -h`
and follow the instructions (most of the time, you'll be fine with running
`setup.sh` with no arguments).

### With Docker Compose

Follow the Docker based instructions for
[running a local instance](docs/running_whole_bayesian.md#running-via-docker-compose).

### Debugging Docker networking connectivity

Network connectivity problems can sometimes arise when attempting to build
container images locally that require access to the Red Hat internal network
during the build process. This is particularly common when using a VPN tunnel,
rather than being directly connected to the internal network.

The following three commands can be used to help determine if a local build
failure is due to that problem:

    $ curl -sI http://coprbe.devel.redhat.com/repos/
    $ sudo docker run --rm centos curl -sI http://coprbe.devel.redhat.com/repos/
    $ sudo docker run --rm fedora:25 curl -sI http://coprbe.devel.redhat.com/repos/

All of those should print out `HTTP/1.1 200 OK` and various other details, and
if they don't, then there's a problem accessing the Red Hat internal COPR
instance. The first command checks if the local host itself has internal
network access, while the latter two check connectivity from CentOS and
Fedora based Docker containers.

For Fedora clients, this [Stack Overflow post](http://stackoverflow.com/questions/35693117/how-can-i-give-docker-containers-access-to-a-dnsmasq-local-dns-resolver-on-the-h) describes a particular
problem that can arise with domain name resolution, as well as how to configure
Docker to use a dedicated local resolver running on the host system.

### Integration tests

Refer to the [integration testing README](integration-tests/README.md)
