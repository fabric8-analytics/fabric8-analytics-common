Feature: Tests for user intent API version 1.0

  Scenario Outline: Check the existence of REST API endpoint for user-intent
    Given System is running
    When I access /api/v1/
    Then I should get 200 status code
     And I should receive JSON response containing the paths key
     And I should find the endpoint <endpoint> in the list of supported endpoints

     Examples: endpoints
         |endpoint|
         |/api/v1/user-intent|
         |/api/v1/user-intent/<user>/<ecosystem>|


  Scenario: Check that the API entry point for user intent requires authorization token
    Given System is running
     When I access /api/v1/user-intent
     Then I should not get 200 status code


  Scenario: Check the HTTP POST call for user intent endpoint - the authorization token should be required
    Given System is running
     When I access the /api/v1/user-intent endpoint using the HTTP POST method
     Then I should get 401 status code


  Scenario: Check that the API entry point for user checks 'user' and 'ecosystem' arguments
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I access /api/v1/user-intent with authorization token
     Then I should get 404 status code
      And I should receive a valid JSON response
      And I should receive JSON response containing the error key


  Scenario: Check that the API entry point for user checks 'user' and 'ecosystem' arguments
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I access /api/v1/user-intent/user with authorization token
     Then I should get 404 status code
      And I should receive a valid JSON response
      And I should receive JSON response containing the error key


  Scenario: Check that the API entry point for user checks 'user' and 'ecosystem' arguments
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I access /api/v1/user-intent/user/npm with authorization token
     Then I should get 404 status code
      And I should receive a valid JSON response
      And I should receive JSON response containing the error key


  Scenario Outline: Check that the user intent REST API endpoint requires authorization token even for improper HTTP methods
    Given System is running
     When I access the /api/v1/user-intent endpoint using the HTTP <method> method
     Then I should get <status> status code

     Examples: HTTP methods
     | method | status |
     | HEAD   | 404 |
     | POST   | 401 |
     | PUT    | 405 |
     | DELETE | 405 |


  Scenario Outline: Check that the user intent REST API endpoint requires authorization token even for improper HTTP methods
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I access the /api/v1/user-intent endpoint using the HTTP <method> method and authorization token
     Then I should get <status> status code

     Examples: HTTP methods
     | method | status |
     | HEAD   | 404 |
     | POST   | 400 |
     | PUT    | 405 |
     | DELETE | 405 |


  Scenario: Check the HTTP POST call for user intent endpoint - proper authorization token, but no payload
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I call user-intent endpoint without any payload
     Then I should get 400 status code
      And I should receive a valid JSON response
      And I should receive JSON response containing the error key
      And I should receive JSON response with the error key set to Expected JSON request


  Scenario: Check the HTTP POST call for user intent endpoint - proper authorization token and empty payload
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I call user-intent endpoint with empty payload
     Then I should get 400 status code
      And I should receive a valid JSON response
      And I should receive JSON response containing the error key
      And I should receive JSON response with the error key set to Expected JSON request


  Scenario: Check the HTTP POST call for user intent endpoint - proper authorization token and incorrect payload
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I call user-intent endpoint with incorrect payload
     Then I should get 400 status code
      And I should receive a valid JSON response
      And I should receive JSON response containing the error key
      And I should receive JSON response with the error key set to Expected ecosystem in the request


  Scenario: Check the HTTP POST call for user intent endpoint - proper authorization token and manual tagging in JSON
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I call user-intent endpoint with payload that contains only manual_tagging attribute
     Then I should get 400 status code
      And I should receive a valid JSON response
      And I should receive JSON response containing the error key
      And I should receive JSON response with the error key set to Expected user name in the request


  Scenario: Check the HTTP POST call for user intent endpoint - proper authorization token and manual tagging + user in JSON
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I call user-intent endpoint with payload that contains only manual_tagging and user attributes
     Then I should get 400 status code
      And I should receive a valid JSON response
      And I should receive JSON response containing the error key
      And I should receive JSON response with the error key set to Expected tags in the request


  Scenario: Check the HTTP POST call for user intent endpoint - proper authorization token and ecosystem in JSON
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I call user-intent endpoint with payload that contains only ecosystem attribute
     Then I should get 400 status code
      And I should receive a valid JSON response
      And I should receive JSON response containing the error key
      And I should receive JSON response with the error key set to Expected data in the request
