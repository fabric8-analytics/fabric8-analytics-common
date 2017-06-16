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

  Scenario: Check that new job can be posted with state paused
    Given System is running
    When I post a job metadata job1.json with state paused
    Then I should get 201 status code
    When I access jobs API /api/v1/jobs
    Then I should see 5 jobs

  Scenario: Check that multiple jobs can be posted with state paused
    Given System is running
    When I access jobs API /api/v1/jobs
    Then I should see 5 jobs
    When I post a job metadata job1.json with state paused
    Then I should get 201 status code
    When I access jobs API /api/v1/jobs
    Then I should see 6 jobs
    When I post a job metadata job1.json with state paused
    Then I should get 201 status code
    When I access jobs API /api/v1/jobs
    Then I should see 7 jobs

