Feature: Dependency Editor Stack-analyses API behaviour

  Scenario: Check that the API entry point
    Given System is running
    When I access /api/v1/depeditor-analyses
    Then I should get 401 status code

  @requires_authorization_token
  Scenario: Check that the API entry point requires authorization token
    Given System is running
    When I access /api/v1/depeditor-analyses
    Then I should get 400 status code


  @requires_authorization_token
  Scenario: Check that the depeditor-analyses returns a valid response for maven ecosystem
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send valid input with list of packages and versions, ecosystem and request_id with authorization token 
    When I wait 20 seconds
    Then I should get 200 status code
     And I should receive JSON response with the correct id
     And I should find the attribute request_id equals to request_id passed in request
     And I should find user_stack_info and recommendation in result
     And I should find analyzed_dependencies in user_stack_info
     And I should find that unknown_dependencies are none
     And I should find that none analyzed package can be found in recommendation/companion packages as well
     And I should find that dep_snapshot is same as the request payload
