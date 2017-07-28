Feature: Jobs debug API

  @jobs.requires_auth
  Scenario: Basic check the endpoint for analyses report output
    Given System is running
    Given Jobs debug API is running
    When I ask for analyses report for ecosystem maven
    Then I should get 200 status code

  @jobs.requires_auth
  Scenario: Basic check the endpoint for analyses report output
    Given System is running
    Given Jobs debug API is running
    When I ask for analyses report for ecosystem npm
    Then I should get 200 status code

  @jobs.requires_auth
  Scenario: Basic check the endpoint for analyses report output
    Given System is running
    Given Jobs debug API is running
    When I ask for analyses report for ecosystem pypi
    Then I should get 200 status code

