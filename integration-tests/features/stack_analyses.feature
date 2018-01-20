Feature: Analyse API funcationality check

  Scenario: Read outlier probability threshold value
    When I download and parse outlier probability threshold value
    Then I should have outlier probability threshold value between 0.0 and 1.0

  @production
  Scenario: Check that the API entry point
    Given System is running
    When I access /api/v1/stack-analyses
    Then I should get 401 status code

  @production
  Scenario: Check that the API entry point requires authorization token
    Given System is running
    When I wait 10 seconds
    When I send Maven package manifest pom-effective.xml to stack analysis without authorization token
    Then I should get 401 status code

  Scenario: Check that the stack-analyses returns a valid response for maven ecosystem
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I wait 10 seconds
    When I send Maven package manifest pom-effective.xml to stack analysis version 3 with authorization token
    Then I should get 200 status code
     And I should receive JSON response with the correct id
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should get a valid request ID
     And I should find the attribute request_id equals to id returned by stack analysis request
     And I should find that none analyzed package can be found in companion packages as well
     And I should find that valid outliers are reported
     And I should get license_analysis field in stack report
     And I should find that alternate components replace user components
     And I should find the security node for all dependencies
     And I should find the security node for all alternate components
     And I should find input_stack_topics field in recommendation
     And I should find matching topic lists for all user_stack_info/analyzed_dependencies components
