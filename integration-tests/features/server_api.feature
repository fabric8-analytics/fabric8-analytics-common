Feature: Server API

  @production
  Scenario: Check the API entry point
    Given System is running
    When I access /api/v1/
    Then I should get 200 status code
    Then I should receive JSON response containing the paths key

  @production
  Scenario: Check the /api/v1/readiness response
    Given System is running
    When I access /api/v1/readiness
    Then I should get 200 status code
    Then I should receive empty JSON response

  @production
  Scenario: Check the /api/v1/liveness response
    Given System is running
    When I wait 20 seconds
    When I access /api/v1/liveness
    Then I should get 200 status code
    Then I should receive empty JSON response

  @production
  Scenario: Check the service/state response
    Given System is running
    When I access /api/v1/system/version/
    Then I should get 200 status code
    Then I should receive JSON response containing the commit_hash key
    Then I should receive JSON response containing the committed_at key

  @production
  Scenario Outline: Check the existence of all expected REST API endpoints
    Given System is running
    When I access /api/v1/
    Then I should get 200 status code
    Then I should receive JSON response containing the paths key
     And I should find the endpoint <endpoint> in the list of supported endpoints

     Examples: endpoints
         |endpoint|
         |/api/v1|
         |/api/v1/component-analyses/<ecosystem>/<package>/<version>|
         |/api/v1/component-search/<package>|
         |/api/v1/generate-file|
         |/api/v1/get-next-component/<ecosystem>|
         |/api/v1/master-tags/<ecosystem>|
         |/api/v1/set-tags|
         |/api/v1/stack-analyses|
         |/api/v1/stack-analyses/<external_request_id>|
         |/api/v1/submit-feedback|
         |/api/v1/system/version|
         |/api/v1/user-feedback|
         |/api/v1/user-intent|
         |/api/v1/user-intent/<user>/<ecosystem>|

  @production
  Scenario: Check the /api/v1/submit-feedback response
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I access /api/v1/submit-feedback without valid values
    Then I should get 400 status code
