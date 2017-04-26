# Deploying Bayesian with cloud-deployer

* dnf/yum install awscli ntpdate expect
* git clone cloud-deployer from internal GitLab
* CLOUD_DEPLOYER_PATH=\<path to cloned repo\> AWS_ACCESS_KEY_ID='...' AWS_SECRET_ACCESS_KEY='...' ./deploy.sh

## Customizing

* Different AWS access/secret keys for resources (RDS, S3, SQS): Can be specified in `creds.*` files.
* Different password for database: If you don't want to generate new password, set `RDS_DBPASS` in `creds.rds` to your password.
