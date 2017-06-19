#!/bin/bash -ex

function prepare_venv() {
	virtualenv -p python3 venv && source venv/bin/activate && python3 `which pip3` install -r requirements.txt
}

[ "$NOVENV" == "1" ] || prepare_venv || exit 1

export PYTHONDOCS=/
pydoc -w features/steps/common.py

# Get rid of explicit link to local file
sed -i 's-<a href=\"file:.*</a>--g' common.html

