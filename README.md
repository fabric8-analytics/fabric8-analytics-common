# Project Fabric8-Analytics

*Note on naming: The Fabric8-Analytics project has evolved from 2 different projects called "cucos" and "bayesian". We're currently in process of renaming the modules and updating documentation. Until that is completed, please consider "cucos" and "bayesian" to be synonyms of "Fabric8-Analytics".*

## Overview

Fabric8-Analytics is a new strategic initiative to help developers with the consumption of application components such as packages and containers.

# Using Fabric8-Analytics

At this point we offer several ways of interacting with Baysian: API, a widget in SonarQube and Jenkins plugin. Fabric8-Analytics is also built into the [openshift.io](https://openshift.io) build pipeline.

## API

To get up and running with the API please refer to the [API server README](https://github.com/baytemp/server/blob/master/README.md).

For an in-depth example using the API see the [examples repo](https://github.com/baytemp/examples).

## SonarQube

SonarQube is our developer facing integration point. For an in-depth example working with SonarQube see the [examples repo](https://github.com/baytemp/examples).

Note: A special plugin needs to be used for scanning Maven projects, find out [how to use it](https://github.com/baytemp/sonarqube-plugin).

## Triggering analyses from Jenkins

We have a Fabric8-Analytics [Jenkins plugin](https://github.com/baytemp/jenkins-plugin).

It is also possible to trigger Fabric8-Analytics analyses from Jenkins. Please refer to the [documentation](https://github.com/baytemp/sonarqube-plugin/blob/master/docs/running_from_jenkins.md) for details.

# Developing and Running the System

We have detailed [documentation](docs/developing_running.md) that describes possibilities of running whole Fabric8-Analytics, doing code changes, running tests etc.
