Feature: Ecosystems API V1

  Scenario: Access Ecosystems list
    Given System is running
    When I access /api/v1/ecosystems?per_page=5
    Then I should see 5 ecosystems
