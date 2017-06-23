Feature: Jobs debug API

  Scenario: Basic check the endpoint for analyses report output
    Given System is running
    When I wait 20 seconds
    When I ask for analyses report for ecosystem maven
    Then I should get 200 status code

