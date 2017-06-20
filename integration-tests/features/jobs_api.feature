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

  Scenario: Check that job with given ID can be posted via API
    Given System is running
    When I post a job metadata job1.json with job id TEST_1 and state paused
    Then I should get 201 status code

  Scenario: Check that job with given ID is really registered
    Given System is running
    When I post a job metadata job1.json with job id TEST_2 and state paused
    Then I should get 201 status code
    When I access jobs API /api/v1/jobs
    Then I should find job with id TEST_2

  Scenario: Check that jobs are not replaced
    Given System is running
    When I access jobs API /api/v1/jobs
    Then I should not find job with id TEST_3
    Then I should not find job with id TEST_4
    Then I should not find job with id TEST_5
    When I post a job metadata job1.json with job id TEST_3 and state paused
    Then I should get 201 status code
    When I access jobs API /api/v1/jobs
    Then I should find job with id TEST_3
    Then I should not find job with id TEST_4
    Then I should not find job with id TEST_5
    When I post a job metadata job1.json with job id TEST_4 and state paused
    Then I should get 201 status code
    When I access jobs API /api/v1/jobs
    Then I should find job with id TEST_3
    Then I should find job with id TEST_4
    Then I should not find job with id TEST_5

  Scenario: Check that jobs can be deleted
    Given System is running
    When I access jobs API /api/v1/jobs
    Then I should not find job with id TEST_TO_DELETE
    When I post a job metadata job1.json with job id TEST_TO_DELETE and state paused
    Then I should get 201 status code
    When I access jobs API /api/v1/jobs
    Then I should find job with id TEST_TO_DELETE
    When I delete job with id TEST_TO_DELETE
    Then I should get 200 status code
    When I access jobs API /api/v1/jobs
    Then I should not find job with id TEST_TO_DELETE

