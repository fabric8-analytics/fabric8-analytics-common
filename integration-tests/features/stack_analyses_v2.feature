Feature: Stack analysis v2 API

  Scenario: Check that the API entry point
    Given System is running
    When I access /api/stack-analyses-v2
    Then I should get 404 status code

  Scenario: Check that the API entry point accepts manifest
    Given System is running
    When I wait 20 seconds
    When I send Python package manifest requirements.txt to stack analysis version 2
    Then I should get 200 status code

  Scenario: Check that the stack analysis response
    Given System is running
    When I send Python package manifest requirements.txt to stack analysis version 2
    Then I should get 200 status code
    Then I should receive JSON response containing the status key
    Then I should receive JSON response containing the id key
    Then I should receive JSON response containing the submitted_at key
    Then I should receive JSON response with the status key set to success
    Then I should receive JSON response with the correct id

