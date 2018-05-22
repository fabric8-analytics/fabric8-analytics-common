Feature: Checks the package metadata in AWS S3 database

  @requires_s3_access @requires_bayesian_core_package_data_bucket
  Scenario: Initial check if we are able to login to AWS S3 and that the component and package bucket exists
    Given System is running
    When I connect to the AWS S3 database
    Then I should see bayesian-core-package-data bucket


 @requires_s3_access @jobs.requires_auth @requires_bayesian_core_package_data_bucket
 Scenario: Check that the component toplevel metadata are updated properly after analysis: simple package for PyPi
   Given System is running
   When I connect to the AWS S3 database
   Then I should see bayesian-core-package-data bucket
   When I acquire job API authorization token
   Then I should get the proper job API authorization token
   When I post a job metadata job_flow_data/pypi/factorial.json with state running using authorization token
   Then I should get 201 status code
   When I wait for new toplevel data for the package factorial in ecosystem pypi in the AWS S3 database bucket bayesian-core-package-data
   Then I should find the correct package toplevel metadata for package factorial from ecosystem pypi

 @requires_s3_access @jobs.requires_auth @requires_bayesian_core_package_data_bucket
 Scenario: Check that the component toplevel metadata are updated properly simple package for PyPi
   Given System is running
   When I connect to the AWS S3 database
   Then I should see bayesian-core-package-data bucket
   When I acquire job API authorization token
   Then I should get the proper job API authorization token
   When I post a job metadata job_flow_data/pypi/factorial1.json with state running using authorization token
   Then I should get 201 status code
   When I wait for new toplevel data for the package factorial1 in ecosystem pypi in the AWS S3 database bucket bayesian-core-package-data
   Then I should find the correct package toplevel metadata for package factorial1 from ecosystem pypi
