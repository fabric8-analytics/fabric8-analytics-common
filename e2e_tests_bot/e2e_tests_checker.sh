#!/bin/bash -x

function prepare_venv() {
	# we want tests to run on python3.6
	printf 'checking alias `python3.6` ... ' >&2
	PYTHON=$(which python3.6 2> /dev/null)
	if [ "$?" -ne "0" ]; then
		printf "${YELLOW} NOT FOUND ${NORMAL}\n" >&2

		printf 'checking alias `python3` ... ' >&2
		PYTHON=$(which python3 2> /dev/null)

		let ec=$?
		[ "$ec" -ne "0" ] && printf "${RED} NOT FOUND ${NORMAL}\n" && return $ec
	fi

	printf "${GREEN} OK ${NORMAL}\n" >&2

	${PYTHON} -m venv "venv" && source venv/bin/activate && pip install pycodestyle -r requirements.txt
}

python3 -B src/e2e_tests_checker.py $@
