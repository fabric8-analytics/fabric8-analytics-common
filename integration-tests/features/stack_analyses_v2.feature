Feature: Stack analysis v2 API

  @sav2
  Scenario: Check that the REST API point for the stack analyses accepts without user key
    Given System is running
    When I access /api/v2/stack-analyses
    Then I should get 401 status code

  @sav2
  Scenario Outline: Check that the stack analysis REST API endpoint requires user key even for improper HTTP methods
    Given System is running
    When I access the /api/v2/stack-analyses endpoint using the HTTP <method> method without user key
    Then I should not get 200 status code

    Examples: HTTP methods
     | method |
     | GET    |
     | HEAD   |
     | PUT    |
     | DELETE |

  @sav2
  Scenario Outline: Check that the stack analysis REST API endpoint does not accept any HTTP method other than POST
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I access the /api/v2/stack-analyses endpoint using the HTTP <method> method with user key
    Then I should not get 200 status code

    Examples: HTTP methods
     | method |
     | GET    |
     | HEAD   |
     | PUT    |
     | DELETE |

  @sav2
  Scenario: Check that the REST API point for the stack analyses with external ID accepts without user key
    Given System is running
    When I access /api/v2/stack-analyses/external-id
    Then I should get 401 status code

  @sav2
  Scenario Outline: Check that the stack analysis REST API endpoint requires user key even for improper HTTP methods
    Given System is running
    When I access the /api/v2/stack-analyses/external-id endpoint using the HTTP <method> method without user key
    Then I should not get 200 status code

    Examples: HTTP methods
     | method |
     | GET    |
     | HEAD   |
     | PUT    |
     | DELETE |

  @sav2
  Scenario Outline: Check that the stack analysis REST API endpoint does not accept any HTTP method other than POST
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I access the /api/v2/stack-analyses/external-id endpoint using the HTTP <method> method with user key
    Then I should not get 200 status code

    Examples: HTTP methods
     | method |
     | GET    |
     | HEAD   |
     | PUT    |
     | DELETE |

  @sav2
  Scenario: Check that the API entry point without user key
    Given System is running
    When I send pypi package request with manifest valid_manifests/pylist.json to stack analysis v2 without valid user key
    Then I should get 403 status code

  @sav2
  Scenario: Check that the API entry point with invalid user key
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I send pypi package request with manifest valid_manifests/pylist.json to stack analysis v2 with invalid user key
    Then I should get 403 status code

  @sav2
  Scenario: Check that the API entry point with user key
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I send pypi package request with manifest valid_manifests/pylist.json to stack analysis v2 with valid user key
    Then I should get 200 status code

  @sav2
  Scenario Outline: Check the stack analysis v2 response when called with proper user key
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I send <ecosystem> package request with manifest <manifest> to stack analysis v2 with valid user key
    Then I should get 200 status code
     And I should receive JSON response containing the status key
     And I should receive JSON response containing the id key
     And I should receive JSON response containing the submitted_at key
     And I should receive JSON response with the status key set to success
     And I should receive JSON response with the correct id
     And I should receive JSON response with the correct timestamp in attribute submitted_at

    Examples: Stack analyses POST params
     | ecosystem | manifest                         |
     | pypi      | valid_manifests/pylist.json      |
     | npm       | valid_manifests/npmlist.json     |
     | maven     | valid_manifests/dependencies.txt |

  @sav2
  Scenario Outline: Check the stack analysis v2 response for missing data when called with proper user key
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I send <ecosystem> package request with manifest <manifest> to stack analysis v2 with valid user key
    Then I should get 400 status code

    Examples: Stack analyses POST params
     | ecosystem | manifest                     |
     | None      | valid_manifests/pylist.json  |
     | npm       | None                         |
     | None      | None                         |

  @sav2
  Scenario Outline: Check the stack analysis v2 response for invalid manifest data when called with proper user key
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I send <ecosystem> package request with manifest <manifest> to stack analysis v2 with valid user key
    Then I should get 400 status code

    Examples: Stack analyses POST params
     | ecosystem | manifest                         |
     | pypi      | valid_manifests/npmlist.json     |
     | npm       | valid_manifests/dependencies.txt |

  @sav2
  Scenario Outline: Check the stack analysis v2 request and response when called with proper user key
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I send <ecosystem> package request with manifest <manifest> to stack analysis v2 with valid user key
    Then I should get 200 status code
    When I wait for stack analysis v2 to finish with user key
    Then I should find the external request id equals to id returned by stack analysis v2 post request
     And I should get stack analyses v2 response with all attributes

    Examples: Stack analyses POST params
     | ecosystem | manifest                         |
     | pypi      | valid_manifests/pylist.json      |
     | npm       | valid_manifests/npmlist.json     |
     | maven     | valid_manifests/dependencies.txt |

  @sav2
  Scenario Outline: Check the stack analysis v2 with known package data
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I send <ecosystem> package request with manifest <manifest> to stack analysis v2 with valid user key
    Then I should get 200 status code
    When I wait for stack analysis v2 to finish with user key
    Then I should find the value <field> under the path <field_path> in the JSON response
     And I should find the value <version> under the path <version_path> in the JSON response

    Examples: Stack analyses POST params
     | ecosystem | manifest             | field         | field_path                    | version | version_path                    |
     | pypi      | pytest_2_0_0.json    | pytest        | analyzed_dependencies/0/name  | 2.0.0   | analyzed_dependencies/0/version |
     | pypi      | requests_2_20_0.json | requests      | analyzed_dependencies/0/name  | 2.20.0  | analyzed_dependencies/0/version |
     | npm       | npm_sfj_2_0_2.json   | svg.filter.js | analyzed_dependencies/0/name  | 2.0.2   | analyzed_dependencies/0/version |

  @sav2
  Scenario: Check the outlier record
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I send maven package request with manifest springboot_dependencies.txt to stack analysis v2 with valid user key
    Then I should get 200 status code
    When I wait for stack analysis v2 to finish with user key
    Then I should get stack analyses v2 response with all attributes
     And I should find the proper outlier record for the org.springframework:spring-websocket component for stack analyses v2
