# Project Bayesian

## Overview

Bayesian is a new strategic initiative to help developers with the consumption of application components such as packages and containers.

## Project status

The project is an _very_ early alpha stage. So please expect many short comings, downtimes and rough edges. But with your feedback we will strive for the better.

# Using Bayesian

At this point we offer two ways of interacting with Baysian: A widget in SonarQube and an API:

## SonarQube

SonarQube is our developer facing integration point. For an in-depth example working with SonarQube see the [examples repo](https://github.com/baytemp/examples).

Note: A special plugin needs to be used for scanning Maven projects, find out [how to use it](sonarqube-widget/scanning_maven_projects.md).

## API

To get up and running with the API please refer to our [getting started guide](docs/getting_started.md). And refer to the [docs/api](docs/api) for a more detailed explanation and a [API
specification](docs/api/raml/) in
[RAML format](https://github.com/raml-org/raml-spec/blob/master/versions/raml-08/raml-08.md).

For an in-depth example using the API see the [examples repo](https://github.com/baytemp/examples).

## Triggering analyses from Jenkins

It is possible to trigger Bayesian analyses from Jenkins. Please refer to the [documentation](sonarqube-widget/running_from_jenkins.md) for details.

# Developing and Running the System

We have detailed [documentation](docs/developing_running.md) that describes possibilities of running whole Bayesian, doing code changes, running tests etc.
