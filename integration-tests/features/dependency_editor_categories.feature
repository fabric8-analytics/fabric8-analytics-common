Feature: Dependency Editor Categories Search API behaviour

  Scenario: Check that the API entry point
    Given System is running
    When I access /api/v1/categories/springboot without valid access token
    Then I should get 401 status code


  @requires_authorization_token
  Scenario: Check the categories search for existing runtime springboot from the maven ecosystem
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I search for the runtime springboot
    Then I should get 200 status code
     And I should receive JSON response with the request_id
     And I should find categories
     And I should find categories with pkg_count and list of packages 

  @requires_authorization_token
  Scenario: Check the categories search for existing runtime vertx from the maven ecosystem
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I search for the runtime vertx
    Then I should get 200 status code
     And I should receive JSON response with the request_id
     And I should find categories
     And I should find categories with pkg_count and list of packages 

  @requires_authorization_token
    Scenario: Check the categories search for existing runtime wildflyswarm from the maven ecosystem
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I search for the runtime wildflyswarm
    Then I should get 200 status code
     And I should receive JSON response with the request_id
     And I should find categories
     And I should find categories with pkg_count and list of packages 

  @requires_authorization_token
    Scenario: Check the categories search for nonexisting runtime thronetail
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I search for the runtime thronetail
    Then I should get 200 status code
     And I should receive JSON response with the request_id
     And I should find categories are none
