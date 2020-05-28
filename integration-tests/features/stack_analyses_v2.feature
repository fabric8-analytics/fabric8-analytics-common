Feature: Stack analysis v2 API

  @sav2
  Scenario: Check that the REST API point for the stack analyses accepts authorization tokens
    Given System is running
     When I access /api/v2/stack-analyses
     Then I should get 401 status code

  @sav2
  Scenario Outline: Check that the stack analysis REST API endpoint requires authorization token even for improper HTTP methods
    Given System is running
     When I access the /api/v2/stack-analyses endpoint using the HTTP <method> method
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
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I access the /api/v2/stack-analyses endpoint using the HTTP <method> method and authorization token
     Then I should not get 200 status code

     Examples: HTTP methods
     | method |
     | GET    |
     | HEAD   |
     | PUT    |
     | DELETE |

  @sav2
  Scenario: Check that the REST API point for the stack analyses with external ID accepts authorization tokens
    Given System is running
    When I access /api/v2/stack-analyses/external-id
    Then I should get 401 status code

  @sav2
  Scenario Outline: Check that the stack analysis REST API endpoint requires authorization token even for improper HTTP methods
    Given System is running
     When I access the /api/v2/stack-analyses/external-id endpoint using the HTTP <method> method
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
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I access the /api/v2/stack-analyses/external-id endpoint using the HTTP <method> method and authorization token
     Then I should not get 200 status code

     Examples: HTTP methods
     | method |
     | GET    |
     | HEAD   |
     | PUT    |
     | DELETE |

  @sav2
  Scenario: Check that the API entry point without authorization token
    Given System is running
    When I wait 10 seconds
    When I send pypi package request with manifest valid_manifests/pylist.json to stack analysis v2 without authorization token
    Then I should get 401 status code

  @sav2
  Scenario: Check that the API entry point with authorization token
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I wait 20 seconds
    When I send pypi package request with manifest valid_manifests/pylist.json to stack analysis v2 with authorization token
    Then I should get 200 status code

  @sav2
  Scenario Outline: Check the stack analysis v2 response when called with proper authorization token
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send <ecosystem> package request with manifest <manifest> to stack analysis v2 with authorization token
    Then I should get 200 status code
    Then I should receive JSON response containing the status key
    Then I should receive JSON response containing the id key
    Then I should receive JSON response containing the submitted_at key
    Then I should receive JSON response with the status key set to success
    Then I should receive JSON response with the correct id
    Then I should receive JSON response with the correct timestamp in attribute submitted_at

    Examples: Stack analyses POST params
     | ecosystem | manifest                         |
     | pypi      | valid_manifests/pylist.json      |
     | npm       | valid_manifests/npmlist.json     |
     | maven     | valid_manifests/dependencies.txt |

  @sav2
  Scenario Outline: Check the stack analysis v2 response for missing data when called with proper authorization token
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send <ecosystem> package request with manifest <manifest> to stack analysis v2 with authorization token
    Then I should get 400 status code

    Examples: Stack analyses POST params
     | ecosystem | manifest                     |
     | None      | valid_manifests/pylist.json  |
     | npm       | None                         |
     | None      | None                         |

  @sav2
  Scenario Outline: Check the stack analysis v2 response for invalid manifest data when called with proper authorization token
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send <ecosystem> package request with manifest <manifest> to stack analysis v2 with authorization token
    Then I should get 400 status code

    Examples: Stack analyses POST params
     | ecosystem | manifest                         |
     | pypi      | valid_manifests/npmlist.json     |
     | npm       | valid_manifests/dependencies.txt |

  @sav2
  Scenario Outline: Check the stack analysis v2 request and response when called with proper authorization token
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send <ecosystem> package request with manifest <manifest> to stack analysis v2 with authorization token
    Then I should get 200 status code
    When I wait for stack analysis v2 to finish with authorization token
    Then I should find the external request id equals to id returned by stack analysis v2 post request
     And I should get stack analyses v2 response with all attributes

    Examples: Stack analyses POST params
     | ecosystem | manifest                         |
     | pypi      | valid_manifests/pylist.json      |
     | npm       | valid_manifests/npmlist.json     |
     | maven     | valid_manifests/dependencies.txt |
