Feature: Checks the component metadata in AWS S3 database

  @requires_s3_access
  Scenario: Initial check if we are able to login to AWS S3 and read job toplevel metadata
    Given System is running
    When I connect to the AWS S3 database
    Then I should see bayesian-core-data bucket
    When I read job toplevel data for the package clojure_py version 0.2.4 in ecosystem pypi from the AWS S3 database bucket bayesian-core-data
    Then I should find the correct job toplevel metadata for package clojure_py version 0.2.4 ecosystem pypi with latest version 0.2.4
 
  @requires_s3_access
  Scenario: Check that the metadata for job toplevel data are updated properly
    Given System is running
    When I wait 30 seconds
    When I connect to the AWS S3 database
    Then I should see bayesian-core-data bucket
    When I acquire job API authorization token
    Then I should get the proper job API authorization token
    When I post a job metadata job_pypi_clojure_py.json with state running using authorization token
    Then I should get 201 status code
    When I wait for new toplevel data for the package clojure_py version 0.2.4 in ecosystem pypi in the AWS S3 database bucket bayesian-core-data
    Then I should find the correct job toplevel metadata for package clojure_py version 0.2.4 ecosystem pypi with latest version 0.2.4
 
  @requires_s3_access
  Scenario: Check that the analysis had really been performed based on timestamps tests
    Given System is running
    When I wait 30 seconds
    When I connect to the AWS S3 database
    Then I should see bayesian-core-data bucket
    When I acquire job API authorization token
    Then I should get the proper job API authorization token
    When I read job toplevel data for the package clojure_py version 0.2.4 in ecosystem pypi from the AWS S3 database bucket bayesian-core-data
    Then I should find the correct job toplevel metadata for package clojure_py version 0.2.4 ecosystem pypi with latest version 0.2.4
    When I remember timestamps from the last job toplevel data
     And I post a job metadata job_pypi_clojure_py.json with state running using authorization token
    Then I should get 201 status code
    When I wait for new toplevel data for the package clojure_py version 0.2.4 in ecosystem pypi in the AWS S3 database bucket bayesian-core-data
    Then I should find that timestamps from current toplevel metadata are newer than remembered timestamps

