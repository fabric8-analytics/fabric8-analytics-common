Feature: Adding Dynamic Manifests check

  @dynamic-manifest
  Scenario: Check that the stack-analyses returns a valid response for dynamic manifest files
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I wait 10 seconds
    When I tried to fetch dynamic manifests from s3
    Then I should be able to validate them
    When I wait 5 seconds
    When I send Python package manifest valid_manifests/pylist.json to stack analysis version 3 with authorization token
    When I wait 5 seconds
    Then I should get 200 status code
      And I should receive JSON response with the correct id
    When I wait for stack analysis to finish with authorization token
    Then I should get 200 status code
     And I should get a valid request ID
     And I should find the attribute request_id equals to id returned by stack analysis request
     And I should find that none analyzed package can be found in companion packages as well
     And I should find that valid outliers are reported
     And I should get license_analysis field in stack report
     And I should find the security node for all dependencies
    When I send new Maven package manifest valid_manifests/dependencies.txt to stack analysis version 3 with authorization token
    When I wait 5 seconds
    Then I should get 200 status code
      And I should receive JSON response with the correct id
    When I wait for stack analysis to finish with authorization token
    Then I should get 200 status code
     And I should get a valid request ID
     And I should find the attribute request_id equals to id returned by stack analysis request
     And I should find that none analyzed package can be found in companion packages as well
     And I should find that valid outliers are reported
     And I should get license_analysis field in stack report
     And I should find the security node for all dependencies
    When I send NPM package manifest valid_manifests/npmlist.json to stack analysis version 3 with authorization token
    When I wait 15 seconds
    Then I should get 200 status code
      And I should receive JSON response with the correct id
    When I wait for stack analysis to finish with authorization token
    When I wait 10 seconds
    Then I should get 200 status code
     And I should get a valid request ID
     And I should find the attribute request_id equals to id returned by stack analysis request
     And I should find that none analyzed package can be found in companion packages as well
     And I should find that valid outliers are reported
     And I should get license_analysis field in stack report
     And I should find the security node for all dependencies