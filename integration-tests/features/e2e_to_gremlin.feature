Feature: The end to end tests, from the start of analysis to the graph database

  @requires_access_to_graph_db
  Scenario: Check that the Gremlin is available
    Given System is running
    When I access Gremlin API
    Then I should get 200 status code
     And I should get valid Gremlin response
    When I read the last update time for the package clojure_py version 0.2.4 in the ecosystem pypi
     And I remember the current time
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should get a valid timestamp represented as UNIX time
     And I should find that the returned timestamp is older than remembered time
    When I acquire job API authorization token
    Then I should get the proper job API authorization token
    When I post a job metadata job_pypi_clojure_py.json with state running using authorization token
    Then I should get 201 status code
    When I wait for the update in the graph database for the package clojure_py version 0.2.4 in the ecosystem pypi
     And I read the last update time for the package clojure_py version 0.2.4 in the ecosystem pypi
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should get a valid timestamp represented as UNIX time
     And I should find that the returned timestamp is newer than remembered time
