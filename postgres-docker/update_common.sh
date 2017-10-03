#!/bin/bash
curl -o common.sh https://raw.githubusercontent.com/sclorg/postgresql-container/master/9.4/root/usr/share/container-scripts/postgresql/common.sh && patch < multiple_dbs.patch

