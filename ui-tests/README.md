# UI Tests

## Preliminary info

All the tests defined in this directory are configured to be run locally in a
shell, locally in a docker container, and in a docker container in Centos CI.
The tests can be run against a local or remove server by specifying the
server's URL as an environment variable.

## Prerequisities

It is possible to use geckodriver or chromedrier. To install chromedrier on
Fedora run the following command:


```
dnf install chromedriver
```

## Setup

Three environment variables need to be setup:

* `TARGET_SERVER`
* `OPENSHIFT_USERNAME`
* `OPENSHIFT_PASSWORD`
