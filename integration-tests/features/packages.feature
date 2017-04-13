Feature: Packages API V1

  Scenario: Access packages list for empty ecosystem
    Given System is in initial state
    When I access /api/v1/packages/pypi/
    Then I should see 0 packages

  Scenario: Access packages list for non-empty ecosystem
    Given System is running
    When I access /api/v1/analyses/pypi/six/1.9.0
    And I wait for pypi/six/1.9.0 analysis to start
    And I access /api/v1/packages/pypi/
    Then I should see 1 packages (six), all from pypi ecosystem
