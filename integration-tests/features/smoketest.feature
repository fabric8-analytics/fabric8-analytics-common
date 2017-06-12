Feature: Smoke test

  Scenario: Check the API entry point
    Given System is running
    When I access /api/v1/
    Then I should get 200 status code
