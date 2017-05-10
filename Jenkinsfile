#!/usr/bin/env groovy
@Library('github.com/msrb/cicd-pipeline-helpers') _

node('docker') {

    stage('Checkout') {
        checkout scm
    }

    stage('Integration Tests') {
        // git url: 'https://gitlab.cee.redhat.com/jpopelka/cloud-deployer', branch: 'delete-resources', credentialsId: 'baytemp-ci-gh'
        // get aws creds.* for cloud-deployer

        //sh '''
        //    suffix=$(cat /dev/urandom | tr -cd 'a-z' | head -c 8)
        //    echo $suffix
        //    '''
        //export TESTS_DEPLOYMENT_PREFIX="tests-${suffix}"
        //export CLOUD_DEPLOYER_PATH=../../../cloud-deployer/

        //oc --context=tests new-project $TESTS_DEPLOYMENT_PREFIX

        //openshift/cloud-deploy/deploy.sh

        //while oc --context=tests get pod integration-tests -o=custom-columns=STATUS:.status.phase | grep Running;
        //do
        //    sleep 5
        //done

        //oc --context=tests logs integration-tests
        //oc --context=tests delete project $TESTS_DEPLOYMENT_PREFIX
        //cloud-deployer/delete-aws-resources.sh $TESTS_DEPLOYMENT_PREFIX
    }
}

