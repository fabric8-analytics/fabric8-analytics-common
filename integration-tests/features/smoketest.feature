Feature: Smoke test

  @smoketest @production
  Scenario: Check the API entry point
    Given System is running
    When I access /api/v1/
    Then I should get 200 status code

  @smoketest @production
  Scenario: Check the /system/version entry point
    Given System is running
    When I access /api/v1/system/version/
    Then I should get 200 status code
     And I should receive JSON response containing the commit_hash key
     And I should receive JSON response containing the committed_at key
     And I should find the correct commit hash in the JSON response
     And I should find the correct committed at timestamp in the JSON response

  @smoketest @production
  Scenario: Check the jobs API entry point
    Given System is running
    When I access /api/v1/readiness
    Then I should get 200 status code

  @smoketest @production
  Scenario: Check the jobs API entry point
    Given System is running
    When I access jobs API /api/v1
    Then I should get 200 status code

  @smoketest @production
  Scenario: Check the jobs API entry point
    Given System is running
    When I access jobs API /api/v1/readiness
    Then I should get 200 status code

  @smoketest @production
  Scenario: Check the jobs API entry point
    Given System is running
    When I access jobs API /api/v1/liveness
    Then I should get 200 status code

  @jobs.requires_auth
  Scenario: Check the jobs API entry point
    Given System is running
    When I access jobs API /api/v1/service/state
    Then I should get 200 status code

  @smoketest @production
  Scenario: Basic check the endpoint for analyses report output w/o authorization token
    Given System is running
    Given Jobs debug API is running
    When I ask for analyses report for ecosystem maven
    Then I should get 401 status code

  @smoketest @production
  Scenario: Basic check the endpoint for analyses report output w/o authorization token
    Given System is running
    Given Jobs debug API is running
    When I ask for analyses report for ecosystem npm
    Then I should get 401 status code

  @smoketest @production
  Scenario: Basic check the endpoint for analyses report output w/o authorization token
    Given System is running
    Given Jobs debug API is running
    When I ask for analyses report for ecosystem pypi
    Then I should get 401 status code

  @smoketest @production
  Scenario: Basic check the endpoint for analyses report output w/o authorization token
    Given System is running
    Given Jobs debug API is running
    When I ask for analyses report for ecosystem nuget
    Then I should get 401 status code

