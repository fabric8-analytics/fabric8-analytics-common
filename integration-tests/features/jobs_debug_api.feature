Feature: Jobs debug API

  Scenario: Basic check the endpoint for analyses report output
    Given System is running
    Given Jobs debug API is running
    When I ask for analyses report for ecosystem maven
    Then I should get 200 status code

  Scenario: Basic check the endpoint for analyses report output
    Given System is running
    Given Jobs debug API is running
    When I ask for analyses report for ecosystem npm
    Then I should get 200 status code

  Scenario: Basic check the endpoint for analyses report output
    Given System is running
    Given Jobs debug API is running
    When I ask for analyses report for ecosystem pypi
    Then I should get 200 status code

