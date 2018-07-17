Feature: Dependency Editor API behaviour

  Scenario: Check the API entry point of Dependency Editor
    Given System is running
    When I access Dependency Editor API entry point
    Then I should get 200 status code

