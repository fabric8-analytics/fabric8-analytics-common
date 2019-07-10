#!/bin/bash -ex

if [ ! -f /var/run/docker.pid ]
then
    echo "!!! Docker service is probably not running !!!"
fi

function prepare_venv() {
	virtualenv -p python3 venv && source venv/bin/activate && python3 `which pip3` install -r requirements.txt
}

[ "$NOVENV" == "1" ] || prepare_venv || exit 1

PYTHONDONTWRITEBYTECODE=1 python3.4 `which behave` --tags=-skip --tags=-data-sanity -D dump_errors=true @feature_list.txt $@
