Feature: CVEs Bydate and Ecosystem API behaviour

  
  Scenario: Check the API entry point
    Given System is running
    When I access /api/v1/
    Then I should get 200 status code

  
  Scenario: Check that the cve_bydate API entry point checks for empty date
    Given System is running
    And cve_bydate_ecosystem service is running
    When I access /api/v1/cves/bydate
    Then I should get 404 status code

 
  Scenario: Check that the cve_bydate_ecosystem API entry point checks for a non existent ecosystem
    Given System is running
    And cve_bydate_ecosystem service is running
    When I search for ecosystem unknown-ecosystem
    Then I should receive an empty response
    Then I should get 200 status code

  
  Scenario: Check that the cve_bydate_ecosystem API entry point checks for a non existent date
    Given System is running
    And cve_bydate_ecosystem service is running
    When I search for 19470814 date
    Then I should receive an empty response
    Then I should get 200 status code
 