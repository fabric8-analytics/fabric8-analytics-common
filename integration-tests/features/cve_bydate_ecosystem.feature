  Scenario: Check that the cve_bydate API entry point checks for Invalid date format
    Given System is running
    Given cve_bydate_ecosystem service is running
    When I access /api/v1/cves/bydate/1000-01-01/
    Then I should get 400 status code
  
  Scenario: Check that the cve_bydate_ecosystem API entry point checks for Invalid date format 
    Given System is running
    Given cve_bydate_ecosystem service is running
    When I access /api/v1/cves/bydate/1000-01-01/ecosystem
    Then I should get 400 status code
  
  Scenario: Check that the cve_bydate API entry point checks for valid date format
    Given System is running
    Given cve_bydate_ecosystem service is running
    When I access /api/v1/cves/bydate/10000101/
    Then I should get 200 status code
  
  Scenario: Check that the cve_bydate_ecosystem API entry point checks for non-existing date & existing ecosystem
    Given System is running
    Given cve_bydate_ecosystem service is running
    When I search for 19470815 date and pypi ecosystem
    Then I should receive an empty JSON response
    Then I should get 200 status code
  
  Scenario: Check that the cve_bydate_ecosystem API entry point checks for non-existing date  & non-existing ecosystem
    Given System is running
    Given cve_bydate_ecosystem service is running
    When I search for 19470815 date and non-existing ecosystem
    Then I should receive an empty JSON response
    Then I should get 200 status code