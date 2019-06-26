Feature: Thorough stack analysis v3 API tests for PyPi ecosystem, with pylist.json as input

  @requires_authorization_token
  Scenario: Check the analyzed dependencies for newer version of click package (6.7)
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file requirements_click_6_7.json for stack analysis from vscode
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
    When I test pypi dependencies file requirements_click_7_0.json for stack analysis from vscode
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
  Scenario: Check the analyzed dependencies for array split package (7.0)
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file array_split.json for stack analysis from vscode
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
     And I should find analyzed dependency named array-split with version 0.3.0 in the stack analysis

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (array-split) in the stack analysis
     And I should find dependency named array-split with version 0.3.0 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies
     And I should find the following analyzed dependencies (array-split) in the stack analysis
     And I should find analyzed dependency named array-split with version 0.3.0 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for common and popular Python packages
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file fastlog_urllib_requests.json for stack analysis from vscode
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

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 3 dependencies
     And I should find the following dependencies (fastlog, requests, urllib3) in the stack analysis
     And I should find dependency named fastlog with version 1.0.0b1 in the stack analysis
     And I should find dependency named requests with version 2.18.4 in the stack analysis
     And I should find dependency named urllib3 with version 1.22 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 3 analyzed dependencies
     And I should find the following analyzed dependencies (fastlog, requests, urllib3) in the stack analysis
     And I should find analyzed dependency named fastlog with version 1.0.0b1 in the stack analysis
     And I should find analyzed dependency named requests with version 2.18.4 in the stack analysis
     And I should find analyzed dependency named urllib3 with version 1.22 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies



  @requires_authorization_token
  Scenario: Check the analyzed dependencies for common and popular Python packages
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file numpy_1_11_0.json for stack analysis from vscode
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

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (numpy) in the stack analysis
     And I should find dependency named numpy with version 1.11.0 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies
     And I should find the following analyzed dependencies (numpy) in the stack analysis
     And I should find analyzed dependency named numpy with version 1.11.0 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for common and popular Python packages
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file numpy_1_12_0.json for stack analysis from vscode
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

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (numpy) in the stack analysis
     And I should find dependency named numpy with version 1.12.0 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies
     And I should find the following analyzed dependencies (numpy) in the stack analysis
     And I should find analyzed dependency named numpy with version 1.12.0 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for common and popular Python packages
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file numpy_1_16_2.json for stack analysis from vscode
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

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (numpy) in the stack analysis
     And I should find dependency named numpy with version 1.16.2 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies
     And I should find the following analyzed dependencies (numpy) in the stack analysis
     And I should find analyzed dependency named numpy with version 1.16.2 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for common and popular Python packages
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file numpy_1_16_3.json for stack analysis from vscode
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

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (numpy) in the stack analysis
     And I should find dependency named numpy with version 1.16.3 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies
     And I should find the following analyzed dependencies (numpy) in the stack analysis
     And I should find analyzed dependency named numpy with version 1.16.3 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for common and popular Python packages
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file numpy_scipy.json for stack analysis from vscode
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

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 2 dependencies
     And I should find the following dependencies (numpy, scipy) in the stack analysis
     And I should find dependency named numpy with version 1.11.0 in the stack analysis
     And I should find dependency named scipy with version 1.1.0 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 2 analyzed dependencies
     And I should find the following analyzed dependencies (numpy, scipy) in the stack analysis
     And I should find analyzed dependency named numpy with version 1.11.0 in the stack analysis
     And I should find analyzed dependency named scipy with version 1.1.0 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for common and popular Python packages
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file pytest_2_0_0.json for stack analysis from vscode
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

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (pytest) in the stack analysis
     And I should find dependency named pytest with version 2.0.0 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies
     And I should find the following analyzed dependencies (pytest) in the stack analysis
     And I should find analyzed dependency named pytest with version 2.0.0 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for common and popular Python packages
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file pytest_2_0_1.json for stack analysis from vscode
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

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (pytest) in the stack analysis
     And I should find dependency named pytest with version 2.0.1 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies
     And I should find the following analyzed dependencies (pytest) in the stack analysis
     And I should find analyzed dependency named pytest with version 2.0.1 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for common and popular Python packages
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file pytest_3_2_2.json for stack analysis from vscode
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

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (pytest) in the stack analysis
     And I should find dependency named pytest with version 3.2.2 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies
     And I should find the following analyzed dependencies (pytest) in the stack analysis
     And I should find analyzed dependency named pytest with version 3.2.2 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for common and popular Python packages
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file requests_2_20_0.json for stack analysis from vscode
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

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (requests) in the stack analysis
     And I should find dependency named requests with version 2.21.0 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies
     And I should find the following analyzed dependencies (requests) in the stack analysis
     And I should find analyzed dependency named requests with version 2.21.0 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for common and popular Python packages
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file requests_2_20_1.json for stack analysis from vscode
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

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (requests) in the stack analysis
     And I should find dependency named requests with version 2.21.1 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 0 analyzed dependencies


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for common and popular Python packages
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file requests_2_21_0.json for stack analysis from vscode
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

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (requests) in the stack analysis
     And I should find dependency named requests with version 2.21.0 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies
     And I should find the following analyzed dependencies (requests) in the stack analysis
     And I should find analyzed dependency named requests with version 2.21.0 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for common and popular Python packages
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file scipy_1_1_0.json for stack analysis from vscode
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

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (scipy) in the stack analysis
     And I should find dependency named scipy with version 1.1.0 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies
     And I should find the following analyzed dependencies (scipy) in the stack analysis
     And I should find analyzed dependency named scipy with version 1.1.0 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for common and popular Python packages
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file scipy_1_2_0.json for stack analysis from vscode
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

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (scipy) in the stack analysis
     And I should find dependency named scipy with version 1.2.0 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies
     And I should find the following analyzed dependencies (scipy) in the stack analysis
     And I should find analyzed dependency named scipy with version 1.2.0 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies


  @requires_authorization_token
  Scenario: Check the analyzed dependencies for common and popular Python packages
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file scipy_1_2_1.json for stack analysis from vscode
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

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies
     And I should find the following dependencies (scipy) in the stack analysis
     And I should find dependency named scipy with version 1.2.1 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies
     And I should find the following analyzed dependencies (scipy) in the stack analysis
     And I should find analyzed dependency named scipy with version 1.2.1 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies
