Feature: Dependency Editor CVE Analyses API behaviour

  Scenario: Check that the API entry point
    Given System is running
    When I access /api/v1/depeditor-cve-analyses
    Then I should get 401 status code

  @requires_authorization_token
  Scenario: Check that the API entry point requires authorization token
    Given System is running
    When I access /api/v1/depeditor-cve-analyses
    Then I should get 400 status code


  @requires_authorization_token
  Scenario: Check that the depeditor-cve-analyses returns a valid response for maven ecosystem
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send valid input with list of packages and versions, ecosystem and request_id with authorization token 
    When I wait 20 seconds
    Then I should get 200 status code
     And I should receive JSON response
     And I should find the attribute request_id equals to request_id passed in request
     And I should find the result with the list of package, version and cve
     And I should find stack_highest_cvss equals to -1 if there is no CVEs in stack
