#!/bin/bash

function prepare_venv() {
    VIRTUALENV=$(which virtualenv)
    if [ $? -eq 1 ]; then
        # python36 which is in CentOS does not have virtualenv binary
        VIRTUALENV=$(which virtualenv-3)
    fi
    if [ $? -eq 1 ]; then
        # still don't have virtual environment -> use python3.6 directly
        python3.6 -m venv venv && source venv/bin/activate && python3 "$(which pip3)" install radon==3.0.1
    else
        ${VIRTUALENV} -p python3 venv && source venv/bin/activate && python3 "$(which pip3)" install radon==3.0.1
    fi
}

[ "$NOVENV" == "1" ] || prepare_venv || exit 1

radon mi -s -i venv .

if [[ "$1" == "--fail-on-error" ]]
then
    defects="$(radon mi -s -n B -i venv . | wc -l)"
    if [[ $defects -gt 0 ]]
    then
        echo "File(s) with too low maintainability index detected!"
        exit 1
    fi
fi
