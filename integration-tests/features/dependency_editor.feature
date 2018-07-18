Feature: Dependency Editor API behaviour

  Scenario: Check the API entry point of Dependency Editor
    Given System is running
    When I access Dependency Editor API entry point
    Then I should get 200 status code

  Scenario: Verify that the stack-analyses API endpoint returns a valid ID
    Given System is running
    When I access the Dependency Editor stack-analyses endpoint
    Then I should receive a valid ID

  Scenario: Verify that the stack-analyses API endpoint accepts a valid ID
    Given System is running
    When I access the Dependency Editor stack-analyses endpoint for an ID
    Then I should receive full analysis output


