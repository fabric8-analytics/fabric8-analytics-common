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

  Scenario: Check the analyzed dependencies for newer version of click package
    When I send Python package manifest requirements_click_newest_6_7.txt to stack analysis version 2
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish
    Then I should get 200 status code
    Then I should find the value click under the path result/0/user_stack_info/analyzed_dependencies/0/package in the JSON response
    Then I should find the value 6.7 under the path result/0/user_stack_info/analyzed_dependencies/0/version in the JSON response

  Scenario: Check the analyzed dependencies for older version of click package
    When I send Python package manifest requirements_click_version_eq_5_0.txt to stack analysis version 2
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish
    Then I should get 200 status code
    Then I should find the value click under the path result/0/user_stack_info/analyzed_dependencies/0/package in the JSON response
    Then I should find the value 5.0 under the path result/0/user_stack_info/analyzed_dependencies/0/version in the JSON response

  Scenario: Check the analyzed dependencies for older version of click package with click>=5.0 in requirements
    When I send Python package manifest requirements_click_version_ge_5_0.txt to stack analysis version 2
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish
    Then I should get 200 status code
    Then I should find the value click under the path result/0/user_stack_info/analyzed_dependencies/0/package in the JSON response
    Then I should find the value 6.7 under the path result/0/user_stack_info/analyzed_dependencies/0/version in the JSON response

  Scenario: Check the analyzed dependencies for older version of click package with click>5.0 in requirements
    When I send Python package manifest requirements_click_version_gt_5_0.txt to stack analysis version 2
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish
    Then I should get 200 status code
    Then I should find the value click under the path result/0/user_stack_info/analyzed_dependencies/0/package in the JSON response
    Then I should find the value 6.7 under the path result/0/user_stack_info/analyzed_dependencies/0/version in the JSON response
