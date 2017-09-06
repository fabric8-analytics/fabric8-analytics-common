Feature: Component search API

  Scenario: Check the component search functionality for nonexistent component
    Given System is running
    Given Component search service is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I search for component sequence with authorization token
    Then I should not find the analysis for the component sequence from ecosystem npm

  Scenario: Check the component search functionality for existing component
    Given System is running
    Given Component search service is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I search for component wisp with authorization token
    Then I should find the analysis for the component wisp from ecosystem npm

