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
    Then I should receive JSON response with the correct timestamp in attribute submitted_at

  Scenario: Check if the stack analysis is finished
    Given System is running
    When I send Python package manifest requirements.txt to stack analysis version 2
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish
    Then I should get 200 status code

  Scenario: Check the stack analysis timestamp attributes
    When I send Python package manifest requirements.txt to stack analysis version 2
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish
    Then I should get 200 status code
    Then I should find analyzed dependency named click with version 6.7 in the stack analysis
    Then I should receive JSON response with the correct timestamp in attribute started_at
    Then I should receive JSON response with the correct timestamp in attribute finished_at
    Then I should find proper timestamp under the path result/0/_audit/started_at
    Then I should find proper timestamp under the path result/0/_audit/ended_at
