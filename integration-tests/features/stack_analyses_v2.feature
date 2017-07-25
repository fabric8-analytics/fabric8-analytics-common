Feature: Stack analysis v2 API

  Scenario: Check that the API entry point
    Given System is running
    When I access /api/stack-analyses-v2
    Then I should get 404 status code

  Scenario: Check that the API entry point requires authorization token
    Given System is running
    When I wait 60 seconds
    When I send Python package manifest requirements.txt to stack analysis version 2 without authorization token
    Then I should get 401 status code

  Scenario: Check that the API entry point requires authorization token
    Given System is running
    When I generate authorization token from the private key private_key.pem
    Then I should get the proper authorization token
    When I wait 20 seconds
    When I send Python package manifest requirements.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code

  Scenario: Check that the stack analysis response
    Given System is running
    When I generate authorization token from the private key private_key.pem
    Then I should get the proper authorization token
    When I send Python package manifest requirements.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code
    Then I should receive JSON response containing the status key
    Then I should receive JSON response containing the id key
    Then I should receive JSON response containing the submitted_at key
    Then I should receive JSON response with the status key set to success
    Then I should receive JSON response with the correct id
    Then I should receive JSON response with the correct timestamp in attribute submitted_at

  Scenario: Check if the stack analysis requires authorization
    Given System is running
    When I generate authorization token from the private key private_key.pem
    Then I should get the proper authorization token
    When I send Python package manifest requirements.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish without authorization token
    Then I should get 401 status code

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

  Scenario: Check the integer normalization in requirements.txt for major and minor version numbers
    When I send Python package manifest requirements_click_normalize_integer_minor.txt to stack analysis version 2
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish
    Then I should get 200 status code
    Then I should find the value click under the path result/0/user_stack_info/analyzed_dependencies/0/package in the JSON response
    Then I should find the value 6.7 under the path result/0/user_stack_info/analyzed_dependencies/0/version in the JSON response
    When I send Python package manifest requirements_click_normalize_integer_major.txt to stack analysis version 2
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish
    Then I should get 200 status code
    Then I should find the value click under the path result/0/user_stack_info/analyzed_dependencies/0/package in the JSON response
    Then I should find the value 6.7 under the path result/0/user_stack_info/analyzed_dependencies/0/version in the JSON response
    When I send Python package manifest requirements_click_normalize_integer_major_minor.txt to stack analysis version 2
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish
    Then I should get 200 status code
    Then I should find the value click under the path result/0/user_stack_info/analyzed_dependencies/0/package in the JSON response
    Then I should find the value 6.7 under the path result/0/user_stack_info/analyzed_dependencies/0/version in the JSON response

