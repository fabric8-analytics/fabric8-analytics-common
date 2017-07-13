Feature: Jobs API

  Scenario: Check that the API entry point
    Given System is running
    When I access /api/stack-analyses
    Then I should get 404 status code

  Scenario: Check that the API entry point
    Given System is running
    When I wait 10 seconds
    Then I wait 10 seconds
    When I send NPM package manifest wisp-prettyprinted.json to stack analysis
    Then I should get 200 status code
    Then I should receive JSON response containing the status key
    Then I should receive JSON response containing the id key
    Then I should receive JSON response containing the submitted_at key

