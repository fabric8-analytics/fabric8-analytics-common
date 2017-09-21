Feature: Regression tests

  @requires_authorization_token
  Scenario: Check the issue #847 (https://github.com/openshiftio/openshift.io/issues/847)
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Python package manifest requirements_click_compatible_with_0_7.txt to stack analysis with authorization token
    Then I should get 200 status code
    When I wait for stack analysis to finish with authorization token
    Then I should get 200 status code
    Then I should find the value click under the path result/0/user_stack_info/analyzed_dependencies/0/package in the JSON response
    Then I should find the value 0.7 under the path result/0/user_stack_info/analyzed_dependencies/0/version in the JSON response

  @requires_authorization_token
  Scenario: Check the issue #848 (https://github.com/openshiftio/openshift.io/issues/848)
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Python package manifest requirements_click_0_star.txt to stack analysis with authorization token
    Then I should get 200 status code
    When I wait for stack analysis to finish with authorization token
    Then I should get 200 status code
    Then I should find the value click under the path result/0/user_stack_info/analyzed_dependencies/0/package in the JSON response
    Then I should find the value 0.7 under the path result/0/user_stack_info/analyzed_dependencies/0/version in the JSON response

