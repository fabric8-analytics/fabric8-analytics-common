set -ex

export CICO_API_KEY=$(cat ~/duffy.key )

# get node
n=1
while true
do
    cico_output=$(cico node get -f value -c ip_address -c comment)
        if [ $? -eq 0 ]; then
            read CICO_hostname CICO_ssid <<< $cico_output
            if  [ ! -z "$CICO_hostname" ]; then
                # we got hostname from cico
                break
            fi
            echo "'cico node get' succeed, but can't get hostname from output"
        fi
        if [ $n -gt 15 ]; then
            # give up after 15 tries
            echo "giving up on 'cico node get'"
            exit 1
        fi
        echo "'cico node get' failed, trying again in 60s ($n/15)"
        n=$[$n+1]
        sleep 60
done
echo 'Using Host' $CICO_hostname

cp ~/cico-tools/env-toolkit .
./env-toolkit dump -f integration-tests/jenkins-env.json
env > integration-tests/jenkins-env

gc() {{
    rtn_code=$?
    cico node done $CICO_ssid || :
    exit $rtn_code
}}
trap gc EXIT SIGINT
set -e

# Run E2E tests
sshopts="-t -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -l root"
ssh_cmd="ssh $sshopts $CICO_hostname"
$ssh_cmd yum -y install rsync
rsync -e "ssh $sshopts" -Ha $(pwd)/ $CICO_hostname:payload-tests
$ssh_cmd -t "cd payload-tests/integration-tests && /bin/bash cico_run_tests.sh"
