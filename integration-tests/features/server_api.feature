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
         |/api/v1/schemas|
         |/api/v1/schemas/<collection>|
         |/api/v1/schemas/<collection>/<name>|
         |/api/v1/schemas/<collection>/<name>/<version>|
         |/api/v1/set-tags|
         |/api/v1/stack-analyses|
         |/api/v1/stack-analyses/<external_request_id>|
         |/api/v1/submit-feedback|
         |/api/v1/system/version|
         |/api/v1/user-feedback|
         |/api/v1/user-intent|
         |/api/v1/user-intent/<user>/<ecosystem>|

  @production
  Scenario Outline: Check the /api/v1/schemas response, API endpoints
    Given System is running
    When I access /api/v1/schemas/
    Then I should get 200 status code
    Then I should receive JSON response containing the api key
     And I should find the schema <schema> version <version> in the list of supported schemas for API calls

     Examples: schemas
         |schema|version|
         |analyses_graphdb|1-0-0|
         |analyses_graphdb|1-1-0|
         |analyses_graphdb|1-2-0|
         |component_analyses|1-0-0|
         |component_analyses|1-0-1|
         |component_analyses|1-1-0|
         |component_analyses|1-1-2|
         |component_analyses|1-1-3|
         |stack_analyses|1-0-0|
         |stack_analyses|1-1-0|
         |stack_analyses|1-2-0|
         |stack_analyses|2-0-0|
         |stack_analyses|2-0-1|
         |stack_analyses|2-0-2|
         |stack_analyses|2-0-3|
         |stack_analyses|2-1-0|
         |stack_analyses|2-1-1|
         |stack_analyses|2-1-2|
         |stack_analyses|2-1-3|
         |stack_analyses|2-1-4|
         |stack_analyses|2-2-0|
         |version_range_resolver|1-0-0|

  @production
  Scenario Outline: Check the /api/v1/schemas response, component analyses
    Given System is running
    When I access /api/v1/schemas/
    Then I should get 200 status code
    Then I should receive JSON response containing the api key
     And I should find the schema <schema> version <version> in the list of component analyses schemas

     Examples: schemas
         |schema|version|
         |binary_data|1-0-0|
         |code_metrics|1-0-0|
         |crypto_algorithms|1-0-0|
         |dependency_snapshot|1-0-0|
         |digests|1-0-0|
         |github_details|1-0-0|
         |github_details|1-0-1|
         |github_details|1-0-2|
         |github_details|1-0-3|
         |github_details|1-0-4|
         |github_details|2-0-0|
         |github_details|2-0-1|
         |keywords_tagging|1-0-0|
         |languages|1-0-0|
         |metadata|1-0-0|
         |metadata|1-0-1|
         |metadata|1-1-0|
         |metadata|2-0-0|
         |metadata|2-1-0|
         |metadata|2-1-1|
         |metadata|3-0-0|
         |metadata|3-0-1|
         |metadata|3-1-0|
         |metadata|3-1-1|
         |metadata|3-2-0|
         |package_keywords_tagging|1-0-0|
         |security_issues|1-0-0|
         |security_issues|2-0-0|
         |security_issues|3-0-0|
         |security_issues|3-0-1|
         |source_licenses|1-0-0|
         |source_licenses|2-0-0|
         |source_licenses|3-0-0|

  @production
  Scenario Outline: Check the /api/v1/schemas/api response
    Given System is running
    When I access /api/v1/schemas/api
    Then I should get 200 status code
    Then I should find the schema <schema> version <version> in the list of supported schemas

     Examples: schemas
         |schema|version|
         |analyses_graphdb|1-0-0|
         |analyses_graphdb|1-1-0|
         |analyses_graphdb|1-2-0|
         |component_analyses|1-0-0|
         |component_analyses|1-0-1|
         |component_analyses|1-1-0|
         |component_analyses|1-1-2|
         |component_analyses|1-1-3|
         |stack_analyses|1-0-0|
         |stack_analyses|1-1-0|
         |stack_analyses|1-2-0|
         |stack_analyses|2-0-0|
         |stack_analyses|2-0-1|
         |stack_analyses|2-0-2|
         |stack_analyses|2-0-3|
         |stack_analyses|2-1-0|
         |stack_analyses|2-1-1|
         |stack_analyses|2-1-2|
         |stack_analyses|2-1-3|
         |stack_analyses|2-1-4|
         |stack_analyses|2-2-0|
         |version_range_resolver|1-0-0|

  @production
  Scenario Outline: Check the /api/v1/schemas/component_analyses response
    Given System is running
    When I access /api/v1/schemas/component_analyses
    Then I should get 200 status code
    Then I should find the schema <schema> version <version> in the list of supported schemas

     Examples: schemas
         |schema|version|
         |binary_data|1-0-0|
         |code_metrics|1-0-0|
         |crypto_algorithms|1-0-0|
         |dependency_snapshot|1-0-0|
         |digests|1-0-0|
         |github_details|1-0-0|
         |github_details|1-0-1|
         |github_details|1-0-2|
         |github_details|1-0-3|
         |github_details|1-0-4|
         |github_details|2-0-0|
         |github_details|2-0-1|
         |keywords_tagging|1-0-0|
         |languages|1-0-0|
         |metadata|1-0-0|
         |metadata|1-0-1|
         |metadata|1-1-0|
         |metadata|2-0-0|
         |metadata|2-1-0|
         |metadata|2-1-1|
         |metadata|3-0-0|
         |metadata|3-0-1|
         |metadata|3-1-0|
         |metadata|3-1-1|
         |metadata|3-2-0|
         |package_keywords_tagging|1-0-0|
         |security_issues|1-0-0|
         |security_issues|2-0-0|
         |security_issues|3-0-0|
         |security_issues|3-0-1|
         |source_licenses|1-0-0|
         |source_licenses|2-0-0|
         |source_licenses|3-0-0|

  @production
  Scenario Outline: Check the /api/v1/schemas/api/<name> response
    Given System is running
    When I access /api/v1/schemas/api/<schema>
    Then I should get 200 status code
    Then I should find the schema version <version> in the list of schema versions

     Examples: schemas
         |schema|version|
         |analyses_graphdb|1-0-0|
         |analyses_graphdb|1-1-0|
         |analyses_graphdb|1-2-0|
         |component_analyses|1-0-0|
         |component_analyses|1-0-1|
         |component_analyses|1-1-0|
         |component_analyses|1-1-2|
         |component_analyses|1-1-3|
         |stack_analyses|1-0-0|
         |stack_analyses|1-1-0|
         |stack_analyses|1-2-0|
         |stack_analyses|2-0-0|
         |stack_analyses|2-0-1|
         |stack_analyses|2-0-2|
         |stack_analyses|2-0-3|
         |stack_analyses|2-1-0|
         |stack_analyses|2-1-1|
         |stack_analyses|2-1-2|
         |stack_analyses|2-1-3|
         |stack_analyses|2-1-4|
         |stack_analyses|2-2-0|
         |version_range_resolver|1-0-0|

  @production
  Scenario Outline: Check the /api/v1/schemas/<collection>/<schema>/<version> response
    Given System is running
    When I access /api/v1/schemas/<collection>/<schema>/<version>
    Then I should get 200 status code
     And I should find valid schema in the server response

     Examples: schemas
         |collection|schema|version|
         |api|analyses_graphdb|1-0-0|
         |api|analyses_graphdb|1-1-0|
         |api|analyses_graphdb|1-2-0|
         |api|component_analyses|1-0-0|
         |api|component_analyses|1-0-1|
         |api|component_analyses|1-1-0|
         |api|component_analyses|1-1-2|
         |api|component_analyses|1-1-3|
         |api|stack_analyses|1-0-0|
         |api|stack_analyses|1-1-0|
         |api|stack_analyses|1-2-0|
         |api|stack_analyses|2-0-0|
         |api|stack_analyses|2-0-1|
         |api|stack_analyses|2-0-2|
         |api|stack_analyses|2-0-3|
         |api|stack_analyses|2-1-0|
         |api|stack_analyses|2-1-1|
         |api|stack_analyses|2-1-2|
         |api|stack_analyses|2-1-3|
         |api|stack_analyses|2-1-4|
         |api|stack_analyses|2-2-0|
         |api|version_range_resolver|1-0-0|
         |component_analyses|binary_data|1-0-0|
         |component_analyses|code_metrics|1-0-0|
         |component_analyses|crypto_algorithms|1-0-0|
         |component_analyses|dependency_snapshot|1-0-0|
         |component_analyses|digests|1-0-0|
         |component_analyses|github_details|1-0-0|
         |component_analyses|github_details|1-0-1|
         |component_analyses|github_details|1-0-2|
         |component_analyses|github_details|1-0-3|
         |component_analyses|github_details|1-0-4|
         |component_analyses|github_details|2-0-0|
         |component_analyses|github_details|2-0-1|
         |component_analyses|keywords_tagging|1-0-0|
         |component_analyses|languages|1-0-0|
         |component_analyses|metadata|1-0-0|
         |component_analyses|metadata|1-0-1|
         |component_analyses|metadata|1-1-0|
         |component_analyses|metadata|2-0-0|
         |component_analyses|metadata|2-1-0|
         |component_analyses|metadata|2-1-1|
         |component_analyses|metadata|3-0-0|
         |component_analyses|metadata|3-0-1|
         |component_analyses|metadata|3-1-0|
         |component_analyses|metadata|3-1-1|
         |component_analyses|metadata|3-2-0|
         |component_analyses|package_keywords_tagging|1-0-0|
         |component_analyses|security_issues|1-0-0|
         |component_analyses|security_issues|2-0-0|
         |component_analyses|security_issues|3-0-0|
         |component_analyses|security_issues|3-0-1|
         |component_analyses|source_licenses|1-0-0|
         |component_analyses|source_licenses|2-0-0|
         |component_analyses|source_licenses|3-0-0|

  @production
  Scenario: Check the /api/v1/submit-feedback response
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I access /api/v1/submit-feedback without valid values
    Then I should get 400 status code
