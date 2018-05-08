Feature: Checks the package metadata in AWS S3 database


  @requires_s3_access @requires_bayesian_core_data_bucket @requires_bayesian_core_package_data_bucket
  Scenario: Initial check if we are able to login to AWS S3 and that the component and package bucket exists
    Given System is running
    When I connect to the AWS S3 database
    Then I should see bayesian-core-data bucket
    Then I should see bayesian-core-package-data bucket


  @requires_s3_access @requires_bayesian_core_data_bucket @requires_bayesian_core_package_data_bucket
  Scenario: Check the package toplevel metadata schema for io.vertx:vertx-core package (startup)
    Given System is running
    When I connect to the AWS S3 database
    Then I should see bayesian-core-package-data bucket
    When I read package toplevel metadata for the package io.vertx:vertx-core in ecosystem maven from the AWS S3 database bucket bayesian-core-package-data
    Then I should find that the metadata conformns to package_toplevel schema


  @requires_s3_access @requires_bayesian_core_data_bucket @requires_bayesian_core_package_data_bucket
  Scenario Outline: Check the toplevel metadata for all io.vertx packages
    Given System is running
    When I connect to the AWS S3 database
    Then I should see bayesian-core-package-data bucket
    When I read package toplevel metadata for the package <package> in ecosystem maven from the AWS S3 database bucket bayesian-core-package-data
    Then I should find that the metadata conformns to package_toplevel schema

     Examples: packages
     |package|
     |io.vertx:vertx-core|


  @requires_s3_access @requires_bayesian_core_data_bucket @requires_bayesian_core_package_data_bucket
  Scenario: Check the git stats metadata schema for io.vertx:vertx-core package (startup)
    Given System is running
    When I connect to the AWS S3 database
    Then I should see bayesian-core-package-data bucket
    When I read git stats metadata for the package io.vertx:vertx-core in ecosystem maven from the AWS S3 database bucket bayesian-core-package-data
    Then I should find that the metadata conformns to package_git_stats schema


  @requires_s3_access @requires_bayesian_core_data_bucket @requires_bayesian_core_package_data_bucket
  Scenario Outline: Check the git stats metadata for all io.vertx packages
    Given System is running
    When I connect to the AWS S3 database
    Then I should see bayesian-core-package-data bucket
    When I read git stats metadata for the package <package> in ecosystem maven from the AWS S3 database bucket bayesian-core-package-data
    Then I should find that the metadata conformns to package_git_stats schema

     Examples: packages
     |package|
     |io.vertx:vertx-core|


  @requires_s3_access @requires_bayesian_core_data_bucket @requires_bayesian_core_package_data_bucket
  Scenario: Check the github details metadata schema for io.vertx:vertx-core package (startup)
    Given System is running
    When I connect to the AWS S3 database
    Then I should see bayesian-core-package-data bucket
    When I read github details metadata for the package io.vertx:vertx-core in ecosystem maven from the AWS S3 database bucket bayesian-core-package-data
    Then I should find that the metadata conformns to package_github_details schema


  @requires_s3_access @requires_bayesian_core_data_bucket @requires_bayesian_core_package_data_bucket
  Scenario Outline: Check the toplevel metadata for all io.vertx packages
    Given System is running
    When I connect to the AWS S3 database
    Then I should see bayesian-core-package-data bucket
    When I read github details metadata for the package <package> in ecosystem maven from the AWS S3 database bucket bayesian-core-package-data
    Then I should find that the metadata conformns to package_github_details schema

     Examples: packages
     |package|
     |io.vertx:vertx-core|


