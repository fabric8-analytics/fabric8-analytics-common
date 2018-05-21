# Project Fabric8-Analytics

[![Build Status](https://ci.centos.org/buildStatus/icon?job=devtools-e2e-fabric8-analytics)](https://ci.centos.org/job/devtools-e2e-fabric8-analytics/)

*Note on naming: The Fabric8-Analytics project has evolved from 2 different projects called "cucos" and "bayesian". We're currently in process of renaming the modules and updating documentation. Until that is completed, please consider "cucos" and "bayesian" to be synonyms of "Fabric8-Analytics".*

## Overview

Fabric8-Analytics is a new strategic initiative to help developers with the consumption of application components such as packages and containers.

# Using Fabric8-Analytics

At this point we offer several ways of interacting with Fabric8-Analytics: API, a widget in SonarQube and Jenkins plugin. Fabric8-Analytics is also built into the [openshift.io](https://openshift.io) build pipeline.

## API

To get up and running with the API please refer to the [API server README](https://github.com/fabric8-analytics/fabric8-analytics-server/blob/master/README.md).

For an in-depth example using the API see the [examples repo](https://github.com/fabric8-analytics/examples).

## SonarQube

SonarQube is our developer facing integration point. For an in-depth example working with SonarQube see the [examples repo](https://github.com/fabric8-analytics/examples).

Note: A special plugin needs to be used for scanning Maven projects, find out [how to use it](https://github.com/fabric8-analytics/fabric8-analytics-sonarqube-plugin).

## Triggering analyses from Jenkins

We have a Fabric8-Analytics [Jenkins plugin](https://github.com/fabric8-analytics/fabric8-analytics-jenkins-plugin).

It is also possible to trigger Fabric8-Analytics analyses from Jenkins. Please refer to the [documentation](https://github.com/fabric8-analytics/fabric8-analytics-sonarqube-plugin/blob/master/docs/running_from_jenkins.md) for details.

# Developing and Running the System

We have detailed [documentation](https://github.com/fabric8-analytics/fabric8-analytics-deployment/blob/master/README.md) that describes possibilities of running whole Fabric8-Analytics, doing code changes, running tests etc.

### Footnotes

#### Coding standards

- You can use scripts `run-linter.sh` and `check-docstyle.sh` to check if the code follows [PEP 8](https://www.python.org/dev/peps/pep-0008/) and [PEP 257](https://www.python.org/dev/peps/pep-0257/) coding standards. These scripts can be run w/o any arguments:

```
./run-linter.sh
./check-docstyle.sh
```

The first script checks the indentation, line lengths, variable names, white space around operators etc. The second
script checks all documentation strings - its presence and format. Please fix any warnings and errors reported by these
scripts.

#### Code complexity measurement

The scripts `measure-cyclomatic-complexity.sh` and `measure-maintainability-index.sh` are used to measure code complexity. These scripts can be run w/o any arguments:

```
./measure-cyclomatic-complexity.sh
./measure-maintainability-index.sh
```

The first script measures cyclomatic complexity of all Python sources found in the repository. Please see [this table](https://radon.readthedocs.io/en/latest/commandline.html#the-cc-command) for further explanation how to comprehend the results.

The second script measures maintainability index of all Python sources found in the repository. Please see [the following link](https://radon.readthedocs.io/en/latest/commandline.html#the-mi-command) with explanation of this measurement.

