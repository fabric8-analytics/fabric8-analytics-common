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
  Scenario: Check the system/version response
    Given System is running
    When I access /api/v1/system/version/
    Then I should get 200 status code
     And I should receive JSON response containing the commit_hash key
     And I should receive JSON response containing the committed_at key
     And I should find the correct commit hash in the JSON response
     And I should find the correct committed at timestamp in the JSON response

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
         |/api/v1/stack-analyses|
         |/api/v1/stack-analyses/<external_request_id>|
         |/api/v1/submit-feedback|
         |/api/v1/system/version|
         |/api/v1/user-feedback|
         |/api/v1/user-intent|
         |/api/v1/user-intent/<user>/<ecosystem>|
         |/api/v1/master-tags/<ecosystem>|
         |/api/v1/set-tags|
         |/api/v1/categories/<runtime>|
         |/api/v1/depeditor-analyses|
         |/api/v1/depeditor-cve-analyses|
         |/api/v1/get-core-dependencies/<runtime>|
         |/api/v1/empty-booster|
         |/api/v1/recommendation_feedback/<ecosystem>|
         |/api/v1/cves/bydate/<modified_date>/<ecosystem>|


  @production
  Scenario Outline: Check that the HTTP method is check properly on server side for the /api/v1/ endpoint
    Given System is running
     When I call the /api/v1/ endpoint using the HTTP <method> method
     Then I should get 405 status code

     Examples: HTTP methods
         | method |
         | PUT    |
         | PATCH  |
         | DELETE |


  @production
  Scenario: Check that the HTTP method is check properly on server side for the /api/v1/ endpoint
    Given System is running
     When I call the /api/v1/ endpoint using the HTTP HEAD method
     Then I should get 200 status code


  @production
  Scenario Outline: Check that the HTTP method is check properly on server side for the /api/v1/readiness endpoint
    Given System is running
     When I call the /api/v1/readiness endpoint using the HTTP <method> method
     Then I should get 405 status code

     Examples: HTTP methods
         | method |
         | PUT    |
         | PATCH  |
         | DELETE |


  @production
  Scenario: Check that the HTTP method is check properly on server side for the /api/v1/readiness endpoint
    Given System is running
     When I call the /api/v1/readiness endpoint using the HTTP HEAD method
     Then I should get 200 status code


  @production
  Scenario Outline: Check that the HTTP method is check properly on server side for the /api/v1/liveness endpoint
    Given System is running
     When I call the /api/v1/liveness endpoint using the HTTP <method> method
     Then I should get 405 status code

     Examples: HTTP methods
         | method |
         | PUT    |
         | PATCH  |
         | DELETE |


  @production
  Scenario: Check that the HTTP method is check properly on server side for the /api/v1/liveness endpoint
    Given System is running
     When I call the /api/v1/liveness endpoint using the HTTP HEAD method
     Then I should get 200 status code


  Scenario Outline: Check that the HTTP method is check properly on server side for the /api/v1/system/version
    Given System is running
     When I access /api/v1/system/version/
     When I call the /api/v1/system/version endpoint using the HTTP <method> method
     Then I should get 405 status code

     Examples: HTTP methods
         | method |
         | PUT    |
         | PATCH  |
         | DELETE |


  @production
  Scenario: Check that the HTTP method is check properly on server side for the /api/v1/system/version
    Given System is running
     When I access /api/v1/system/version/
     When I call the /api/v1/system/version endpoint using the HTTP HEAD method
     Then I should get 200 status code

  @production
  Scenario: Check the /api/v1/submit-feedback response with invalid payload
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I access /api/v1/submit-feedback without valid values
    Then I should get 400 status code

  @production
  Scenario: Check the /api/v1/submit-feedback response with empty payload
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I access /api/v1/submit-feedback with empty payload
    Then I should get 400 status code

  @production
  Scenario: Check the /api/v1/submit-feedback response without any payload
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I access /api/v1/submit-feedback without any payload
    Then I should get 400 status code
