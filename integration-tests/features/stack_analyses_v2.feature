Feature: Stack analysis v2 API

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

  Scenario: Check that the API entry point requires authorization token
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I wait 20 seconds
    When I send Python package manifest requirements.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code

  Scenario: Check the stack analysis v2 response when called with proper authorization token
    Given System is running
    When I acquire the authorization token
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
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Python package manifest requirements.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish without authorization token
    Then I should get 401 status code

  Scenario: Check if the stack analysis is finished
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Python package manifest requirements.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish with authorization token
    Then I should get 200 status code

  Scenario: Check the stack analysis output
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Python package manifest requirements.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish with authorization token
    Then I should get 200 status code
    Then I should receive JSON response containing the started_at key
    Then I should receive JSON response containing the finished_at key
    Then I should receive JSON response containing the request_id key
    Then I should find the value requirements.txt under the path result/0/manifest_name in the JSON response
    Then I should find the value 0 under the path result/0/user_stack_info/total_licenses in the JSON response
    Then I should find the value 0 under the path result/0/user_stack_info/unknown_dependencies_count in the JSON response
    Then I should find the value pypi under the path result/0/user_stack_info/ecosystem in the JSON response

  Scenario: Check the stack analysis timestamp attributes
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Python package manifest requirements.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish with authorization token
    Then I should get 200 status code
    Then I should find analyzed dependency named click with version 6.7 in the stack analysis
    Then I should receive JSON response with the correct timestamp in attribute started_at
    Then I should receive JSON response with the correct timestamp in attribute finished_at
    Then I should find proper timestamp under the path result/0/_audit/started_at
    Then I should find proper timestamp under the path result/0/_audit/ended_at

  Scenario: Check the analyzed dependencies for newer version of click package
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Python package manifest requirements_click_newest_6_7.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish with authorization token
    Then I should get 200 status code
    Then I should find the value click under the path result/0/user_stack_info/analyzed_dependencies/0/package in the JSON response
    Then I should find the value 6.7 under the path result/0/user_stack_info/analyzed_dependencies/0/version in the JSON response

  Scenario: Check the analyzed dependencies for the exact version (arbitrary equality)
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Python package manifest requirements_click_arbitrary_equality.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish with authorization token
    Then I should get 200 status code
    Then I should find the value click under the path result/0/user_stack_info/analyzed_dependencies/0/package in the JSON response
    Then I should find the value 6.7 under the path result/0/user_stack_info/analyzed_dependencies/0/version in the JSON response

  Scenario: Check the analyzed dependencies for older version of click package
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Python package manifest requirements_click_version_eq_5_0.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish with authorization token
    Then I should get 200 status code
    Then I should find the value click under the path result/0/user_stack_info/analyzed_dependencies/0/package in the JSON response
    Then I should find the value 5.0 under the path result/0/user_stack_info/analyzed_dependencies/0/version in the JSON response

  Scenario: Check the analyzed dependencies for older version of click package with click>=5.0 in requirements
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Python package manifest requirements_click_version_ge_5_0.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish with authorization token
    Then I should get 200 status code
    Then I should find the value click under the path result/0/user_stack_info/analyzed_dependencies/0/package in the JSON response
    Then I should find the value 6.7 under the path result/0/user_stack_info/analyzed_dependencies/0/version in the JSON response

  Scenario: Check the analyzed dependencies for older version of click package with click>5.0 in requirements
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Python package manifest requirements_click_version_gt_5_0.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish with authorization token
    Then I should get 200 status code
    Then I should find the value click under the path result/0/user_stack_info/analyzed_dependencies/0/package in the JSON response
    Then I should find the value 6.7 under the path result/0/user_stack_info/analyzed_dependencies/0/version in the JSON response

  Scenario: Check the analyzed dependencies for older version of click package with click>=5.0, <=6.0 in requirements
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Python package manifest requirements_click_version_ge_5_0_le_6_0.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish with authorization token
    Then I should get 200 status code
    Then I should find the value click under the path result/0/user_stack_info/analyzed_dependencies/0/package in the JSON response
    Then I should find the value 6.0 under the path result/0/user_stack_info/analyzed_dependencies/0/version in the JSON response

  Scenario: Check the analyzed dependencies for older version of click package with click>=5.0, <6.0 in requirements
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Python package manifest requirements_click_version_ge_5_0_lt_6_0.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish with authorization token
    Then I should get 200 status code
    Then I should find the value click under the path result/0/user_stack_info/analyzed_dependencies/0/package in the JSON response
    Then I should find the value 5.1 under the path result/0/user_stack_info/analyzed_dependencies/0/version in the JSON response

  Scenario: Check the analyzed dependencies for older version of click package with click>5.0, <6.0 in requirements
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Python package manifest requirements_click_version_gt_5_0_lt_6_0.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish with authorization token
    Then I should get 200 status code
    Then I should find the value click under the path result/0/user_stack_info/analyzed_dependencies/0/package in the JSON response
    Then I should find the value 5.1 under the path result/0/user_stack_info/analyzed_dependencies/0/version in the JSON response

  Scenario: Check the analyzed dependencies for older version of click package with click>5.0, <=6.0 in requirements
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Python package manifest requirements_click_version_gt_5_0_le_6_0.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish with authorization token
    Then I should get 200 status code
    Then I should find the value click under the path result/0/user_stack_info/analyzed_dependencies/0/package in the JSON response
    Then I should find the value 6.0 under the path result/0/user_stack_info/analyzed_dependencies/0/version in the JSON response

  Scenario: Check the analyzed dependencies for click 6.7.*
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Python package manifest requirements_click_6_7_star.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish with authorization token
    Then I should get 200 status code
    Then I should find the value click under the path result/0/user_stack_info/analyzed_dependencies/0/package in the JSON response
    Then I should find the value 6.7.dev0 under the path result/0/user_stack_info/analyzed_dependencies/0/version in the JSON response

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

  Scenario: Check the analyzed dependencies part
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Python package manifest requirements_click_newest_6_7.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code
    When I wait for stack analysis version 2 to finish with authorization token
    Then I should find the following analyzed dependencies (click) in the stack analysis

