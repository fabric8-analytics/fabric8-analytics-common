#!/bin/bash -ex

docker-compose -f docker-compose.yml -f docker-compose.volumes.yml $@

