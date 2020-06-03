Feature: Smoketests for stack analysis API tests for Maven ecosystem


  @requires_authorization_token
  Scenario Outline: Check the stack analysis response for selected selected Maven projects
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key

    # request the stack analysis
    When I wait 10 seconds
    When I test Maven dependencies file <file> for stack analysis from vscode through 3scale gateway with user_key
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response containing the status key
     And I should receive JSON response containing the id key
     And I should receive JSON response containing the submitted_at key
     And I should receive JSON response with the status key set to success
     And I should receive JSON response with the correct id
     And I should receive JSON response with the correct timestamp in attribute submitted_at

    # Wait for response from stack analysis
    When I wait for stack analysis to finish with user_key
    Then I should get 200 status code
     And I should receive a valid JSON response

    # SLA/SLO-related checks
    When I look at the stack analysis duration
    Then I should see that the duration is less than 180 seconds

    # Timestamp checks
    When I look at recent stack analysis
    Then I should receive JSON response containing the started_at key
     And I should receive JSON response containing the finished_at key
     And I should receive JSON response with the correct timestamp in attribute started_at
     And I should receive JSON response with the correct timestamp in attribute finished_at

    # Request ID check
    When I look at recent stack analysis
    Then I should receive JSON response containing the request_id key

    # Dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 dependencies

    # Analyzed dependencies checks
    When I look at recent stack analysis
    Then I should find at least 1 analyzed dependencies

    # Analyzed CVE(s) part
    When I look at recent stack analysis
    Then I should find the security node for all dependencies
     And I should find the security node for all alternate components
     And I should find a recommended version when a CVE is found

     Examples: files containing packages to test
     | file                         |
     | basic.txt                    |
     | springboot_dependencies.txt  |
     | vertx_3_4_1_dependencies.txt |
     | vertx_3_4_2_dependencies.txt |
     | vertx_dependencies.txt       |
