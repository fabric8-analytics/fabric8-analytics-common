Feature: Versions API V1

  Scenario: Access version list for not tracked package
    Given System is in initial state
    When I access /api/v1/versions/npm/sequence
    Then I should get 404 status code

  Scenario: Access version list for tracked package
    Given System is running
    When I access /api/v1/analyses/npm/sequence/2.2.1
    And I access /api/v1/analyses/npm/sequence/2.2.0
    And I wait for npm/sequence/2.2.1 analysis to finish
    And I wait for npm/sequence/2.2.0 analysis to start
    And I access /api/v1/versions/npm/sequence
    Then I should see 2 versions (2.2.0, 2.2.1), all for npm/sequence package
