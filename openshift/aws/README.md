# Allocating AWS resources

fabric8-analytics depends on Amazon RDS (and other AWS resources). You can use AWS CLI to create a new instance, or you can use [cloud-deployer](#using-cloud-deployer) tool (internal).

[`../secrets-template.yaml`](../secrets-template.yaml) expects endpoint of the RDS instance and password as one of its parameters.


## Using cloud-deployer

* dnf/yum install awscli ntpdate expect
* git clone cloud-deployer from GitLab (internal)
* CLOUD_DEPLOYER_PATH=\<path to cloned repo\> AWS_ACCESS_KEY_ID='...' AWS_SECRET_ACCESS_KEY='...' ./allocate-aws-resources.sh

Find the newly generated secrets in `values.${timestamp}` file.


## Customizing

* Different AWS access/secret keys for resources (RDS, S3, SQS): Can be specified in `creds.*` files.
* Different password for database: If you don't want to generate new password, set `RDS_DBPASS` in `creds.rds` to your password.

