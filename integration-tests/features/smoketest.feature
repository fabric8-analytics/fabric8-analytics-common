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

  Scenario: Check the Gemini API /api/v1/register response
    Given Gemini service is running
      And Gemini service git url is https://github.com/jitpack/maven-simple
      And Gemini service git sha is 9466faa13d65044c8430b418327df826f13ca07a
    When I post to Gemini API api/v1/register
    Then I should get 401 status code


#  @smoketest @production
#  Scenario: Check the jobs API entry point
#    Given System is running
#    When I access /api/v1/readiness
#    Then I should get 200 status code
#
#  @smoketest @production
#  Scenario: Check the jobs API entry point
#    Given System is running
#    When I access jobs API /api/v1
#    Then I should get 200 status code
#
#  @smoketest @production
#  Scenario: Check the jobs API entry point
#    Given System is running
#    When I access jobs API /api/v1/readiness
#    Then I should get 200 status code
#
#  @smoketest @production
#  Scenario: Check the jobs API entry point
#    Given System is running
#    When I access jobs API /api/v1/liveness
#    Then I should get 200 status code
#
#  @jobs.requires_auth
#  Scenario: Check the jobs API entry point
#    Given System is running
#    When I access jobs API /api/v1/service/state
#    Then I should get 200 status code
#
#  @smoketest @production
#  Scenario: Basic check the endpoint for analyses report output w/o authorization token
#    Given System is running
#    Given Jobs debug API is running
#    When I ask for analyses report for ecosystem maven
#    Then I should get 401 status code
#
#  @smoketest @production
#  Scenario: Basic check the endpoint for analyses report output w/o authorization token
#    Given System is running
#    Given Jobs debug API is running
#    When I ask for analyses report for ecosystem npm
#    Then I should get 401 status code
#
#  @smoketest @production
#  Scenario: Basic check the endpoint for analyses report output w/o authorization token
#    Given System is running
#    Given Jobs debug API is running
#    When I ask for analyses report for ecosystem pypi
#    Then I should get 401 status code
#
#  @smoketest @production
#  Scenario: Basic check the endpoint for analyses report output w/o authorization token
#    Given System is running
#    Given Jobs debug API is running
#    When I ask for analyses report for ecosystem nuget
#    Then I should get 401 status code

