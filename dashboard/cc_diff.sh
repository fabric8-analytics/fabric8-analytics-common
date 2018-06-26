REPOS="f8a-server-backbone fabric8-analytics-data-model fabric8-analytics-jobs fabric8-analytics-license-analysis fabric8-analytics-server fabric8-analytics-stack-analysis fabric8-analytics-tagger fabric8-analytics-worker fabric8-gemini-server fabric8-analytics-api-gateway fabric8-analytics-auth fabric8-analytics-nvd-toolkit fabric8-analytics-version-comparator fabric8-analytics-ingestion fabric8-analytics-jenkins-plugin fabric8-analytics-npm-insights"

for repo in $REPOS
do
    echo ${repo}
    sdiff -w 210 ${repo}.coverage.0.txt ${repo}.coverage.1.txt > ${repo}.coverage.diff.txt
done

