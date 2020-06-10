Feature: Smoketests for stack analysis V2 API tests

  @sav2
  Scenario Outline: Check the stack analysis smoke test for <ecosystem> package with <file>
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key

    # request the stack analysis
    When I wait 10 seconds
    When I send <ecosystem> package request with manifest <file> to stack analysis v2 with valid user key
    Then I should get 200 status code
     And I should receive JSON response containing the status key
     And I should receive JSON response containing the id key
     And I should receive JSON response containing the submitted_at key
     And I should receive JSON response with the status key set to success
     And I should receive JSON response with the correct id
     And I should receive JSON response with the correct timestamp in attribute submitted_at

    # Wait for response from stack analysis
    When I wait for stack analysis v2 to finish with user key

    # Request ID check
    Then I should find the external request id equals to id returned by stack analysis v2 post request

    # Check all parameters of response including timestamp
     And I should get stack analyses v2 response with all attributes

    # SLA/SLO-related checks
    When I look at the stack analysis duration
    Then I should see that the duration is less than 120 seconds

    # Analyzed direct dependencies checks
    When I look at recent stack analysis
    Then I should find <analyzed_deps_count> analyzed dependencies for stack analyses v2

    # Unknown dependencies checks -- This are disabled till support for a flag in platform to ignore dummy
    # unknown dependency ingestion.
    #When I look at recent stack analysis
    #Then I should find <unknown_deps_count> unknown dependencies for stack analyses v2

    # Check license count
    When I look at recent stack analysis
    Then I should find <unknown_license_count> unknown licenses for stack analyses v2
     And I should find <distinct_license_count> distinct licenses for stack analyses v2

    # Verify recommendation data
    When I look at recent stack analysis
    Then I should find <usage_outlier_count> usage outliers for stack analyses v2

    # Verify Free user having registration link.
    When I look at recent stack analysis
    Then I should find registration link for stack analyses v2

    # Analyzed dependencies attribute check
    When I look at recent stack analysis
    Then I should find all attribute about analyzed dependencies for stack analyses v2

     Examples: files containing packages to test
     | ecosystem | file                         | analyzed_deps_count | unknown_deps_count | license_count | unknown_license_count | distinct_license_count | usage_outlier_count | companion_count |
     | pypi      | requirements_click_6_7.json  | 1                   | 0                  | 1             | 1                     | 1                      | 0                   | 5               |
     | pypi      | requirements_click_7_0.json  | 1                   | 0                  | 1             | 0                     | 1                      | 0                   | 5               |
     | pypi      | fastlog_urllib_requests.json | 3                   | 0                  | 3             | 1                     | 3                      | 0                   | 5               |
     | pypi      | array_split.json             | 1                   | 0                  | 1             | 0                     | 1                      | 0                   | 0               |
     | pypi      | numpy_1_11_0.json            | 1                   | 0                  | 1             | 0                     | 1                      | 0                   | 5               |
     | pypi      | numpy_1_16_2.json            | 1                   | 0                  | 0             | 0                     | 0                      | 0                   | 5               |
     | pypi      | numpy_scipy.json             | 2                   | 0                  | 1             | 0                     | 1                      | 0                   | 5               |
     | pypi      | pytest_2_0_0.json            | 1                   | 0                  | 1             | 0                     | 1                      | 0                   | 5               |
     | pypi      | pytest_3_2_2.json            | 1                   | 0                  | 1             | 0                     | 1                      | 0                   | 5               |
     | pypi      | requests_2_20_0.json         | 1                   | 0                  | 1             | 0                     | 1                      | 0                   | 3               |
     | pypi      | requests_2_21_0.json         | 1                   | 0                  | 1             | 0                     | 1                      | 0                   | 3               |
     | pypi      | scipy_1_1_0.json             | 1                   | 0                  | 1             | 0                     | 1                      | 0                   | 5               |
     | pypi      | scipy_1_2_0.json             | 1                   | 0                  | 1             | 0                     | 1                      | 0                   | 5               |
     | pypi      | scipy_1_2_1.json             | 1                   | 0                  | 0             | 0                     | 0                      | 0                   | 5               |
     | maven     | basic.txt                    | 9                   | 0                  | 14            | 0                     | 14                     | 0                   | 5               |
     | maven     | springboot_dependencies.txt  | 4                   | 0                  | 8             | 0                     | 8                      | 1                   | 0               |
     | maven     | vertx_3_4_1_dependencies.txt | 7                   | 0                  | 8             | 1                     | 8                      | 1                   | 0               |
     | maven     | vertx_3_4_2_dependencies.txt | 7                   | 0                  | 8             | 1                     | 8                      | 1                   | 0               |
     | maven     | vertx_dependencies.txt       | 7                   | 1                  | 8             | 1                     | 8                      | 1                   | 0               |
     | npm       | npm_1_direct.json            | 1                   | 0                  | 1             | 0                     | 1                      | 0                   | 0               |
     | npm       | npm_10_direct.json           | 10                  | 0                  | 2             | 0                     | 2                      | 0                   | 0               |
     | npm       | npm_50_direct_799_tr.json    | 50                  | 0                  | 16            | 11                    | 16                     | 0                   | 2               |
     | npm       | npm_100_direct_1039_tr.json  | 100                 | 0                  | 19            | 14                    | 19                     | 0                   | 3               |
     | npm       | npm_150_direct_1170_tr.json  | 150                 | 0                  | 20            | 15                    | 20                     | 0                   | 1               |
