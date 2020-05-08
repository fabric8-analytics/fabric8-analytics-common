Feature: Analyse API functionality check

  @production
  Scenario: Check that the REST API point for the stack analyses accepts authorization tokens
    Given System is running
     When I access /api/v1/stack-analyses
     Then I should get 401 status code


  Scenario Outline: Check that the stack analysis REST API endpoint requires authorization token even for improper HTTP methods
    Given System is running
     When I access the /api/v1/stack-analyses endpoint using the HTTP <method> method
     Then I should not get 200 status code

     Examples: HTTP methods
     | method |
     | GET    |
     | HEAD   |
     | PUT    |
     | DELETE |


  Scenario Outline: Check that the stack analysis REST API endpoint does not accept any HTTP method other than POST
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I access the /api/v1/stack-analyses endpoint using the HTTP <method> method and authorization token
     Then I should not get 200 status code

     Examples: HTTP methods
     | method |
     | GET    |
     | HEAD   |
     | PUT    |
     | DELETE |


  @production
  Scenario: Check that the REST API point for the stack analyses with external ID accepts authorization tokens
    Given System is running
    When I access /api/v1/stack-analyses/external-id
    Then I should get 401 status code

  Scenario Outline: Check that the stack analysis REST API endpoint requires authorization token even for improper HTTP methods
    Given System is running
     When I access the /api/v1/stack-analyses/external-id endpoint using the HTTP <method> method
     Then I should not get 200 status code

     Examples: HTTP methods
     | method |
     | GET    |
     | HEAD   |
     | PUT    |
     | DELETE |


  Scenario Outline: Check that the stack analysis REST API endpoint does not accept any HTTP method other than POST
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I access the /api/v1/stack-analyses/external-id endpoint using the HTTP <method> method and authorization token
     Then I should not get 200 status code

     Examples: HTTP methods
     | method |
     | GET    |
     | HEAD   |
     | PUT    |
     | DELETE |


  @production
  Scenario: Check that the API entry point requires authorization token
    Given System is running
    When I wait 10 seconds
    When I send Maven package manifest pom-effective.xml to stack analysis without authorization token
    Then I should get 401 status code

  Scenario: Check that the stack-analyses returns a valid response for maven ecosystem
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I wait 10 seconds
    When I send Maven package manifest pom-effective.xml to stack analysis version 3 with authorization token
    Then I should get 200 status code
     And I should receive JSON response with the correct id
    When I wait for stack analysis to finish with authorization token
    Then I should get 200 status code
     And I should get a valid request ID
     And I should find the attribute request_id equals to id returned by stack analysis request
     And I should find that none analyzed package can be found in companion packages as well
     And I should find that valid outliers are reported
     And I should get license_analysis field in stack report
     And I should find that alternate components replace user components
     And I should find the security node for all dependencies
     And I should find the security node for all alternate components
     And I should find input_stack_topics field in recommendation
     And I should find matching topic lists for all user_stack_info/analyzed_dependencies components

  Scenario: Check that the stack-analyses returns a valid response for NPM ecosystem
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I wait 10 seconds
    When I send NPM package manifest package.json to stack analysis version 3 with authorization token
    Then I should get 200 status code
     And I should receive JSON response with the correct id
    When I wait for stack analysis to finish with authorization token
    Then I should get 200 status code
     And I should get a valid request ID
     And I should find the attribute request_id equals to id returned by stack analysis request
     And I should find that none analyzed package can be found in companion packages as well
     # Alternates, Outliers are not yet implemented.
     And I should find that total 0 outliers are reported
     And I should find that greater than 0 companions are reported
     And I should get license_analysis field in stack report
     And I should find the security node for all dependencies
     And I should find input_stack_topics field in recommendation
     And I should find matching topic lists for all user_stack_info/analyzed_dependencies components

  Scenario: Check that the stack-analyses returns a valid response for pypi ecosystem
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I wait 10 seconds
    When I test pypi dependencies file pylist.json for stack analysis from vscode
    Then I should get 200 status code
     And I should receive JSON response with the correct id
    When I wait for stack analysis to finish with authorization token
    Then I should get 200 status code
     And I should get a valid request ID
     And I should find the attribute request_id equals to id returned by stack analysis request
     And I should find that none analyzed package can be found in companion packages as well
     And I should find that valid outliers are reported
     And I should get license_analysis field in stack report
     And I should find the security node for all dependencies

  Scenario: Check that the stack-analyses returns a valid response for dynamic manifest files
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I wait 10 seconds
    When I tried to fetch dynamic manifests from s3
    Then I should be able to validate them
    When I wait 5 seconds
    When I send Python package manifest valid_manifests/pylist.json to stack analysis version 3 with authorization token
    When I wait 5 seconds
    Then I should get 200 status code
      And I should receive JSON response with the correct id
    When I wait for dynamic stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should get a valid request ID
     And I should find the attribute request_id equals to id returned by stack analysis request
     And I should find that none analyzed package can be found in companion packages as well
     And I should find that valid outliers are reported
     And I should get license_analysis field in stack report
     And I should find the security node for all dependencies
    When I send new Maven package manifest valid_manifests/dependencies.txt to stack analysis version 3 with authorization token
    When I wait 5 seconds
    Then I should get 200 status code
      And I should receive JSON response with the correct id
    When I wait for dynamic stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should get a valid request ID
     And I should find the attribute request_id equals to id returned by stack analysis request
     And I should find that none analyzed package can be found in companion packages as well
     And I should find that valid outliers are reported
     And I should get license_analysis field in stack report
     And I should find the security node for all dependencies
    When I send NPM package manifest valid_manifests/npmlist.json to new stack analysis version 3 with authorization token
    When I wait 15 seconds
    Then I should get 200 status code
      And I should receive JSON response with the correct id
    When I wait for dynamic stack analysis version 3 to finish with authorization token
    When I wait 10 seconds
    Then I should get 200 status code
     And I should get a valid request ID
     And I should find the attribute request_id equals to id returned by stack analysis request
     And I should find that none analyzed package can be found in companion packages as well
     And I should find that valid outliers are reported
     And I should get license_analysis field in stack report
     And I should find the security node for all dependencies

