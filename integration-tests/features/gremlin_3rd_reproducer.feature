Feature: 3rd Gremlin reproducer

  @requires_access_to_graph_db
  Scenario: Basic check for Gremlin ability to search for given package in the Maven ecosystem
    Given System is running
    When I ask Gremlin to find the package io.vertx:vertx-core in the ecosystem maven
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should find that the latest_version property is higher than or equal to 3.4.2 in the package properties
