Feature: Checks for the license analysis service

  @smoketest @production
  Scenario: Basic check if the license analysis service is running
    Given System is running
    When I access the license analysis service
    Then I should get 200 status code
    When I acquire the authorization token
    Then I should get proper authorization token
    When I access the license analysis service with authorization token
    Then I should get 200 status code
