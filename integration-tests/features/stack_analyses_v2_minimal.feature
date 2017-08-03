Feature: Stack analysis v2 API Minimal

  Scenario: Read outlier probability threshold value
    When I download and parse outlier probability threshold value
    Then I should have outlier probability threshold value between 0.0 and 1.0

  Scenario: Check that the API entry point
    Given System is running
    When I access /api/v1/stack-analyses-v2
    Then I should get 401 status code

  Scenario: Check that the API entry point requires authorization token
    Given System is running
    When I wait 60 seconds
    When I send Python package manifest requirements.txt to stack analysis version 2 without authorization token
    Then I should get 401 status code

  @requires_authorization_token
  Scenario: Check that the API entry point requires authorization token
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I wait 20 seconds
    When I send Python package manifest requirements.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code

  @requires_authorization_token
  Scenario: Check if the stack analysis requires authorization
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Python package manifest requirements.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish without authorization token
    Then I should get 401 status code

  @requires_authorization_token
  Scenario: Check if the stack analysis is finished
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Python package manifest requirements.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish with authorization token
    Then I should get 200 status code

  @requires_authorization_token
  Scenario: Check the integer normalization in requirements.txt for major and minor version numbers
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Python package manifest requirements_click_normalize_integer_minor.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish with authorization token
    Then I should get 200 status code
    Then I should find the value click under the path result/0/user_stack_info/analyzed_dependencies/0/package in the JSON response
    Then I should find the value 6.7 under the path result/0/user_stack_info/analyzed_dependencies/0/version in the JSON response
    When I send Python package manifest requirements_click_normalize_integer_major.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish with authorization token
    Then I should get 200 status code
    Then I should find the value click under the path result/0/user_stack_info/analyzed_dependencies/0/package in the JSON response
    Then I should find the value 6.7 under the path result/0/user_stack_info/analyzed_dependencies/0/version in the JSON response
    When I send Python package manifest requirements_click_normalize_integer_major_minor.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish with authorization token
    Then I should get 200 status code
    Then I should find the value click under the path result/0/user_stack_info/analyzed_dependencies/0/package in the JSON response
    Then I should find the value 6.7 under the path result/0/user_stack_info/analyzed_dependencies/0/version in the JSON response

