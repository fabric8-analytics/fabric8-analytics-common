#Template with default values used to configure dev deployment of fabric8-analytics

#Openshift configuration
export OC_URI='dev.rdu2c.fabric8.io:8443'
# Your dev cluster username
export OC_USERNAME='not-set'
# Your dev cluster password
export OC_PASSWD='not-set'
export OC_PROJECT="${OC_USERNAME}-fabric8-analytics"

#AWS credentials
export AWS_ACCESS_KEY_ID='not-set'
export AWS_SECRET_ACCESS_KEY='not-set'
export AWS_DEFAULT_REGION='us-east-1'

#GitHub
# Comma-separated list of tokens for talking to GitHub API
#   You can generate a token here: https://github.com/settings/tokens
export GITHUB_API_TOKENS='not-set'
# Create a new GitHub OAuth App here: https://github.com/settings/developers
# You will need to provide homepage and callback URL; for the dev cluster, use following values (replace OC_USERNAME):
# "Homepage URL" is "http://bayesian-jobs-${OC_USERNAME}-fabric8-analytics.dev.rdu2c.fabric8.io/"
# "Authorization callback URL" is "http://bayesian-jobs-${OC_USERNAME}-fabric8-analytics.dev.rdu2c.fabric8.io/api/v1/authorized"
# In return, you'll get GITHUB_OAUTH_CONSUMER_KEY and GITHUB_OAUTH_CONSUMER_SECRET from GitHub.
#   Client ID is GITHUB_OAUTH_CONSUMER_KEY
#   Client Secret is GITHUB_OAUTH_CONSUMER_SECRET
export GITHUB_OAUTH_CONSUMER_KEY='not-set'
export GITHUB_OAUTH_CONSUMER_SECRET='not-set'

export KEYCLOAK_URL='https://sso.openshift.io'
export FLASK_APP_SECRET_KEY='notsosecret'

#AWS RDS configuration variables are use to provision RDS instance
export RDS_ENDPOINT=''
export RDS_INSTANCE_NAME="${OC_USERNAME}-bayesiandb"
export RDS_INSTANCE_CLASS='db.t2.micro'
export RDS_DBNAME='postgres'
export RDS_DBADMIN='coreapi'
export RDS_STORAGE=5
export RDS_PASSWORD=''
export RDS_SUBNET_GROUP_NAME='dv peering az'
export RDS_ARN='not-set'

#Integration tests settings
export F8A_API_URL='not-set'
export F8A_JOB_API_URL='not-set'
export RECOMMENDER_API_TOKEN='not-set'

export DEPLOYMENT_PREFIX=${DEPLOYMENT_PREFIX:-${OC_USERNAME}}
