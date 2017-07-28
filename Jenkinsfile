#!/usr/bin/env groovy
@Library('github.com/msrb/cicd-pipeline-helpers') _

def apiUrl = 'http://bayesian-api-bayesian-preview.b6ff.rh-idev.openshiftapps.com'
def jobsApiUrl = 'http://bayesian-jobs-bayesian-preview.b6ff.rh-idev.openshiftapps.com'
def anityaApiUrl = 'not-used'

node('docker') {

    def image = docker.image('bayesian/coreapi-postgres')

    stage('Checkout') {
        checkout scm
    }

    stage('Integration Tests') {
        if (params.runOnOpenShift) {
            dir('integration-tests') {
                timeout(10) {
                    withEnv(["F8A_API_URL=${apiUrl}", "F8A_JOB_API_URL=${jobsApiUrl}", "F8A_ANITYA_API_URL=${anityaApiUrl}"]) {
                        sh './runtest.sh --tags=-jobs.requires_auth'
                    }
                }
            }
        } else {
            dockerCleanup()
            docker.build(image.id, '--pull --no-cache postgres-docker/')
            sh "docker tag ${image.id} registry.devshift.net/${image.id}"
            docker.withRegistry('https://registry.devshift.net/') {
                docker.image('bayesian/bayesian-api').pull()
                docker.image('bayesian/cucos-worker').pull()
                docker.image('bayesian/coreapi-jobs').pull()
                docker.image('bayesian/coreapi-pgbouncer').pull()
                docker.image('bayesian/data-model-importer').pull()
                docker.image('bayesian/cvedb-s3-dump').pull()
                docker.image('bayesian/anitya-server').pull()
                docker.image('bayesian/gremlin').pull()
            }

            dir('integration-tests') {
                timeout(10) {
                    sh './runtest.sh'
                }
            }

            if (env.BRANCH_NAME == 'master') {
                stage('Push Images') {
                    docker.withRegistry('https://registry.devshift.net/') {
                        image.push('latest')
                    }
                }
            }
        }
    }
}

