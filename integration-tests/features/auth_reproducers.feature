Feature: The auth-related issues reproducer

  @requires_authorization_token
  Scenario: Check if the user feedback is received by the system
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I post valid input to the /api/v1/user-feedback endpoint without authorization token
    Then I should get 401 status code
    When I post invalid input to the /api/v1/user-feedback endpoint with authorization token
    Then I should get 400 status code
    When I post valid input to the /api/v1/user-feedback endpoint with authorization token
    Then I should get 200 status code
