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

  Scenario: Check the stack analysis output
    When I send Python package manifest requirements.txt to stack analysis version 2
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish
    Then I should get 200 status code
    Then I should receive JSON response containing the started_at key
    Then I should receive JSON response containing the finished_at key
    Then I should receive JSON response containing the request_id key
    Then I should find the value requirements.txt under the path result/0/manifest_name in the JSON response
    Then I should find the value 0 under the path result/0/user_stack_info/total_licenses in the JSON response
    Then I should find the value 0 under the path result/0/user_stack_info/unknown_dependencies_count in the JSON response
    Then I should find the value pypi under the path result/0/user_stack_info/ecosystem in the JSON response
