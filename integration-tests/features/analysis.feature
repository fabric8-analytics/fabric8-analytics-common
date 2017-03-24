Feature: Analysis API V1

  Scenario: Access analysis of not yet analyzed package
    Given System is in initial state
    When I access /api/v1/analyses/npm/sequence/3.0.0
    Then I should see empty analysis
    And I should get 202 status code
    When I wait for npm/sequence/3.0.0 analysis to start
    And I access /api/v1/analyses/npm/sequence/3.0.0
    Then I should see incomplete analysis result for npm/sequence/3.0.0

  @slow
  Scenario: Validate analysis of a package
    Given System is in initial state
    When I access /api/v1/analyses/npm/sequence/3.0.0
    And I wait for npm/sequence/3.0.0 analysis to finish
    And I access /api/v1/analyses/npm/sequence/3.0.0
    Then I should get 200 status code
    And I should see complete analysis result for npm/sequence/3.0.0
    And Result of npm/sequence/3.0.0 should be valid
