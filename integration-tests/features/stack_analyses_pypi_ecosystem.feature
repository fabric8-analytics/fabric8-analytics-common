Feature: Thorough stack analysis v3 API tests for PyPi ecosystem


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for newer version of click package (6.7)
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file requirements_click_newest_6_7.txt for stack analysis from vscode
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response containing the status key
     And I should receive JSON response containing the id key
     And I should receive JSON response containing the submitted_at key
     And I should receive JSON response with the status key set to success
     And I should receive JSON response with the correct id
     And I should receive JSON response with the correct timestamp in attribute submitted_at

    # wait for response from stack analysis
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response with the correct request_id
     And I should find analyzed dependency named click with version 6.7 in the stack analysis

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (click) in the stack analysis
     And I should find dependency named click with version 6.7 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies
     And I should find the following analyzed dependencies (click) in the stack analysis
     And I should find analyzed dependency named click with version 6.7 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for newer version of click package (7.0)
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file requirements_click_newest_7_0.txt for stack analysis from vscode
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response containing the status key
     And I should receive JSON response containing the id key
     And I should receive JSON response containing the submitted_at key
     And I should receive JSON response with the status key set to success
     And I should receive JSON response with the correct id
     And I should receive JSON response with the correct timestamp in attribute submitted_at

    # wait for response from stack analysis
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response with the correct request_id
     And I should find analyzed dependency named click with version 7.0 in the stack analysis

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (click) in the stack analysis
     And I should find dependency named click with version 7.0 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies
     And I should find the following analyzed dependencies (click) in the stack analysis
     And I should find analyzed dependency named click with version 7.0 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for exact version of click package (arbitrary equality)
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file requirements_click_arbitrary_equality.txt for stack analysis from vscode
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response containing the status key
     And I should receive JSON response containing the id key
     And I should receive JSON response containing the submitted_at key
     And I should receive JSON response with the status key set to success
     And I should receive JSON response with the correct id
     And I should receive JSON response with the correct timestamp in attribute submitted_at

    # wait for response from stack analysis
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response with the correct request_id
     And I should find analyzed dependency named click with version 6.7 in the stack analysis

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (click) in the stack analysis
     And I should find dependency named click with version 6.7 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies
     And I should find the following analyzed dependencies (click) in the stack analysis
     And I should find analyzed dependency named click with version 6.7 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for older version of click package with click>=5.0 in requirements
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file requirements_click_version_gt_5_0.txt for stack analysis from vscode
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response containing the status key
     And I should receive JSON response containing the id key
     And I should receive JSON response containing the submitted_at key
     And I should receive JSON response with the status key set to success
     And I should receive JSON response with the correct id
     And I should receive JSON response with the correct timestamp in attribute submitted_at

    # wait for response from stack analysis
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response with the correct request_id
     And I should find analyzed dependency named click with version 7.0 in the stack analysis

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (click) in the stack analysis
     And I should find dependency named click with version 7.0 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies
     And I should find the following analyzed dependencies (click) in the stack analysis
     And I should find analyzed dependency named click with version 7.0 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for older version (5.0) of click package
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file requirements_click_version_eq_5_0.txt for stack analysis from vscode
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response containing the status key
     And I should receive JSON response containing the id key
     And I should receive JSON response containing the submitted_at key
     And I should receive JSON response with the status key set to success
     And I should receive JSON response with the correct id
     And I should receive JSON response with the correct timestamp in attribute submitted_at

    # wait for response from stack analysis
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response with the correct request_id
     And I should find analyzed dependency named click with version 5.0 in the stack analysis

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (click) in the stack analysis
     And I should find dependency named click with version 5.0 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies
     And I should find the following analyzed dependencies (click) in the stack analysis
     And I should find analyzed dependency named click with version 5.0 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for older version of click package with click>=5.0, <=6.0 in requirements
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file requirements_click_version_ge_5_0_le_6_0.txt for stack analysis from vscode
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response containing the status key
     And I should receive JSON response containing the id key
     And I should receive JSON response containing the submitted_at key
     And I should receive JSON response with the status key set to success
     And I should receive JSON response with the correct id
     And I should receive JSON response with the correct timestamp in attribute submitted_at

    # wait for response from stack analysis
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response with the correct request_id
     And I should find analyzed dependency named click with version 6.0 in the stack analysis
 
    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (click) in the stack analysis
     And I should find dependency named click with version 6.0 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies
     And I should find the following analyzed dependencies (click) in the stack analysis
     And I should find analyzed dependency named click with version 6.0 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies

 
  @requires_authorization_token
  Scenario: Check the analyzed dependencies for older version of click package with click>=5.0, <6.0 in requirements
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file requirements_click_version_ge_5_0_lt_6_0.txt for stack analysis from vscode
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response containing the status key
     And I should receive JSON response containing the id key
     And I should receive JSON response containing the submitted_at key
     And I should receive JSON response with the status key set to success
     And I should receive JSON response with the correct id
     And I should receive JSON response with the correct timestamp in attribute submitted_at

    # wait for response from stack analysis
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response with the correct request_id
     And I should find analyzed dependency named click with version 5.1 in the stack analysis
 
    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (click) in the stack analysis
     And I should find dependency named click with version 5.1 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies
     And I should find the following analyzed dependencies (click) in the stack analysis
     And I should find analyzed dependency named click with version 5.1 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies

 
  @requires_authorization_token
  Scenario: Check the analyzed dependencies for older version of click package with click>5.0, <6.0 in requirements
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file requirements_click_version_gt_5_0_lt_6_0.txt for stack analysis from vscode
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response containing the status key
     And I should receive JSON response containing the id key
     And I should receive JSON response containing the submitted_at key
     And I should receive JSON response with the status key set to success
     And I should receive JSON response with the correct id
     And I should receive JSON response with the correct timestamp in attribute submitted_at

    # wait for response from stack analysis
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response with the correct request_id
     And I should find analyzed dependency named click with version 5.1 in the stack analysis
 
    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (click) in the stack analysis
     And I should find dependency named click with version 5.1 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies
     And I should find the following analyzed dependencies (click) in the stack analysis
     And I should find analyzed dependency named click with version 5.1 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies

 
  @requires_authorization_token
  Scenario: Check the analyzed dependencies for older version of click package with click>5.0, <=6.0 in requirements
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file requirements_click_version_gt_5_0_le_6_0.txt for stack analysis from vscode
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response containing the status key
     And I should receive JSON response containing the id key
     And I should receive JSON response containing the submitted_at key
     And I should receive JSON response with the status key set to success
     And I should receive JSON response with the correct id
     And I should receive JSON response with the correct timestamp in attribute submitted_at

    # wait for response from stack analysis
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response with the correct request_id
     And I should find analyzed dependency named click with version 6.0 in the stack analysis
 
    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (click) in the stack analysis
     And I should find dependency named click with version 6.0 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies
     And I should find the following analyzed dependencies (click) in the stack analysis
     And I should find analyzed dependency named click with version 6.0 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies

 
  @requires_authorization_token
  Scenario: Check the analyzed dependencies for click 6.7.*
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file requirements_click_6_7_star.txt for stack analysis from vscode
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response containing the status key
     And I should receive JSON response containing the id key
     And I should receive JSON response containing the submitted_at key
     And I should receive JSON response with the status key set to success
     And I should receive JSON response with the correct id
     And I should receive JSON response with the correct timestamp in attribute submitted_at

    # wait for response from stack analysis
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response with the correct request_id
     And I should find analyzed dependency named click with version 6.7 in the stack analysis
 
    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (click) in the stack analysis
     And I should find dependency named click with version 6.7 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies
     And I should find the following analyzed dependencies (click) in the stack analysis
     And I should find analyzed dependency named click with version 6.7 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies


  @requires_authorization_token
  Scenario: Check the integer normalization in requirements.txt for major and minor version numbers
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file requirements_click_normalize_integer_minor.txt for stack analysis from vscode
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response containing the status key
     And I should receive JSON response containing the id key
     And I should receive JSON response containing the submitted_at key
     And I should receive JSON response with the status key set to success
     And I should receive JSON response with the correct id
     And I should receive JSON response with the correct timestamp in attribute submitted_at

    # wait for response from stack analysis
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

    # request the stack analysis
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
     And I should find the value 6 under the path result/0/user_stack_info/total_licenses in the JSON response
     And I should find the value 0 under the path result/0/user_stack_info/transitive_count in the JSON response
     And I should find the value 0 under the path result/0/user_stack_info/unknown_dependencies_count in the JSON response
     And I should find the value 11 under the path result/0/user_stack_info/analyzed_dependencies_count in the JSON response
     And I should find the value pypi under the path result/0/user_stack_info/ecosystem in the JSON response
 
    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 11 dependencies
     And I should find the following dependencies (requests, scikit-learn, coverage, cycler, numpy, mock, nose, scipy, matplotlib, nltk, pandas) in the stack analysis
     And I should find dependency named requests with version 2.22.0 in the stack analysis
     And I should find dependency named scikit-learn with version 0.21.2 in the stack analysis
     And I should find dependency named cycler with version 0.10.0 in the stack analysis
     And I should find dependency named numpy with version 1.17.0rc1 in the stack analysis
     And I should find dependency named mock with version 3.0.5 in the stack analysis
     And I should find dependency named nose with version 1.3.7 in the stack analysis
     And I should find dependency named scipy with version 1.3.0 in the stack analysis
     And I should find dependency named matplotlib with version 3.1.0 in the stack analysis
     And I should find dependency named nltk with version 3.4.3 in the stack analysis
     And I should find dependency named pandas with version 0.24.2 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 11 analyzed dependencies
     And I should find the following analyzed dependencies (requests, scikit-learn, coverage, cycler, numpy, mock, nose, scipy, matplotlib, nltk, pandas) in the stack analysis
     And I should find analyzed dependency named requests with version 2.22.0 in the stack analysis
     And I should find analyzed dependency named scikit-learn with version 0.21.2 in the stack analysis
     And I should find analyzed dependency named cycler with version 0.10.0 in the stack analysis
     And I should find analyzed dependency named numpy with version 1.16.4 in the stack analysis
     And I should find analyzed dependency named mock with version 3.0.5 in the stack analysis
     And I should find analyzed dependency named nose with version 1.3.7 in the stack analysis
     And I should find analyzed dependency named scipy with version 1.3.0 in the stack analysis
     And I should find analyzed dependency named matplotlib with version 3.1.0 in the stack analysis
     And I should find analyzed dependency named nltk with version 3.4.3 in the stack analysis
     And I should find analyzed dependency named pandas with version 0.24.2 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies

