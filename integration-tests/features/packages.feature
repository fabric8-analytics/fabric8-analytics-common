Feature: Packages API V1

  Scenario: Access packages list for empty ecosystem
    Given System is in initial state
    When I access /api/v1/packages/npm/
    Then I should see 0 packages

  Scenario: Access packages list for non-empty ecosystem
    Given System is running
    When I access /api/v1/analyses/npm/sequence/2.2.1
    And I wait for npm/sequence/2.2.1 analysis to start
    And I access /api/v1/packages/npm/
    Then I should see 1 packages (sequence), all from npm ecosystem
