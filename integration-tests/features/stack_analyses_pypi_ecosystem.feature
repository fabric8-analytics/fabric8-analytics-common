Feature: Thorough stack analysis v3 API tests


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for newer version of click package (6.7)
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I test pypi dependencies file requirements_click_newest_6_7.txt for stack analysis from vscode
    Then I should get 200 status code
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response with the correct request_id
     And I should find analyzed dependency named click with version 6.7 in the stack analysis


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for newer version of click package (7.0)
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I test pypi dependencies file requirements_click_newest_7_0.txt for stack analysis from vscode
    Then I should get 200 status code
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response with the correct request_id
     And I should find analyzed dependency named click with version 7.0 in the stack analysis


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for exact version of click package (arbitrary equality)
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I test pypi dependencies file requirements_click_arbitrary_equality.txt for stack analysis from vscode
    Then I should get 200 status code
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response with the correct request_id
     And I should find analyzed dependency named click with version 6.7 in the stack analysis


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for older version of click package with click>=5.0 in requirements
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I test pypi dependencies file requirements_click_version_gt_5_0.txt for stack analysis from vscode
    Then I should get 200 status code
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response with the correct request_id
     And I should find analyzed dependency named click with version 7.0 in the stack analysis


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for older version (5.0) of click package
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I test pypi dependencies file requirements_click_version_eq_5_0.txt for stack analysis from vscode
    Then I should get 200 status code
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response with the correct request_id
     And I should find analyzed dependency named click with version 5.0 in the stack analysis


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for older version of click package with click>=5.0, <=6.0 in requirements
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I test pypi dependencies file requirements_click_version_ge_5_0_le_6_0.txt for stack analysis from vscode
    Then I should get 200 status code
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response with the correct request_id
     And I should find analyzed dependency named click with version 6.0 in the stack analysis
 
 
  @requires_authorization_token
  Scenario: Check the analyzed dependencies for older version of click package with click>=5.0, <6.0 in requirements
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I test pypi dependencies file requirements_click_version_ge_5_0_lt_6_0.txt for stack analysis from vscode
    Then I should get 200 status code
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response with the correct request_id
     And I should find analyzed dependency named click with version 5.1 in the stack analysis
 
 
  @requires_authorization_token
  Scenario: Check the analyzed dependencies for older version of click package with click>5.0, <6.0 in requirements
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I test pypi dependencies file requirements_click_version_gt_5_0_lt_6_0.txt for stack analysis from vscode
    Then I should get 200 status code
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response with the correct request_id
     And I should find analyzed dependency named click with version 5.1 in the stack analysis
 
 
  @requires_authorization_token
  Scenario: Check the analyzed dependencies for older version of click package with click>5.0, <=6.0 in requirements
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I test pypi dependencies file requirements_click_version_gt_5_0_le_6_0.txt for stack analysis from vscode
    Then I should get 200 status code
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response with the correct request_id
     And I should find analyzed dependency named click with version 6.0 in the stack analysis
 
 
  @requires_authorization_token
  Scenario: Check the analyzed dependencies for click 6.7.*
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I test pypi dependencies file requirements_click_6_7_star.txt for stack analysis from vscode
    Then I should get 200 status code
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response with the correct request_id
     And I should find analyzed dependency named click with version 6.7 in the stack analysis
 

  @requires_authorization_token
  Scenario: Check the integer normalization in requirements.txt for major and minor version numbers
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I test pypi dependencies file requirements_click_normalize_integer_minor.txt for stack analysis from vscode
    Then I should get 200 status code
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response with the correct request_id
     And I should find analyzed dependency named click with version 6.7 in the stack analysis
    When I test pypi dependencies file requirements_click_normalize_integer_major.txt for stack analysis from vscode
    Then I should get 200 status code
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response with the correct request_id
     And I should find analyzed dependency named click with version 6.7 in the stack analysis
    When I test pypi dependencies file requirements_click_normalize_integer_major_minor.txt for stack analysis from vscode
    Then I should get 200 status code
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response with the correct request_id
     And I should find analyzed dependency named click with version 6.7 in the stack analysis


  @requires_authorization_token
  Scenario: Check the stack analysis output
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I test pypi dependencies file requirements.txt for stack analysis from vscode
    Then I should get 200 status code
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive JSON response containing the started_at key
     And I should receive JSON response containing the finished_at key
     And I should receive JSON response containing the request_id key
 
    # Timestamp attributes checks
    When I look at recent stack analysis
    Then I should receive JSON response with the correct timestamp in attribute started_at
     And I should receive JSON response with the correct timestamp in attribute finished_at
 
    # Licence and dependency counters checks
    When I look at recent stack analysis
    Then I should find the value requirements.txt under the path result/0/manifest_name in the JSON response
     And I should find the value 7 under the path result/0/user_stack_info/total_licenses in the JSON response
     And I should find the value 0 under the path result/0/user_stack_info/transitive_count in the JSON response
     And I should find the value 0 under the path result/0/user_stack_info/unknown_dependencies_count in the JSON response
     And I should find the value 11 under the path result/0/user_stack_info/analyzed_dependencies_count in the JSON response
     And I should find the value pypi under the path result/0/user_stack_info/ecosystem in the JSON response
 
    # Analyzed dependencies checks
     And I should find analyzed dependency named requests with version 2.22.0 in the stack analysis
     And I should find analyzed dependency named numpy with version 1.16.4 in the stack analysis
     And I should find analyzed dependency named scipy with version 1.3.0 in the stack analysis
     And I should find analyzed dependency named pandas with version 0.24.2 in the stack analysis
