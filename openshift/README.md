# Openshift green field deployment of fabric8-analytics services

Config map and secrets are generated from the configuration stored in environment variables.

## Configure fabric8-analytics services
All configuration for the deployment script resides in env.sh.
To configure your developemnt deployment copy env-template.sh

`cp env-template.sh env.sh`

Update variables with your AWS,Openshift and Github credentials.

## Deploy fabric8-analytics services
Just run the deploy script and enjoy!

`$./deploy.sh`
