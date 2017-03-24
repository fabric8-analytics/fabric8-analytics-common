Feature: StackAnalyses API V1

  Scenario: Access StackAnalyses Requests
    Given System is running
    When I post a valid package.json to /api/v1/stack-analyses
    Then I should get a valid request ID
    When I access /api/v1/stack-analyses
    Then stack analyses response is available via /api/v1/stack-analyses/
