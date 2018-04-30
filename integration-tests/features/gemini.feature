Feature: Gemini Analytics API

  Scenario: Check the Gemini API /api/v1/register response
    Given gemini service is running
    Given gemini service git url is https://github.com/jitpack/maven-simple
    Given gemini service git sha is 9466faa13d65044c8430b418327df826f13ca07a
    When I post to api/v1/register
    Then I should get 401 status code
    When I post to api/v1/register with authorization token
    Then I should receive a valid register response

  Scenario: Check the Gemini API /api/v1/report response
    Given gemini service is running
    Given gemini service git url is https://github.com/jitpack/maven-simple
    Given gemini service git sha is 9466faa13d65044c8430b418327df826f13ca07a
    When I get gemini API api/v1/report
    Then I should get 401 status code
    When I get gemini API api/v1/report with authorization token
    Then I should receive a valid report