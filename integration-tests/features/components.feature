Feature: Components API V1

  Scenario: Check the API entry point
    Given System is running
    When I access /api/v1/
    Then I should get 200 status code

  Scenario: Check if component analysis requires authorization
    Given System is running
    Given Component search service is running
    When I wait 60 seconds
    When I search for component sequence without authorization token
    Then I should get 401 status code

  Scenario: Check the component search API entry point
    Given System is running
    Given Component search service is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I search for component foobar with authorization token
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

  Scenario: Check that the component analyses API entry point make sure resources are specified
    Given System is running
    Given Component search service is running
    When I access /api/v1/component-analyses/
    Then I should get 404 status code

  Scenario: Check if search for packages handle empty results
    Given System is running
    Given Component search service is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I search for component foobar with authorization token
    Then I should get 200 status code
    Then I should see 0 components

  Scenario: Check that component analyses endpoint checks if all resources are specified
    Given System is running
    Given Component search service is running
    When I access /api/v1/component-analyses
    Then I should get 404 status code
    When I access /api/v1/component-analyses/npm
    Then I should get 404 status code
    When I access /api/v1/component-analyses/component
    Then I should get 404 status code

  Scenario: Check if component analysis requires authorization
    Given System is running
    Given Component search service is running
    When I start analysis for component npm/sequence/2.2.0
    Then I should get 401 status code

