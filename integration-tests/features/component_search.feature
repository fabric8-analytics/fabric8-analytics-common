Feature: Component search API

  Scenario: Check the component search functionality for nonexistent component from npm ecosystem
    Given System is running
    Given Component search service is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I search for component unknown-component with authorization token
    Then I should not find the analysis for the component unknown-component from ecosystem npm

  Scenario: Check the component search functionality for nonexistent component from Maven ecosystem
    Given System is running
    Given Component search service is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I search for component unknown-component with authorization token
    Then I should not find the analysis for the component unknown-component from ecosystem maven

  Scenario: Check the component search functionality for nonexistent component from PyPi ecosystem
    Given System is running
    Given Component search service is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I search for component unknown-component with authorization token
    Then I should not find the analysis for the component unknown-component from ecosystem pypi

  Scenario: Check the component search functionality for existing component from the npm ecosystem
    Given System is running
    Given Component search service is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I search for component wisp with authorization token
    Then I should find the analysis for the component wisp from ecosystem npm

  Scenario: Check the component search functionality for existing component from the pypi ecosystem
    Given System is running
    Given Component search service is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I search for component clojure_py with authorization token
    Then I should find the analysis for the component clojure_py from ecosystem pypi

  Scenario: Check the component search functionality for existing component from the maven ecosystem
    Given System is running
    Given Component search service is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I search for component vertx with authorization token
    Then I should find the analysis for the component vertx from ecosystem maven

  Scenario Outline: Check the component search functionality for nonexistent component from npm ecosystem
    Given System is running
    Given Component search service is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I access the /api/v1/component-search endpoint using the HTTP <method> method and authorization token
     Then I should get <status> status code

     Examples: HTTP methods and expected status codes
     | method | status |
     | GET    | 404    |
     | HEAD   | 404    |
     | PUT    | 405    |
     | POST   | 405    |
     | DELETE | 405    |

  Scenario Outline: Check the component search functionality for nonexistent component from npm ecosystem
    Given System is running
    Given Component search service is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I access the /api/v1/component-search/wisp endpoint using the HTTP <method> method and authorization token
     Then I should get <status> status code

     Examples: HTTP methods and expected status codes
     | method | status |
     | GET    | 200    |
     | HEAD   | 200    |
     | PUT    | 405    |
     | POST   | 405    |
     | DELETE | 405    |
