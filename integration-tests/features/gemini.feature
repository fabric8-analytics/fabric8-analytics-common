Feature: Gemini Analytics API

  # see https://github.com/fabric8-analytics/fabric8-gemini-server/issues/133
  #@smoketest @production
  #Scenario: Check the API entry point for the Gemini service
  #  Given System is running
  #  When I access the /api/v1 endpoint of Gemini service
  #  Then I should get 200 status code


  Scenario: Check the 'readiness' REST API point for the Gemini service
    Given System is running
     When I access the /api/v1/readiness endpoint of Gemini service
     Then I should get 200 status code


  Scenario: Check the 'liveness' REST API point for the Gemini service
    Given System is running
     When I access the /api/v1/liveness endpoint of Gemini service
     Then I should get 200 status code


  @production
  Scenario Outline: Check that the HTTP method is check properly on Gemini side for the /api/v1/readiness endpoint
    Given System is running
     When I call the /api/v1/readiness endpoint of Gemini service using the HTTP <method> method
     Then I should get 405 status code

     Examples: HTTP methods
     | method |
     | PUT    |
     | PATCH  |
     | DELETE |


  @production
  Scenario: Check that the HTTP method is check properly on Gemini side for the /api/v1/readiness endpoint
    Given System is running
     When I call the /api/v1/readiness endpoint of Gemini service using the HTTP HEAD method
     Then I should get 200 status code


  @production
  Scenario Outline: Check that the HTTP method is check properly on Gemini side for the /api/v1/liveness endpoint
    Given System is running
     When I call the /api/v1/liveness endpoint of Gemini service using the HTTP <method> method
     Then I should get 405 status code

     Examples: HTTP methods
     | method |
     | PUT    |
     | PATCH  |
     | DELETE |


  @production
  Scenario: Check that the HTTP method is check properly on Gemini side for the /api/v1/liveness endpoint
    Given System is running
     When I call the /api/v1/liveness endpoint of Gemini service using the HTTP HEAD method
     Then I should get 200 status code
  Scenario: Check the 'readiness' REST API point for the Gemini service with using authorization token
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I access the /api/v1/readiness endpoint of Gemini service with authorization token
     Then I should get 200 status code


  Scenario: Check the 'liveness' REST API entry point for the Gemini service with using authorization token
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I access the /api/v1/liveness endpoint of Gemini service with authorization token
     Then I should get 200 status code


  Scenario: Check the Gemini API /api/v1/register response
    Given Gemini service is running
      And Gemini service git url is https://github.com/jitpack/maven-simple
      And Gemini service git sha is 9466faa13d65044c8430b418327df826f13ca07a
    When I post to Gemini API api/v1/register
    Then I should get 401 status code
     And I should receive JSON response containing the error key
     And I should find the text "Authentication failed" stored under the key error
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I post to Gemini API api/v1/register with authorization token
    Then I should get 200 status code


  Scenario: Gemini /api/v1/report check when called without arguments
    Given Gemini service is running
     When I access the /api/v1/report endpoint of Gemini service without authorization token
     Then I should not get 200 status code


  Scenario: Gemini /api/v1/report check when called without arguments
    Given Gemini service is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I access the /api/v1/report endpoint of Gemini service with authorization token
     Then I should not get 200 status code


  Scenario: Check the Gemini API /api/v1/report response
    Given Gemini service is running
      And Gemini service git url is https://github.com/jitpack/maven-simple
      And Gemini service git sha is 9466faa13d65044c8430b418327df826f13ca07a
    When I get to Gemini API api/v1/report
    Then I should get 401 status code
     And I should receive JSON response containing the error key
     And I should find the text "Authentication failed" stored under the key error


  Scenario: Check the Gemini API /api/v1/report response
    Given Gemini service is running
      And Gemini service git url is https://github.com/jitpack/maven-simple
      And Gemini service git sha is 9466faa13d65044c8430b418327df826f13ca07a
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I get to Gemini API api/v1/report with authorization token
    Then I should get 200 status code
     And I should receive JSON response with the correct timestamp in attribute scanned_at
     And I should find the text "https://github.com/jitpack/maven-simple" stored under the key git_url
     And I should find the text "9466faa13d65044c8430b418327df826f13ca07a" stored under the key git_sha
     And I should find 0 CVEs for package junit:junit version 4.12 from ecosystem maven in dependencies
     And I should find 0 CVEs for package org.hamcrest:hamcrest-core version 1.3 from ecosystem maven in dependencies


  Scenario: Check the Gemini API /api/v1/user-repo/scan response
    Given Gemini service is running
        And Gemini service git url is https://github.com/jitpack/maven-simple
        And Gemini service git sha is 9466faa13d65044c8430b418327df826f13ca07a
    When I post to Gemini API /api/v1/user-repo/scan
    Then I should get 401 status code
     And I should receive JSON response containing the error key
     And I should find the text "Authentication failed" stored under the key error
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I post to Gemini API /api/v1/user-repo/scan with authorization token
    Then I should get 200 status code
     And I should find that the status is set to success in the JSON response
     And I should find the text "https://github.com/heroku/node-js-sample.git" stored under the key summary


  Scenario: Check the Gemini API /api/v1/user-repo/notify response
    Given Gemini service is running
        And Gemini service git url is https://github.com/jitpack/maven-simple
        And Gemini service git sha is 9466faa13d65044c8430b418327df826f13ca07a
        And Gemini service epv list is ["test:test:test"]
    When I post to Gemini API /api/v1/user-repo/notify
    Then I should get 401 status code
     And I should receive JSON response containing the error key
     And I should find the text "Authentication failed" stored under the key error
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I post to Gemini API /api/v1/user-repo/notify with authorization token
    Then I should get 200 status code
     And I should find that the status is set to success in the JSON response
     And I should find the text "https://github.com/jitpack/maven-simple" stored under the key summary


  Scenario: Check the Gemini API /api/v1/user-repo/drop
    Given Gemini service is running
        And Gemini service git url is https://github.com/jitpack/maven-simple
        And Gemini service git sha is 9466faa13d65044c8430b418327df826f13ca07a
    When I post to Gemini API /api/v1/user-repo/drop
    Then I should get 401 status code
     And I should receive JSON response containing the error key
     And I should find the text "Authentication failed" stored under the key error
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I post to Gemini API api/v1/user-repo/drop with authorization token
    Then I should get 200 status code
     And I should find that the status is set to success in the JSON response
     And I should find the text "Repository scan unsubscribed" stored under the key summary


  Scenario: Check that the 'register' REST API point for the Gemini service accepts POST method only
    Given System is running
     When I access the /api/v1/register endpoint of Gemini service
     Then I should not get 200 status code


  Scenario: Check that the 'user-repo/scan' REST API point for the Gemini service accepts POST method only
    Given System is running
     When I access the /api/v1/user-repo/scan endpoint of Gemini service
     Then I should not get 200 status code


  Scenario: Check that the 'user-repo/notify' REST API point for the Gemini service accepts POST method only
    Given System is running
     When I access the /api/v1/user-repo/notify endpoint of Gemini service
     Then I should not get 200 status code


  Scenario: Check that the 'user-repo/drop' REST API point for the Gemini service accepts POST method only
    Given System is running
     When I access the /api/v1/user-repo/drop endpoint of Gemini service
     Then I should not get 200 status code


  Scenario: Check the Gemini API endpoint 'stacks-report/list'
    Given System is running
     When I access the /api/v1/stacks-report/list endpoint of Gemini service for monthly report history
     Then I should get 200 status code
     Then I should get a valid report


  Scenario: Check the Gemini API endpoint 'stacks-report/report'
    Given System is running
     When I access the /api/v1/stacks-report/report endpoint of Gemini service for STAGE/monthly/201902.json report
     Then I should get 200 status code
     Then I should get a valid report