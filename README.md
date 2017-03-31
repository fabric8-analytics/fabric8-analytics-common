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

# Developing and Running the System

We have detailed [documentation](docs/developing_running.md) that describes possibilites of running whole Bayesian, doing code changes, running tests etc.
