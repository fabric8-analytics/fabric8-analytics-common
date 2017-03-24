#!/usr/bin/bash -e

oc process -f sonarqube-template.yaml | oc apply -f -

