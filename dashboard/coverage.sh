#!/bin/bash -x

REPOS="f8a-server-backbone fabric8-analytics-data-model fabric8-analytics-jobs fabric8-analytics-license-analysis fabric8-analytics-server fabric8-analytics-stack-analysis fabric8-analytics-tagger fabric8-analytics-worker fabric8-gemini-server fabric8-analytics-api-gateway fabric8-analytics-auth fabric8-analytics-nvd-toolkit fabric8-analytics-version-comparator fabric8-analytics-ingestion fabric8-analytics-jenkins-plugin fabric8-analytics-npm-insights f8a-hpf-insights fabric8-analytics-notification-scheduler cvejob fabric8-analytics-utils fabric8-analytics-github-refresh-cronjob fabric8-analytics-release-monitor f8a-golang-insights f8a-pypi-insights fabric8-analytics-github-events-monitor f8a-stacks-report fabric8-analytics-rudra victimsdb-lib"

for repo in $REPOS
do
    echo ${repo}
    cp ${repo}.coverage.1.txt ${repo}.coverage.0.txt
    cp ${repo}.coverage.txt ${repo}.coverage.1.txt
done

function prepare_venv_() {
	virtualenv -p python3 venv && source venv/bin/activate && python3 `which pip3` install -r requirements.txt
}

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
	# ${PYTHON} -m venv "venv" && source venv/bin/activate
        #${VIRTUALENV} -p python3 venv && source venv/bin/activate && python3 `which pip3` install pycodestyle
}

[ "$NOVENV" == "1" ] || prepare_venv || exit 1

python3 -B src/cc.py $@
links -width 125 -dump coverage2txt.html | sed 's/^[ \t]*//;s/[ \t]*$//' > coverage.txt

for repo in $REPOS
do
    echo ${repo}
    sdiff -w 210 ${repo}.coverage.0.txt ${repo}.coverage.1.txt > ${repo}.coverage.diff.txt
done
