Feature: Thorough stack analysis v3 API tests - NPM ecosystem


  Scenario: Check that the API entry point requires authorization token
    Given System is running
    When I send NPM package manifest package.json to stack analysis version 3 without authorization token
    Then I should get 401 status code


  @requires_authorization_token @data-sanity
  Scenario: Check the stack analysis response when called with proper authorization token
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I send NPM package manifest package.json to stack analysis version 3 with authorization token
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

    # Timestamp checks
    When I look at recent stack analysis
    Then I should receive JSON response containing the started_at key
     And I should receive JSON response containing the finished_at key
     And I should receive JSON response with the correct timestamp in attribute started_at
     And I should receive JSON response with the correct timestamp in attribute finished_at

    # Request ID check
    When I look at recent stack analysis
    Then I should receive JSON response containing the request_id key
     And I should find the attribute request_id equals to id returned by stack analysis request

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 4 dependencies
     And I should find the following dependencies (lodash, moment, request, underscore) in the stack analysis
     And I should find dependency named lodash with version 4.17.11 in the stack analysis
     And I should find dependency named moment with version 2.24.0 in the stack analysis
     And I should find dependency named request with version 2.88.0 in the stack analysis
     And I should find dependency named underscore with version 1.8.1 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 4 analyzed dependencies
     And I should find the following analyzed dependencies (lodash, moment, request, underscore) in the stack analysis
     And I should find analyzed dependency named lodash with version 4.17.11 in the stack analysis
     And I should find analyzed dependency named moment with version 2.24.0 in the stack analysis
     And I should find analyzed dependency named request with version 2.88.0 in the stack analysis
     And I should find analyzed dependency named underscore with version 1.8.1 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies


  @requires_authorization_token @data-sanity
  Scenario: Check the stack analysis response when called with proper authorization token
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I send NPM package manifest wisp-minified.json to stack analysis version 3 with authorization token
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

    # Timestamp checks
    When I look at recent stack analysis
    Then I should receive JSON response containing the started_at key
     And I should receive JSON response containing the finished_at key
     And I should receive JSON response with the correct timestamp in attribute started_at
     And I should receive JSON response with the correct timestamp in attribute finished_at

    # Request ID check
    When I look at recent stack analysis
    Then I should receive JSON response containing the request_id key
     And I should find the attribute request_id equals to id returned by stack analysis request

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 2 dependencies
     And I should find the following dependencies (base64-encode, commander) in the stack analysis
     And I should find dependency named base64-encode with version 1.0.1 in the stack analysis
     And I should find dependency named commander with version 2.20.0 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 2 analyzed dependencies
     And I should find the following analyzed dependencies (base64-encode, commander) in the stack analysis
     And I should find analyzed dependency named base64-encode with version 1.0.1 in the stack analysis
     And I should find analyzed dependency named commander with version 2.20.0 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies


  @requires_authorization_token @data-sanity
  Scenario: Check the stack analysis response when called with proper authorization token
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I send NPM package manifest wisp-prettyprinted.json to stack analysis version 3 with authorization token
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

    # Timestamp checks
    When I look at recent stack analysis
    Then I should receive JSON response containing the started_at key
     And I should receive JSON response containing the finished_at key
     And I should receive JSON response with the correct timestamp in attribute started_at
     And I should receive JSON response with the correct timestamp in attribute finished_at

    # Request ID check
    When I look at recent stack analysis
    Then I should receive JSON response containing the request_id key
     And I should find the attribute request_id equals to id returned by stack analysis request

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 2 dependencies
     And I should find the following dependencies (base64-encode, commander) in the stack analysis
     And I should find dependency named base64-encode with version 1.0.1 in the stack analysis
     And I should find dependency named commander with version 2.20.0 in the stack analysis

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 2 analyzed dependencies
     And I should find the following analyzed dependencies (base64-encode, commander) in the stack analysis
     And I should find analyzed dependency named base64-encode with version 1.0.1 in the stack analysis
     And I should find analyzed dependency named commander with version 2.20.0 in the stack analysis

    # Unknown dependencies checks
    When I look at recent stack analysis
    Then I should find no more than 0 unknown dependencies
