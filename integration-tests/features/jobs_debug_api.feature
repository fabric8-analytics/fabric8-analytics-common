Feature: Jobs debug API

  Scenario: Basic check the endpoint for analyses report output w/o authorization token
    Given System is running
    Given Jobs debug API is running
    When I ask for analyses report for ecosystem maven
    Then I should get 401 status code

  Scenario: Basic check the endpoint for analyses report output w/o authorization token
    Given System is running
    Given Jobs debug API is running
    When I ask for analyses report for ecosystem npm
    Then I should get 401 status code

  Scenario: Basic check the endpoint for analyses report output w/o authorization token
    Given System is running
    Given Jobs debug API is running
    When I ask for analyses report for ecosystem pypi
    Then I should get 401 status code

  @jobs.requires_auth
  Scenario: Basic check the endpoint for analyses report output with authorization token
    Given System is running
    Given Jobs debug API is running
    When I acquire job API authorization token
    Then I should get the proper job API authorization token
    When I ask for analyses report for ecosystem maven with authorization token
    Then I should get 200 status code

  @jobs.requires_auth
  Scenario: Basic check the endpoint for analyses report output with authorization token
    Given System is running
    Given Jobs debug API is running
    When I acquire job API authorization token
    Then I should get the proper job API authorization token
    When I ask for analyses report for ecosystem npm with authorization token
    Then I should get 200 status code

  @jobs.requires_auth
  Scenario: Basic check the endpoint for analyses report output with authorization token
    Given System is running
    Given Jobs debug API is running
    When I acquire job API authorization token
    Then I should get the proper job API authorization token
    When I ask for analyses report for ecosystem pypi with authorization token
    Then I should get 200 status code

