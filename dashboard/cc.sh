#!/bin/bash -x

function prepare_venv() {
	virtualenv -p python3 venv && source venv/bin/activate && python3 `which pip3` install -r requirements.txt
}

[ "$NOVENV" == "1" ] || prepare_venv || exit 1

python3 -B src/cc.py $@
links -width 125 -dump coverage2txt.html | sed 's/^[ \t]*//;s/[ \t]*$//' > coverage2.txt
