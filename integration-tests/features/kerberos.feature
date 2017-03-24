Feature: Kerberos Authentication

  Scenario: Obtain API token
    Given System is running
    When I obtain TGT in kerberos-client service
    And I perform kerberized POST request to /api/v1/api-token
    Then I should get API token
