#!/bin/bash

# script that makes a local clone of all relevant Fabric8 repositories
# the content of repositories are to be used to generate dashboard

REPO_URL_PREFIX="https://github.com/fabric8-analytics/"

REPOSITORIES="
fabric8-analytics-common
fabric8-analytics-data-model
fabric8-analytics-jobs
fabric8-analytics-license-analysis
fabric8-analytics-recommender
fabric8-analytics-server
fabric8-analytics-stack-analysis
fabric8-analytics-tagger
fabric8-analytics-worker"

for repository in $REPOSITORIES
do
    echo $repository
    if [ -d $repository ]
    then
        echo "Pulling changes into $repository"
        pushd $repository
        git pull
        popd
    else
        repo_url="${REPO_URL_PREFIX}${repository}.git"
        echo "Cloning from $repo_url"
        git clone $repo_url
    fi
    echo $repository
done

