Feature: Checks the component metadata in AWS S3 database

  @requires_s3_access
  Scenario: Initial check if we are able to login to AWS S3 and that the component and package bucket exists
    Given System is running
    When I connect to the AWS S3 database
    Then I should see bayesian-core-data bucket
    Then I should see bayesian-core-package-data bucket

  @requires_s3_access
  Scenario: Initial check if we are able to login to AWS S3 and read package toplevel metadata
    Given System is running
    When I connect to the AWS S3 database
    Then I should see bayesian-core-package-data bucket
    When I read package toplevel metadata for the package clojure_py in ecosystem pypi from the AWS S3 database bucket bayesian-core-package-data
    Then I should find the correct package toplevel metadata for package clojure_py from ecosystem pypi

  @requires_s3_access
  Scenario: Initial check if we are able to login to AWS S3 and read component toplevel metadata
    Given System is running
    When I connect to the AWS S3 database
    Then I should see bayesian-core-data bucket
    When I read component toplevel metadata for the package clojure_py version 0.2.4 in ecosystem pypi from the AWS S3 database bucket bayesian-core-data
    Then I should find the correct component toplevel metadata for package clojure_py version 0.2.4 ecosystem pypi with latest version 0.2.4

  @requires_s3_access
  Scenario: Check that the component toplevel metadata are updated properly
    Given System is running
    When I wait 30 seconds
    When I connect to the AWS S3 database
    Then I should see bayesian-core-data bucket
    When I acquire job API authorization token
    Then I should get the proper job API authorization token
    When I post a job metadata job_pypi_clojure_py.json with state running using authorization token
    Then I should get 201 status code
    When I wait for new toplevel data for the package clojure_py version 0.2.4 in ecosystem pypi in the AWS S3 database bucket bayesian-core-data
    Then I should find the correct component toplevel metadata for package clojure_py version 0.2.4 ecosystem pypi with latest version 0.2.4

  @requires_s3_access
  Scenario: Check that the analysis had really been performed based on timestamps tests
    Given System is running
    When I wait 30 seconds
    When I connect to the AWS S3 database
    Then I should see bayesian-core-data bucket
    When I acquire job API authorization token
    Then I should get the proper job API authorization token
    When I read component toplevel metadata for the package clojure_py version 0.2.4 in ecosystem pypi from the AWS S3 database bucket bayesian-core-data
    Then I should find the correct component toplevel metadata for package clojure_py version 0.2.4 ecosystem pypi with latest version 0.2.4
    When I remember timestamps from the last component toplevel metadata
     And I post a job metadata job_pypi_clojure_py.json with state running using authorization token
    Then I should get 201 status code
    When I wait for new toplevel data for the package clojure_py version 0.2.4 in ecosystem pypi in the AWS S3 database bucket bayesian-core-data
    Then I should find that timestamps from current toplevel metadata are newer than remembered timestamps

