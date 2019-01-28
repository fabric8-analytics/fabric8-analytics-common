Feature: Tests for user intent API version 1.0

  @production
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


  @production
  Scenario: Check that the API entry point for user intent requires authorization token
    Given System is running
     When I access /api/v1/user-intent
     Then I should not get 200 status code


  @production
  Scenario: Check that the API entry point for user checks 'user' and 'ecosystem' argumentes
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I access /api/v1/user-intent with authorization token
     Then I should get 404 status code
      And I should receive a valid JSON response
      And I should receive JSON response containing the error key


  @production
  Scenario: Check that the API entry point for user checks 'user' and 'ecosystem' argumentes
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I access /api/v1/user-intent/user with authorization token
     Then I should get 404 status code
      And I should receive a valid JSON response
      And I should receive JSON response containing the error key


  @production
  Scenario: Check that the API entry point for user checks 'user' and 'ecosystem' argumentes
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

