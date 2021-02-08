Feature: Stack analysis v2 API

  @sav2
  Scenario Outline: Check that the stack analysis REST API endpoint for <method> HTTP method without user key
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
  Scenario Outline: Check that the stack analysis REST API endpoint for <method> HTTP method with user key
    Given System is running
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
  Scenario Outline: Check that the REST API enpoint <endpoint> for the stack analyses
    Given System is running
    When I access <endpoint>
    Then I should get 401 status code

    Examples: Endpoints and token
    | endpoint                            |
    | /api/v2/stack-analyses              |
    | /api/v2/stack-analyses/external_id  |

  @sav2
  Scenario: Check that the API entry point without user key
    Given System is running
    When I send pypi package request with manifest valid_pylist.json to stack analysis v2 without valid user key
    Then I should get 403 status code

  @sav2
  Scenario: Check that the API entry point with invalid user key
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I send pypi package request with manifest valid_pylist.json to stack analysis v2 with invalid user key
    Then I should get 403 status code

  @sav2
  Scenario: Check that the API entry point with user key
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I wait 0 seconds
    When I send pypi package request with manifest valid_pylist.json to stack analysis v2 with valid user key
    Then I should get 200 status code

  @sav2
  Scenario Outline: Check the stack analysis v2 for <ecosystem> package and <manifest> manifest with valid user key
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I wait 0 seconds
    When I send <ecosystem> package request with manifest <manifest> to stack analysis v2 with valid user key
    Then I should get 200 status code
     And I should receive JSON response containing the status key
     And I should receive JSON response containing the id key
     And I should receive JSON response containing the submitted_at key
     And I should receive JSON response with the status key set to success
     And I should receive JSON response with the correct id
     And I should receive JSON response with the correct timestamp in attribute submitted_at

    Examples: Stack analyses POST params
     | ecosystem | manifest               |
     | pypi      | valid_pylist.json      |
     | npm       | valid_npmlist.json     |
     | maven     | valid_dependencies.txt |

  @sav2
  Scenario Outline: Check the stack analysis v2 with invalid request parameters
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I wait 0 seconds
    When I send <ecosystem> package request with manifest <manifest> to stack analysis v2 with valid user key
    Then I should get 400 status code

    Examples: Stack analyses POST params
     | ecosystem | manifest           |
     | None      | valid_pylist.json  |
     | npm       | None               |
     | None      | None               |
     | golang    | None               |

  @sav2
  Scenario Outline: Check the stack analysis v2 for invalid manifest data
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I send <ecosystem> package request with manifest <manifest> to stack analysis v2 with valid user key
    Then I should get 400 status code

    Examples: Stack analyses POST params
     | ecosystem | manifest               |
     | pypi      | valid_npmlist.json     |
     | npm       | valid_dependencies.txt |
     

  @sav2
  Scenario Outline: Check the stack analysis v2 request and response for proper data
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I wait 0 seconds
    When I send <ecosystem> package request with manifest <manifest> to stack analysis v2 with valid user key
    Then I should get 200 status code
    When I wait for stack analysis v2 to finish with user key
    Then I should find the external request id equals to id returned by stack analysis v2 post request
     And I should get stack analyses v2 response with all attributes

    Examples: Stack analyses POST params
     | ecosystem | manifest               |
     | pypi      | valid_pylist.json      |
     | npm       | valid_npmlist.json     |
     | maven     | valid_dependencies.txt |

  @sav2
  Scenario Outline: Check the stack analysis v2 with known package data
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I wait 0 seconds
    When I send <ecosystem> package request with manifest <manifest> to stack analysis v2 with valid user key
    Then I should get 200 status code
    When I wait for stack analysis v2 to finish with user key
    Then I should find the value <field> under the path <field_path> in the JSON response
     And I should find the value <version> under the path <version_path> in the JSON response

    Examples: Stack analyses POST params
     | ecosystem | manifest               | field               | field_path                    | version | version_path                    |
     | pypi      | requests_2_20_0.json   | requests            | analyzed_dependencies/0/name  | 2.20.0  | analyzed_dependencies/0/version |
     | npm       | npm_svg_2_0_2.json     | svg.filter.js       | analyzed_dependencies/0/name  | 2.0.2   | analyzed_dependencies/0/version |
     | maven     | vertx_dependencies.txt | io.vertx:vertx-core | analyzed_dependencies/0/name  | 3.4.1   | analyzed_dependencies/0/version |

  @sav2 @skip
  Scenario: Check the outlier record for a known package
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I send maven package request with manifest springboot_dependencies.txt to stack analysis v2 with valid user key
    Then I should get 200 status code
    When I wait for stack analysis v2 to finish with user key
    Then I should get stack analyses v2 response with all attributes
     And I should find the proper outlier record for the org.springframework:spring-websocket component for stack analyses v2

  @sav2
  Scenario Outline: Check stack ananlyses v2 for vulnerabilities count for <ecosystem> with <manifest> manifest
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I send <ecosystem> package request with manifest <manifest> to stack analysis v2 with valid user key
    Then I should get 200 status code
    When I wait for stack analysis v2 to finish with user key
    Then I should get <public_count> public vulnerabilities for <component>
     And I should get <private_count> private vulnerabilities for <component>
     And I should get <transitive_count> transitive vulnerabilities for <component>

    Examples: Stack analyses params
     | ecosystem | manifest                      | component             | public_count | private_count  | transitive_count |
     | pypi      | fastlog_urllib_requests.json  | requests              | 1            | 0              | 0                |
     | npm       | npm_50_direct_799_tr.json     | npm                   | 3            | 0              | 0                |
     | maven     | vertx_dependencies.txt        | io.vertx:vertx-core   | 2            | 0              | 0                |
