Feature: Server API

  Scenario: Check the API entry point
    Given System is running
    When I access /api/v1/
    Then I should get 200 status code
    Then I should receive JSON response containing the paths key

  Scenario: Check the /api/v1/readiness response
    Given System is running
    When I access /api/v1/readiness
    Then I should get 200 status code
    Then I should receive empty JSON response

  Scenario: Check the /api/v1/liveness response
    Given System is running
    When I wait 20 seconds
    When I access /api/v1/liveness
    Then I should get 200 status code
    Then I should receive empty JSON response

  Scenario: Check the service/state response
    Given System is running
    When I access /api/v1/system/version/
    Then I should get 200 status code
    Then I should receive JSON response containing the commit_hash key
    Then I should receive JSON response containing the committed_at key

  Scenario: Check the /api/v1/schemas response
    Given System is running
    When I access /api/v1/schemas/
    Then I should get 200 status code
    Then I should receive JSON response containing the api key

