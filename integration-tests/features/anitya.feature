Feature: Anitya functionality

  Scenario: Access anitya with packages
     Given System is running 
     When I access /api/v1/analyses/npm/sequence/2.2.1
     And I wait for npm/sequence/2.2.1 analysis to finish
     And I access anitya /project/1
     Then I should get 200 status code
