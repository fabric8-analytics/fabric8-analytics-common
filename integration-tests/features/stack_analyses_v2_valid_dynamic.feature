 Feature: Dynamic Manifests and Data Validation checks


 @sav2 @skip
 Scenario: Data validation checks for pypi ecosystem
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I send pypi package request with manifest pylist.json to stack analysis v2 with valid user key with transitives
    Then I should get 200 status code
     And I should receive JSON response containing the status key
     And I should receive JSON response containing the id key
     And I should receive JSON response containing the submitted_at key
     And I should receive JSON response with the status key set to success
     And I should receive JSON response with the correct id
     And I should receive JSON response with the correct timestamp in attribute submitted_at
    When I wait for stack analysis v2 to finish with user key
    Then I should get stack analyses v2 response with all attributes
      And I should find 6 unknown licenses for stack analyses v2
      And I should find 13 distinct licenses for stack analyses v2
      And I should find distinct license LGPL with exceptions or ZPL for license analysis
      And I should be able to validate github data for all dependencies
      And I should get 5 transitive dependencies for requests-futures
      And I should get 2 transitive vulnerabilities for requests-futures
      And I should find lxml with 4.2.1 4.5.2 4.5.0 with SNYK-PYTHON-LXML-72651 and 6.5 for public vulnerbilities
      And I should find Cross-site Scripting (XSS) and medium for lxml in private vulnerbilities
      And I should find License BSD for lxml in analyzed dependencies
      And I should find wtforms with 2.1 2.3.3 2.3.1 with SNYK-PYTHON-WTFORMS-40581 and 6.5 for private vulnerbilities
      And I should find License BSD for wtforms in analyzed dependencies
      And I should find Cross-site Scripting (XSS) and medium for wtforms in private vulnerbilities
  

 @sav2 
 Scenario: Data validation checks for npm ecosystem
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I wait 2 seconds
    When I send npm package request with manifest valid_npmlist.json to stack analysis v2 with valid user key with transitives
    Then I should get 200 status code
     And I should receive JSON response containing the status key
     And I should receive JSON response containing the id key
     And I should receive JSON response containing the submitted_at key
     And I should receive JSON response with the status key set to success
     And I should receive JSON response with the correct id
     And I should receive JSON response with the correct timestamp in attribute submitted_at
    When I wait for stack analysis v2 to finish with user key
    Then I should get stack analyses v2 response with all attributes
      And I should find 3 unknown licenses for stack analyses v2
      And I should find 8 distinct licenses for stack analyses v2
      And I should find distinct license Artistic-2.0 for license analysis
      And I should be able to validate github data for all dependencies
      And I should get 16 transitive dependencies for serve-static
      And I should get 6 transitive vulnerabilities for serve-static
      And I should find bootstrap with 4.1.1 5.0.0-alpha1 4.5.0 with SNYK-JS-BOOTSTRAP-73560 and 6.5 for public vulnerbilities
      And I should find Cross-site Scripting (XSS) and medium for bootstrap in public vulnerbilities
      And I should find License MIT for bootstrap in analyzed dependencies
      And I should find buefy with 0.7.10 0.9.4 0.8.19 with SNYK-JS-BUEFY-567814 and 7.3 for private vulnerbilities
      And I should find Cross-site Scripting (XSS) and high for buefy in private vulnerbilities
      And I should find License MIT for buefy in analyzed dependencies
      


 @sav2
 Scenario: Data validation checks for maven ecosystem
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I wait 2 seconds
    When I send maven package request with manifest vertx_dependencies.txt to stack analysis v2 with valid user key with transitives
    Then I should get 200 status code
     And I should receive JSON response containing the status key
     And I should receive JSON response containing the id key
     And I should receive JSON response containing the submitted_at key
     And I should receive JSON response with the status key set to success
     And I should receive JSON response with the correct id
     And I should receive JSON response with the correct timestamp in attribute submitted_at
    When I wait for stack analysis v2 to finish with user key
    Then I should get stack analyses v2 response with all attributes
      And I should find 0 unknown licenses for stack analyses v2
      And I should find 3 distinct licenses for stack analyses v2
      And I should find distinct license Eclipse Public License - v 1.0 for license analysis
      And I should be able to validate github data for all dependencies
      And I should get 15 transitive dependencies for io.vertx:vertx-core
      And I should get 6 transitive vulnerabilities for io.vertx:vertx-core
      And I should find io.vertx:vertx-core with 3.4.1 4.0.1 4.0.0-milestone5 with SNYK-JAVA-IOVERTX-32470 and 5.3 for public vulnerbilities
      And I should find HTTP Header Injection and medium for io.vertx:vertx-core in public vulnerbilities
      And I should find License The Apache Software License, Version 2.0 for io.vertx:vertx-core in analyzed dependencies
      And I should find org.apache.ignite:ignite-core with 2.7.6 2.9.1 2.8.1 with SNYK-JAVA-ORGAPACHEIGNITE-456561 and 4.8 for private vulnerbilities
      And I should find Denial of Service (DoS) and medium for org.apache.ignite:ignite-core in private vulnerbilities
      And I should find License The Apache Software License, Version 2.0 for org.apache.ignite:ignite-core in analyzed dependencies
      
  @sav2 
  Scenario: Check that the stack-analyses v2 returns a valid response for dynamic manifest files
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I wait 5 seconds
    When I tried to fetch dynamic manifests from s3
    Then I should be able to validate them
    When I wait 2 seconds
    When I send pypi package request with manifest valid_manifests/pylist.json to stack analysis v2 with valid user key
    Then I should get 200 status code
     And I should receive JSON response containing the status key
     And I should receive JSON response containing the id key
     And I should receive JSON response containing the submitted_at key
     And I should receive JSON response with the status key set to success
     And I should receive JSON response with the correct id
     And I should receive JSON response with the correct timestamp in attribute submitted_at
    When I wait for stack analysis v2 to finish with user key
    Then I should get stack analyses v2 response with all attributes
    When I wait 2 seconds
    When I send maven package request with manifest valid_manifests/dependencies.txt to stack analysis v2 with valid user key
     Then I should get 200 status code
     And I should receive JSON response containing the status key
     And I should receive JSON response containing the id key
     And I should receive JSON response containing the submitted_at key
     And I should receive JSON response with the status key set to success
     And I should receive JSON response with the correct id
     And I should receive JSON response with the correct timestamp in attribute submitted_at
    When I wait for stack analysis v2 to finish with user key
    Then I should get stack analyses v2 response with all attributes
    When I wait 2 seconds
    When I send npm package request with manifest valid_manifests/npmlist.json to stack analysis v2 with valid user key
     Then I should get 200 status code
     And I should receive JSON response containing the status key
     And I should receive JSON response containing the id key
     And I should receive JSON response containing the submitted_at key
     And I should receive JSON response with the status key set to success
     And I should receive JSON response with the correct id
     And I should receive JSON response with the correct timestamp in attribute submitted_at
    When I wait for stack analysis v2 to finish with user key
    Then I should get stack analyses v2 response with all attributes

 
  
  @sav2
  Scenario Outline: Check the stack analysis v2 for single companion packages
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I wait 2 seconds
    When I send <ecosystem> package request with manifest <manifest> to stack analysis v2 with valid user key 
    Then I should get 200 status code
     And I should receive JSON response containing the status key
     And I should receive JSON response containing the id key
     And I should receive JSON response containing the submitted_at key
     And I should receive JSON response with the status key set to success
     And I should receive JSON response with the correct id
     And I should receive JSON response with the correct timestamp in attribute submitted_at
    When I wait for stack analysis v2 to finish with user key
    Then I should get stack analyses v2 response with all attributes
    And I should get latest version <latest_version> for <component> in campanion packages
    And I should get latest version <latest_version_2> for <component_2> in campanion packages


     Examples: Stack analyses POST params
     | ecosystem | manifest               | component | latest_version | component_2 | latest_version_2 |
     #| pypi      | pylist.json            | ansible   | 2.9.9          | coveralls   | 2.1.2            |
     | npm       | valid_npmlist.json     | gatsby    | 2.9.2          | history     | 4.9.0            |
