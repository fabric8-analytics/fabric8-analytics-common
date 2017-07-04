#!/usr/bin/env groovy
@Library('github.com/msrb/cicd-pipeline-helpers') _

node('docker') {

    def image = docker.image('bayesian/coreapi-postgres')

    stage('Checkout') {
        checkout scm
    }

    stage('Build') {
        dockerCleanup()
        // build postgres image (needed later by docker-compose)
        docker.build(image.id, '--pull --no-cache postgres-docker/')
        sh "docker tag ${image.id} registry.devshift.net/${image.id}"
    }

    stage('Integration Tests') {
        dockerCleanup()
        docker.withRegistry('https://registry.devshift.net/') {
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

    if (env.BRANCH_NAME == 'master') {
        stage('Push Images') {
            docker.withRegistry('https://registry.devshift.net/') {
                image.push('latest')
                image.push(commitId)
            }
        }
    }
}
