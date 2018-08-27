#!/bin/bash -ex

export NOVENV=0
function prepare_venv() {
    virtualenv -p python3 venv && source venv/bin/activate && python3 "$(which pip3)" install -r requirements.txt
}

[ "$NOVENV" == "1" ] || prepare_venv || exit 1


DIR=$(pwd)
echo $DIR
pushd ../integration-tests/
PYTHONDONTWRITEBYTECODE=1 python3 "${DIR}"/taas.py
popd
