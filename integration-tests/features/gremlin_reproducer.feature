Feature: Check the Gremlin instance and its behaviour

  @requires_access_to_graph_db
  Scenario: Basic check for Gremlin ability to search for given package in any versions for the Maven ecosystem
    Given System is running
    When I ask Gremlin to find all versions of the package io.vertx:vertx-core in the ecosystem maven
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should find the following properties (description, last_updated, pecosystem, pname, version, vertex_label) in all found packages
     And I should find the following properties (cm_avg_cyclomatic_complexity, cm_loc, cm_num_files, dependents_count) in all found packages
     And I should find that all found packages have valid timestamp with the last update time
