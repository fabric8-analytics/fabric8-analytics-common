Feature: Stack analysis v2 API Minimal

  Scenario: Read outlier probability threshold value
    When I download and parse outlier probability threshold value
    Then I should have outlier probability threshold value between 0.0 and 1.0

  Scenario: Check that the API entry point
    Given System is running
    When I access /api/v1/stack-analyses-v2
    Then I should get 401 status code

  Scenario: Check that the API entry point requires authorization token
    Given System is running
    When I wait 10 seconds
    When I send Python package manifest requirements.txt to stack analysis version 2 without authorization token
    Then I should get 401 status code

  Scenario: Check that the stack-analyses-v2 returns a valid response
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I wait 10 seconds
    When I send Python package manifest requirements.txt to stack analysis version 2 with authorization token
    Then I should get 200 status code
    Then I should receive JSON response with the correct id
    When I wait for stack analysis version 2 to finish with authorization token
    Then I should get 200 status code
    Then I should get a valid request ID
    Then I should find the attribute request_id equals to id returned by stack analysis request
    Then I should find the proper sentiment values in the stack analysis response
    Then I should find that none analyzed package can be found in companion packages as well
    Then I should find that total 2 outliers are reported
    Then I should find that valid outliers are reported
    Then I should get license_analysis field in stack report
    Then I should find that alternate components replace user components
    Then I should find the security node for all dependencies
    Then I should find the security node for all alternate components
