Feature: Components API V1

  Scenario: Check the API entry point
    Given System is running
    When I access /api/v1/
    Then I should get 200 status code

  Scenario: Check the component search API entry point
    Given System is running
    Given Component search service is running
    When I search for component foobar
    Then I should get 200 status code

  Scenario: Check that the component search API entry point requires component name
    Given System is running
    Given Component search service is running
    When I access /api/v1/component-search
    Then I should get 404 status code

  Scenario: Check that the component search API entry point checks for empty component name
    Given System is running
    Given Component search service is running
    When I access /api/v1/component-search/
    Then I should get 404 status code

  Scenario: Check if search for packages handle empty results
    Given System is running
    Given Component search service is running
    When I search for component foobar
    Then I should see 0 components

