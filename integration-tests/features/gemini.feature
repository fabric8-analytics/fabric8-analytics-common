Feature: Gemini Analytics API

#  Scenario: Check the Gemini API /api/v1/register response
#    Given Gemini service is running
#      And Gemini service git url is https://github.com/jitpack/maven-simple
#      And Gemini service git sha is 9466faa13d65044c8430b418327df826f13ca07a
#    When I post to Gemini API api/v1/register
#    Then I should get 401 status code
#     And I should receive JSON response containing the error key
#     And I should find the text "Authentication failed" stored under the key error
#    When I acquire the authorization token
#    Then I should get the proper authorization token
#    When I post to Gemini API api/v1/register with authorization token
#    Then I should get 200 status code
#
#
#  Scenario: Check the Gemini API /api/v1/report response
#    Given Gemini service is running
#      And Gemini service git url is https://github.com/jitpack/maven-simple
#      And Gemini service git sha is 9466faa13d65044c8430b418327df826f13ca07a
#    When I get to Gemini API api/v1/report
#    Then I should get 401 status code
#     And I should receive JSON response containing the error key
#     And I should find the text "Authentication failed" stored under the key error
#    When I acquire the authorization token
#    Then I should get the proper authorization token
#    When I get to Gemini API api/v1/report with authorization token
#    Then I should get 200 status code
#     And I should receive JSON response with the correct timestamp in attribute scanned_at
#     And I should find the text "https://github.com/jitpack/maven-simple" stored under the key git_url
#     And I should find the text "9466faa13d65044c8430b418327df826f13ca07a" stored under the key git_sha
#     And I should find 0 CVEs for package junit:junit version 4.12 from ecosystem maven in dependencies
#     And I should find 0 CVEs for package org.hamcrest:hamcrest-core version 1.3 from ecosystem maven in dependencies


  Scenario: Check the Gemini API /api/v1/user-repo/scan response
    Given Gemini service is running
        And Gemini service git url is https://github.com/jitpack/maven-simple
        And Gemini service git sha is 9466faa13d65044c8430b418327df826f13ca07a
        And Gemini service dependency files are set
    When I post to Gemini API /api/v1/user-repo/scan
    Then I should get 401 status code
     And I should receive JSON response containing the error key
     And I should find the text "Authentication failed" stored under the key error
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I post to Gemini API /api/v1/user-repo/scan with authorization token
    Then I should get 200 status code
     And I should find that the status is set to success in the JSON response
     And I should find the text "https://github.com/jitpack/maven-simple" stored under the key summary


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



  Scenario: Check the Gemini API /api/v1/user-repo/scan response
    Given Gemini service is running
        And Gemini service git url is https://github.com/jitpack/maven-simple
        And Gemini service git sha is 9466faa13d65044c8430b418327df826f13ca07a
        And Gemini service dependency files are set
    When I post to Gemini API /api/v1/user-repo/scan
    Then I should get 401 status code
     And I should receive JSON response containing the error key
     And I should find the text "Authentication failed" stored under the key error
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I post to Gemini API /api/v1/user-repo/scan with authorization token
    Then I should get 200 status code
     And I should find that the status is set to success in the JSON response
     And I should find the text "https://github.com/jitpack/maven-simple" stored under the key summary


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



  Scenario: Check the Gemini API /api/v1/user-repo/scan response
    Given Gemini service is running
        And Gemini service git url is https://github.com/jitpack/maven-simple
        And Gemini service git sha is 9466faa13d65044c8430b418327df826f13ca07a
        And Gemini service dependency files are set
    When I post to Gemini API /api/v1/user-repo/scan
    Then I should get 401 status code
     And I should receive JSON response containing the error key
     And I should find the text "Authentication failed" stored under the key error
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I post to Gemini API /api/v1/user-repo/scan with authorization token
    Then I should get 200 status code
     And I should find that the status is set to success in the JSON response
     And I should find the text "https://github.com/jitpack/maven-simple" stored under the key summary


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



  Scenario: Check the Gemini API /api/v1/user-repo/scan response
    Given Gemini service is running
        And Gemini service git url is https://github.com/jitpack/maven-simple
        And Gemini service git sha is 9466faa13d65044c8430b418327df826f13ca07a
        And Gemini service dependency files are set
    When I post to Gemini API /api/v1/user-repo/scan
    Then I should get 401 status code
     And I should receive JSON response containing the error key
     And I should find the text "Authentication failed" stored under the key error
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I post to Gemini API /api/v1/user-repo/scan with authorization token
    Then I should get 200 status code
     And I should find that the status is set to success in the JSON response
     And I should find the text "https://github.com/jitpack/maven-simple" stored under the key summary


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



  Scenario: Check the Gemini API /api/v1/user-repo/scan response
    Given Gemini service is running
        And Gemini service git url is https://github.com/jitpack/maven-simple
        And Gemini service git sha is 9466faa13d65044c8430b418327df826f13ca07a
        And Gemini service dependency files are set
    When I post to Gemini API /api/v1/user-repo/scan
    Then I should get 401 status code
     And I should receive JSON response containing the error key
     And I should find the text "Authentication failed" stored under the key error
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I post to Gemini API /api/v1/user-repo/scan with authorization token
    Then I should get 200 status code
     And I should find that the status is set to success in the JSON response
     And I should find the text "https://github.com/jitpack/maven-simple" stored under the key summary


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
