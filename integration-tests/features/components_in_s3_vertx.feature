Feature: Checks the component metadata in AWS S3 database


  @requires_s3_access @requires_bayesian_core_data_bucket @requires_bayesian_core_package_data_bucket
  Scenario: Initial check if we are able to login to AWS S3 and that the component and package bucket exists
    Given System is running
    When I connect to the AWS S3 database
    Then I should see bayesian-core-data bucket
    Then I should see bayesian-core-package-data bucket


  @requires_s3_access @requires_bayesian_core_data_bucket @requires_bayesian_core_package_data_bucket
  Scenario: Check the code metrics metadata schema for io.vertx:vertx-core (startup)
    Given System is running
    When I connect to the AWS S3 database
    Then I should see bayesian-core-data bucket
    When I read code metrics metadata for the package io.vertx:vertx-core version 3.4.0 in ecosystem maven from the AWS S3 database bucket bayesian-core-data
    Then I should find that the metadata conformns to component_code_metrics schema


  @requires_s3_access @requires_bayesian_core_data_bucket @requires_bayesian_core_package_data_bucket
  Scenario Outline: Check the code metrics metadata for all versions of the io.vertx packages
    Given System is running
    When I connect to the AWS S3 database
    Then I should see bayesian-core-data bucket
    When I read code metrics metadata for the package <package> version <version> in ecosystem maven from the AWS S3 database bucket bayesian-core-data
    Then I should find that the metadata conformns to component_code_metrics schema

     Examples: versions
     |package|version|
     |io.vertx:vertx-core|2.0.0-final|
     |io.vertx:vertx-core|2.0.1-final|
     |io.vertx:vertx-core|2.0.2-final|
     |io.vertx:vertx-core|2.1.1|
     |io.vertx:vertx-core|2.1.2|
     |io.vertx:vertx-core|2.1.5|
     |io.vertx:vertx-core|2.1.6|
     |io.vertx:vertx-core|2.1|
     |io.vertx:vertx-core|3.0.0-milestone2|
     |io.vertx:vertx-core|3.0.0-milestone5|
     |io.vertx:vertx-core|3.0.0|
     |io.vertx:vertx-core|3.1.0|
     |io.vertx:vertx-core|3.2.0|
     |io.vertx:vertx-core|3.2.1|
     |io.vertx:vertx-core|3.3.0|
     |io.vertx:vertx-core|3.3.1|
     |io.vertx:vertx-core|3.3.2|
     # |io.vertx:vertx-core|3.3.3| # disabled, see https://github.com/openshiftio/openshift.io/issues/3243
     |io.vertx:vertx-core|3.4.0.Beta1|
     |io.vertx:vertx-core|3.4.0|
     |io.vertx:vertx-core|3.4.1|
     # |io.vertx:vertx-core|3.4.2| # the worker has been disabled by Frido
     # |io.vertx:vertx-core|3.5.0| # the worker has been disabled by Frido
     # |io.vertx:vertx-core|3.5.1| # the worker has been disabled by Frido

  @requires_s3_access @requires_bayesian_core_data_bucket @requires_bayesian_core_package_data_bucket
  Scenario: Check the dependency snapshot metadata schema for io.vertx:vertx-core (startup), schema is determined automatically
    Given System is running
    When I connect to the AWS S3 database
    Then I should see bayesian-core-data bucket
    When I read dependency snapshot metadata for the package io.vertx:vertx-core version 3.5.1 in ecosystem maven from the AWS S3 database bucket bayesian-core-data
    Then I should find that the metadata conformns to component_dependency_snapshot schema


  @requires_s3_access @requires_bayesian_core_data_bucket @requires_bayesian_core_package_data_bucket
  Scenario: Check the dependency snapshot metadata schema for io.vertx:vertx-core (startup), schema is determined automatically
    Given System is running
    When I connect to the AWS S3 database
    Then I should see bayesian-core-data bucket
    When I read dependency snapshot metadata for the package io.vertx:vertx-core version 2.0.0-final in ecosystem maven from the AWS S3 database bucket bayesian-core-data
    Then I should find that the metadata conformns to component_dependency_snapshot schema


  @requires_s3_access @requires_bayesian_core_data_bucket @requires_bayesian_core_package_data_bucket
  Scenario Outline: Check the dependency snapshot metadata schema for io.vertx:vertx-core
    Given System is running
    When I connect to the AWS S3 database
    Then I should see bayesian-core-data bucket
    When I read dependency snapshot metadata for the package <package> version <version> in ecosystem maven from the AWS S3 database bucket bayesian-core-data
    Then I should find that the metadata conformns to component_dependency_snapshot schema

      Examples: versions
      |package|version|
      |io.vertx:vertx-core|2.0.0-final|
      |io.vertx:vertx-core|2.0.1-final|
      |io.vertx:vertx-core|2.0.2-final|
      |io.vertx:vertx-core|2.1.1|
      |io.vertx:vertx-core|2.1.2|
      |io.vertx:vertx-core|2.1.5|
      |io.vertx:vertx-core|2.1.6|
      |io.vertx:vertx-core|2.1|
      |io.vertx:vertx-core|3.0.0-milestone2|
      |io.vertx:vertx-core|3.0.0-milestone5|
      |io.vertx:vertx-core|3.0.0|
      |io.vertx:vertx-core|3.1.0|
      |io.vertx:vertx-core|3.2.0|
      |io.vertx:vertx-core|3.2.1|
      |io.vertx:vertx-core|3.3.0|
      |io.vertx:vertx-core|3.3.1|
      |io.vertx:vertx-core|3.3.2|
      |io.vertx:vertx-core|3.3.3| # missing data
      |io.vertx:vertx-core|3.4.0.Beta1|
      |io.vertx:vertx-core|3.4.0|
      |io.vertx:vertx-core|3.4.1|
      |io.vertx:vertx-core|3.4.2|
      |io.vertx:vertx-core|3.5.0|
      |io.vertx:vertx-core|3.5.1|


