Feature: Jobs API

  Scenario: Check the /api/v1/readiness response
    Given System is running
    When I access jobs API /api/v1/readiness
    Then I should get 200 status code
    Then I should receive empty JSON response

  Scenario: Check the /api/v1/liveness response
    Given System is running
    When I access jobs API /api/v1/liveness
    Then I should get 200 status code
    Then I should receive empty JSON response

  Scenario: Check the API entry point
    Given System is running
    When I access jobs API /api/v1/service/state
    Then I should get 200 status code
    Then I should receive JSON response with the state key set to running

  Scenario: Check the API entry point
    Given System is running
    When I access jobs API /api/v1/jobs
    Then I should get 200 status code
    Then I should receive JSON response containing the jobs key
    Then I should receive JSON response containing the jobs_count key

  Scenario: Check initial number of jobs
    Given System is running
    When I access jobs API /api/v1/jobs
    Then I should get 200 status code
    Then I should see 4 jobs

