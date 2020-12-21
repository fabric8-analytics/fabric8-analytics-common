Feature: Smoke test


  @smoketest @production
  Scenario: Check the API entry point for server deployment
    Given System is running
    When I access /api/v1/
    Then I should get 200 status code


  @smoketest @production
  Scenario: Check the /system/version entry point for server deployment
    Given System is running
    When I access /api/v1/system/version/
    Then I should get 200 status code
     And I should receive JSON response containing the commit_hash key
     And I should receive JSON response containing the committed_at key
     And I should find the correct commit hash in the JSON response
     And I should find the correct committed at timestamp in the JSON response


  @smoketest @production
  Scenario: Check if 3scale staging url requires authentication
    Given 3scale staging pod is running
     When I access get_route API end point for 3scale without authorization
     Then I should get 404 status code
      And I should get proper 3scale error message


  @smoketest @production
  Scenario: Check the 'readiness' REST API point for the Gemini service
    Given System is running
    When I access the /api/v1/readiness endpoint of Gemini service
    Then I should get 200 status code


  @smoketest @production
  Scenario: Check the 'liveness' REST API point for the Gemini service
    Given System is running
    When I access the /api/v1/liveness endpoint of Gemini service
    Then I should get 200 status code
