Feature: Server API

  @production
  Scenario: Check the /api/v1/submit-feedback response
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I access /api/v1/submit-feedback without valid values
    Then I should get 400 status code

