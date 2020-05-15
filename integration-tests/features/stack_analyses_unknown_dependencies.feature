Feature: Thorough stack analysis v3 API tests

  @requires_authorization_token @skip
  Scenario: Check the stack analysis output
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token

    # request the stack analysis
    When I test pypi dependencies file requirements_1_unknown_dependency.txt for stack analysis from vscode
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
     And I should find exactly one really unknown dependency
