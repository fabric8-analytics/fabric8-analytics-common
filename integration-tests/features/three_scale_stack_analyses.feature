Feature: Three Scale Analyse API functionality check

  Scenario: Check that the API entry point requires user_key
    Given System is running
    Given Three scale preview service is running
    When I wait 10 seconds
    When I send NPM package manifest package.json to stack analysis through 3scale gateway without user_key
    Then I should get 403 status code
  
  @skip
  Scenario: Check that the stack-analyses returns a valid response for NPM ecosystem
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I wait 10 seconds
    When I send NPM package manifest package.json to stack analysis through 3scale gateway with user_key
    Then I should get 200 status code
     And I should receive JSON response with the correct id
    When I wait for stack analysis to finish with user_key
    Then I should get 200 status code
     And I should get a valid request ID
     And I should find the attribute request_id equals to id returned by stack analysis request
     And I should find that none analyzed package can be found in companion packages as well
     And I should find that total 0 outliers are reported
     And I should find that greater than 0 companions are reported
     And I should get license_analysis field in stack report
     And I should find the security node for all dependencies
     And I should find input_stack_topics field in recommendation
     And I should find matching topic lists for all user_stack_info/analyzed_dependencies components
  
  @skip
  Scenario: Check that the stack-analyses GET returns limits exceeded for NPM ecosystem
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I wait 10 seconds
    When I send NPM package manifest package.json to stack analysis through 3scale gateway with user_key
    Then I should get 200 status code
     And I should receive JSON response with the correct id
    When I call stack analysis 40 times in a minute with user_key
    Then I should get 429 status code
     And I should get Limits exceeded text response

  @skip
  Scenario: Check that the stack-analyses POST returns limits exceeded for NPM ecosystem
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I wait 10 seconds
    When I send NPM package manifest package.json to stack analysis 40 times in a minute through 3scale gateway with user_key
    Then I should get 429 status code
     And I should get Limits exceeded text response

  Scenario: Check the /api/v1/submit-feedback response via 3scale gateway
    Given System is running
    Given Three scale preview service is running
    When I wait 60 seconds
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I access /api/v1/submit-feedback without valid values via 3scale gateway
    Then I should get 400 status code
  
  @skip
  Scenario: Check the /api/v1/submit-feedback response via 3scale gateway
    Given System is running
    Given Three scale preview service is running
    When I acquire the use_key for 3scale
    Then I should get the proper user_key
    When I access /api/v1/submit-feedback without valid values 40 times in a minute via 3scale gateway
    Then I should get 429 status code
     And I should get Limits exceeded text response
