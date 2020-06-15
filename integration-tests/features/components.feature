Feature: Components API V1

  @production
  Scenario: Check the API entry point
    Given System is running
     When I access /api/v1/
     Then I should get 200 status code

  @production
  Scenario: Check that the component analyses API entry point make sure resources are specified
    Given System is running
     When I access /api/v1/component-analyses/
     Then I should get 404 status code

  @production
  Scenario: Check that component analyses endpoint checks if all resources are specified
    Given System is running
     When I access /api/v1/component-analyses
     Then I should get 404 status code
     When I access /api/v1/component-analyses/npm
     Then I should get 404 status code
     When I access /api/v1/component-analyses/npm/component
     Then I should get 404 status code

  @production
  Scenario: Check if component analysis requires authorization
    Given System is running
     When I start analysis for component npm/sequence/2.2.0
     Then I should get 401 status code

  Scenario: Check if component analysis is accessible via API
    Given System is running
    Given Three scale preview service is running
    When I wait 1 seconds
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
     When I start component analyses npm/sequence/2.2.0 with user_key
     Then I should get 200 status code

  Scenario: Check if component analysis returns error code for unknown ecosystem
    Given System is running
    Given Three scale preview service is running
    When I wait 1 seconds
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
     When I start component analyses foobar/sequence/2.2.0 with user_key
     Then I should not get 200 status code

  Scenario: Check if component analysis returns error code for unknown ecosystem
    Given System is running
    Given Three scale preview service is running
    When I wait 1 seconds
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
     When I start component analyses XYZZY/sequence/2.2.0 with user_key
     Then I should not get 200 status code

  @production
  Scenario Outline: Check that the HTTP method is checked properly on the server side for the /api/v1/component-analyses endpoint
    Given System is running
     When I call the /api/v1/component-analyses/ endpoint using the HTTP <method> method
     Then I should get 405 status code

     Examples: HTTP methods
     | method |
     | PUT    |
     | PATCH  |
     | DELETE |


  @production
  Scenario Outline: Check that the HTTP method is checked properly on the server side for the /api/v1/component-analyses endpoint
    Given System is running
     When I call the /api/v1/component-analyses/npm/sequence/2.2.0 endpoint using the HTTP <method> method
     Then I should get 405 status code

     Examples: HTTP methods
     | method |
     | PUT    |
     | PATCH  |
     | DELETE |


  @production
  Scenario Outline: Check that the HTTP method is checked properly on the server side for the /api/v1/component-analyses endpoint
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I call the /api/v1/component-analyses/ endpoint using the HTTP <method> method and authorization token
     Then I should get 405 status code

     Examples: HTTP methods
     | method |
     | PUT    |
     | PATCH  |
     | DELETE |


  @production
  Scenario Outline: Check that the HTTP method is checked properly on the server side for the /api/v1/component-analyses endpoint
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I call the /api/v1/component-analyses/npm/sequence/2.2.0 endpoint using the HTTP <method> method and authorization token
     Then I should get 405 status code

     Examples: HTTP methods
     | method |
     | PUT    |
     | PATCH  |
     | DELETE |


  Scenario: Check the HTTP HEAD method for the component analyses endpoint and proper resource specification
    Given System is running
     When I access the /api/v1/component-analyses/npm/sequence/2.2.0 endpoint using the HTTP HEAD method
     Then I should get 401 status code
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I access the /api/v1/component-analyses/npm/sequence/2.2.0 endpoint using the HTTP HEAD method
     Then I should get 401 status code
     When I access the /api/v1/component-analyses/npm/sequence/2.2.0 endpoint using the HTTP HEAD method and authorization token
     Then I should get 200 status code


  @requires_authorization_token @production
  Scenario Outline: Check the HTTP HEAD method for the component analyses endpoint and incomplete resource specification
    Given System is running
     When I access the /api/v1/component-analyses<resource> endpoint using the HTTP HEAD method
     Then I should get 404 status code

    Examples: resource paths
    | resource      |
    |               |
    |/              |
    |/npm           |
    |/npm/          |
    |/npm/component |
    |/npm/component/|
