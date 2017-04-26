#!/usr/bin/env groovy
@Library('github.com/msrb/cicd-pipeline-helpers')

node('docker') {

    stage('Checkout') {
        checkout scm
    }

    stage('Integration Tests') {
        dockerCleanup()
        docker.withRegistry('https://docker-registry.usersys.redhat.com/') {
            docker.image('bayesian/bayesian-api').pull()
            docker.image('bayesian/cucos-worker').pull()
            docker.image('bayesian/coreapi-downstream-data-import').pull()
            docker.image('bayesian/coreapi-jobs').pull()
            docker.image('bayesian/coreapi-pgbouncer').pull()
        }

        dir('integration-tests') {
            timeout(30) {
                sh './runtest.sh'
            }
        }
    }
}
