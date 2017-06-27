Feature: Smoke test

  Scenario: Check the API entry point
    Given System is running
    When I access /api/v1/
    Then I should get 200 status code

  Scenario: Check the /schemas entry point
    Given System is running
    When I access /api/v1/schemas/
    Then I should get 200 status code

  Scenario: Check the /system/version entry point
    Given System is running
    When I access /api/v1/system/version/
    Then I should get 200 status code

  #Scenario: Check the jobs API entry point
  #  Given System is running
  #  When I access /api/v1/readiness
  #  Then I should get 200 status code

  #Scenario: Check the jobs API entry point
  #  Given System is running
  #  When I access jobs API /api/v1
  #  Then I should get 200 status code

  #Scenario: Check the jobs API entry point
  #  Given System is running
  #  When I access jobs API /api/v1/readiness
  #  Then I should get 200 status code

  #Scenario: Check the jobs API entry point
  #  Given System is running
  #  When I access jobs API /api/v1/liveness
  #  Then I should get 200 status code

  #Scenario: Check the jobs API entry point
  #  Given System is running
  #  When I access jobs API /api/v1/service/state
  #  Then I should get 200 status code

