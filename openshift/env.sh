# This is temporary file
# All env variables will be exported in users shell configuration.
# After there is documentation on how to do so.

export AWS_ACCESS_KEY_ID='Not set'
export AWS_SECRET_ACCESS_KEY='Not set'
export GITHUB_API_TOKENS='Not set'
export GITHUB_OAUTH_CONSUMER_KEY='Not set'
export GITHUB_OAUTH_CONSUMER_SECRET='Not set'
export FLASK_APP_SECRET_KEY='Not set'
export RDS_ENDPOINT='Not set'
export RDS_PASSWORD="$(date +%s | sha256sum | base64 | head -c 32 ;)"
export KEYCLOAK_URL='Not set'

export OC_URI='192.168.42.71:8443'
export OC_USERNAME='developer'
export OC_PASSWD='developer'

export OC_PROJECT=$(whoami)'-greenfield-test-1'
