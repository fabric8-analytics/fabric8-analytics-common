#!/bin/bash -ex

if [ ! -f /var/run/docker.pid ]
then
    echo "!!! Docker service is probably not running !!!"
fi

function prepare_venv() {
	virtualenv -p python3.6 venv && source venv/bin/activate && python3.6 `which pip3` install -r requirements.txt
}

[ "$NOVENV" == "1" ] || prepare_venv || exit 1


export THREE_SCALE_PREVIEW_USER_KEY=""
export F8A_API_V2_URL=""



locust -f locustfile.py --host=http://localhost:8089 

