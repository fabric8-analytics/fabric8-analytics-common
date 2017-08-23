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

  Scenario: Basic check the endpoint for analyses report output w/o authorization token
    Given System is running
    Given Jobs debug API is running
    When I ask for analyses report for ecosystem nuget
    Then I should get 401 status code

  @jobs.requires_auth
  Scenario: Basic check the endpoint for analyses report output with authorization token, maven ecosystem is tested
    Given System is running
    Given Jobs debug API is running
    When I acquire job API authorization token
    Then I should get the proper job API authorization token
    When I ask for analyses report for ecosystem maven with authorization token
    Then I should get 200 status code

  @jobs.requires_auth
  Scenario: Basic check the endpoint for analyses report output with authorization token, npm ecosystem is tested
    Given System is running
    Given Jobs debug API is running
    When I acquire job API authorization token
    Then I should get the proper job API authorization token
    When I ask for analyses report for ecosystem npm with authorization token
    Then I should get 200 status code

  @jobs.requires_auth
  Scenario: Basic check the endpoint for analyses report output with authorization token, pypi ecosystem is tested
    Given System is running
    Given Jobs debug API is running
    When I acquire job API authorization token
    Then I should get the proper job API authorization token
    When I ask for analyses report for ecosystem pypi with authorization token
    Then I should get 200 status code

  @jobs.requires_auth
  Scenario: Basic check the endpoint for analyses report output with authorization token, nuget ecosystem is tested
    Given System is running
    Given Jobs debug API is running
    When I acquire job API authorization token
    Then I should get the proper job API authorization token
    When I ask for analyses report for ecosystem nuget with authorization token
    Then I should get 200 status code

  Scenario: Basic check for the endpoint /debug/github-tokens w/o authorization key
    Given System is running
    Given Jobs debug API is running
    When I access jobs API /api/v1/debug/github-tokens
    Then I should get 401 status code

  @jobs.requires_auth
  Scenario: Basic check for the endpoint /debug/github-tokens with authorization key
    Given System is running
    Given Jobs debug API is running
    When I acquire job API authorization token
    Then I should get the proper job API authorization token
    When I access jobs API /api/v1/debug/github-tokens with authorization token
    Then I should get 200 status code

  @jobs.requires_auth
  Scenario: More check for the endpoint /debug/github-tokens with authorization key
    Given System is running
    Given Jobs debug API is running
    When I acquire job API authorization token
    Then I should get the proper job API authorization token
    When I access jobs API /api/v1/debug/github-tokens with authorization token
    Then I should get 200 status code
    Then I should see proper information about job API tokens

