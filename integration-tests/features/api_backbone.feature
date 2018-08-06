Feature: Stack Analysis Backbone API 

  Scenario: Check the Backbone API /api/v1/stack_aggregator response
    Given backbone service is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I post backbone_input.json to Backbone API api/v1/stack_aggregator
    Then I should get 200 status code
     And I should receive a valid stack_aggregator json response
     And I should find a valid stack_aggregator database entry

  Scenario: Check the Backbone API /api/v1/recommender response
    Given backbone service is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I post backbone_input.json to Backbone API api/v1/recommender
    Then I should get 200 status code
     And I should receive a valid recommendation json response
     And I should find a valid recommendation database entry
