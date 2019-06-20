#!/bin/bash -ex

function prepare_venv() {
	virtualenv -p python3 venv && source venv/bin/activate && python3 `which pip3` install -r requirements.txt
}

[ "$NOVENV" == "1" ] || prepare_venv || exit 1

export VS_CODE_VERSION=1.32
PYTHONDONTWRITEBYTECODE=1 python3 `which behave` --tags=-skip -D dump_errors=true @feature_list.txt $@
