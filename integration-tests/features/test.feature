Feature: Server API

  @production
  Scenario: Check the /api/v1/submit-feedback response
    Given System is running
    When I access /api/v1/submit-feedback without valid values
    Then I should get 400 status code

