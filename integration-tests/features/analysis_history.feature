Feature: Analysis History Recording

  @slow
  Scenario: Component analysis results are recorded
    Given System is in initial state
    And the analysis indexer is running locally
    Then the bayesian-analysis_record template should have been uploaded
    When I access /api/v1/analyses/npm/sequence/3.0.0
    And I wait for npm/sequence/3.0.0 analysis to finish
    And I access /api/v1/analyses/npm/sequence/3.0.0
    Then I should get 200 status code
    And I should see complete analysis result for npm/sequence/3.0.0
    And Result of npm/sequence/3.0.0 should be valid
    And I should see component bayesian-analysis_record entries for npm/sequence/3.0.0
