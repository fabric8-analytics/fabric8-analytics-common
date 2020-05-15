Feature: Component Search API Through 3Scale Gateway

  Scenario: Check the ability to get the proper user key
    Given System is running
    Given Three scale preview service is running
    When I wait 5 seconds
    When I acquire the use_key for 3scale
    Then I should get the proper user_key

  Scenario: Check the component analyses functionality for existent npm dependency through 3scale gateway
    Given System is running
    Given Three scale preview service is running
    When I wait 60 seconds
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I start component analyses npm/sequence/2.2.0 with user_key
    Then I should get 200 status code

  Scenario: Check the component analyses functionality for improper ecosystem
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I start component analyses foobar/sequence/2.2.0 with user_key
    Then I should not get 200 status code

  Scenario: Check the component analyses functionality for improper ecosystem
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I start component analyses XYZZY/sequence/2.2.0 with user_key
    Then I should not get 200 status code

  @skip
  Scenario: Check that the component-analyses returns limits exceeded for npm ecosystem
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I start component analyses npm/sequence/2.2.0 40 times in a minute with user_key
    Then I should get 429 status code
     And I should get Limits exceeded text response
