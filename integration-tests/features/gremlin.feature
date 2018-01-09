Feature: Check the Gremlin instance and its behaviour

  @requires_access_to_graph_db
  Scenario: Check that the Gremlin is available
    Given System is running
    When I access Gremlin API
    Then I should get 200 status code
    Then I should get valid Gremlin response

  @requires_access_to_graph_db
  Scenario: Basic check for Gremlin ability to find vertexes
    Given System is running
    When I ask Gremlin to find all vertexes having property vertex_label set to foobar
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should get 0 vertexes

  @requires_access_to_graph_db
  Scenario: Basic check for Gremlin ability to find vertexes for given ecosystems
    Given System is running
    When I ask Gremlin to find number of vertexes for the ecosystem npm
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should find at least one such vertex
    When I ask Gremlin to find number of vertexes for the ecosystem go
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should find at least one such vertex
    When I ask Gremlin to find number of vertexes for the ecosystem pypi
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should find at least one such vertex
    When I ask Gremlin to find number of vertexes for the ecosystem maven
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should find at least one such vertex

  @requires_access_to_graph_db
  Scenario: Basic check for Gremlin ability to search for given package in any versions for the npm ecosystem
    Given System is running
    When I ask Gremlin to find all versions of the package sequence in the ecosystem npm
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should find the following properties (description, last_updated, pecosystem, pname, version, vertex_label) in all found packages
     And I should not find any property apart from (description, last_updated, pecosystem, pname, version, vertex_label, licenses, gh_release_date) in all found packages
     And I should find that all found packages have valid timestamp with the last update time

  @requires_access_to_graph_db
  Scenario: Basic check for Gremlin ability to search for given package in any versions for the Maven ecosystem
    Given System is running
    When I ask Gremlin to find all versions of the package io.vertx:vertx-core in the ecosystem maven
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should find the following properties (description, last_updated, pecosystem, pname, version, vertex_label) in all found packages
     And I should find the following properties (cm_avg_cyclomatic_complexity, cm_loc, cm_num_files, dependents_count, shipped_as_downstream) in all found packages
     And I should find that all found packages have valid timestamp with the last update time

  @requires_access_to_graph_db
  Scenario: Basic check for Gremlin ability to search for given package in any versions for the Pypi ecosystem
    Given System is running
    When I ask Gremlin to find all versions of the package clojure_py in the ecosystem pypi
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should find the following properties (description, last_updated, pecosystem, pname, version, vertex_label) in all found packages
     And I should find that all found packages have valid timestamp with the last update time

  @requires_access_to_graph_db
  Scenario: Basic check for Gremlin ability to search for given package and version for the npm ecosystem
    Given System is running
    When I ask Gremlin to find the package sequence version 3.0.0 in the ecosystem npm
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should find the following properties (description, last_updated, pecosystem, pname, version, vertex_label) in all found packages
     And I should not find any property apart from (description, last_updated, pecosystem, pname, version, vertex_label, licenses) in all found packages
     And I should find that the pecosystem property is set to npm in the package properties
     And I should find that the pname property is set to sequence in the package properties
     And I should find that the version property is set to 3.0.0 in the package properties
     And I should find that the licenses property is set to Apache 2.0 in the package properties
     And I should find that all found packages have valid timestamp with the last update time

  @requires_access_to_graph_db
  Scenario: Basic check for Gremlin ability to search for given package and version for ecosystem Maven
    Given System is running
    When I ask Gremlin to find the package io.vertx:vertx-core version 3.4.0 in the ecosystem maven
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should find the following properties (description, last_updated, pecosystem, pname, version, vertex_label) in all found packages
     And I should find the following properties (cm_avg_cyclomatic_complexity, cm_loc, cm_num_files, dependents_count, shipped_as_downstream, relative_used) in all found packages
     And I should find that the pecosystem property is set to maven in the package properties
     And I should find that the pname property is set to io.vertx:vertx-core in the package properties
     And I should find that the version property is set to 3.4.0 in the package properties
     And I should find that all found packages have valid timestamp with the last update time

  @requires_access_to_graph_db
  Scenario: Basic check for Gremlin ability to search for given package and version for ecosystem Pypi
    Given System is running
    When I ask Gremlin to find the package clojure_py version 0.2.4 in the ecosystem pypi
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should find the following properties (description, last_updated, pecosystem, pname, version, vertex_label) in all found packages
     And I should find that the pecosystem property is set to pypi in the package properties
     And I should find that the pname property is set to clojure_py in the package properties
     And I should find that the version property is set to 0.2.4 in the package properties
     And I should find that all found packages have valid timestamp with the last update time

  @requires_access_to_graph_db
  Scenario: Basic check for Gremlin ability to search for given package in the npm ecosystem
    Given System is running
    When I ask Gremlin to find the package sequence in the ecosystem npm
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should find that all found packages have valid timestamp with the last update time

  @requires_access_to_graph_db
  Scenario: Basic check for Gremlin ability to search for given package in the Maven ecosystem
    Given System is running
    When I ask Gremlin to find the package io.vertx:vertx-core in the ecosystem maven
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should find that all found packages have valid timestamp with the last update time

  @requires_access_to_graph_db
  Scenario: Basic check for Gremlin ability to search for given package in the Pypi ecosystem
    Given System is running
    When I ask Gremlin to find the package clojure_py in the ecosystem pypi
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should find that all found packages have valid timestamp with the last update time

  @requires_access_to_graph_db
  Scenario: Basic check for Gremlin ability to search for given package
    Given System is running
    When I ask Gremlin to find the package sequence in the ecosystem npm
     And I remember the current time
    Then I should get 200 status code
     And I should get valid Gremlin response
      And I should find that all found packages have valid timestamp with the last update time
      And I should find that the package data is older than remembered time

  @requires_access_to_graph_db
  Scenario: Basic check for Gremlin ability to read last update timestamp for the selected package from the Pypi ecosystem
    Given System is running
    When I read the last update time for the package clojure_py version 0.2.4 in the ecosystem pypi
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should get a valid timestamp represented as UNIX time

  @requires_access_to_graph_db
  Scenario: Basic check for Gremlin ability to read last update timestamp for the selected package from the npm ecosystem
    Given System is running
    When I read the last update time for the package sequence version 3.0.0 in the ecosystem npm
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should get a valid timestamp represented as UNIX time

  @requires_access_to_graph_db
  Scenario: Basic check for Gremlin ability to read last update timestamp for the selected package from the Maven ecosystem
    Given System is running
    When I read the last update time for the package io.vertx:vertx-core version 3.4.0 in the ecosystem maven
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should get a valid timestamp represented as UNIX time

  @requires_access_to_graph_db
  Scenario: Check numeric values for GitHub metadata for the package from the pypi ecosystem
    When I ask Gremlin to find the package clojure_py in the ecosystem pypi
    Then I should get 200 status code
     And I should find that the gh_forks property has numeric value greater than or equal to -1
     And I should find that the gh_issues_last_month_opened property has numeric value greater than or equal to -1
     And I should find that the gh_issues_last_month_closed property has numeric value greater than or equal to -1
     And I should find that the gh_issues_last_year_opened property has numeric value greater than or equal to -1
     And I should find that the gh_issues_last_year_closed property has numeric value greater than or equal to -1
     And I should find that the gh_prs_last_month_opened property has numeric value greater than or equal to -1
     And I should find that the gh_prs_last_month_closed property has numeric value greater than or equal to -1
     And I should find that the gh_prs_last_year_opened property has numeric value greater than or equal to -1
     And I should find that the gh_prs_last_year_closed property has numeric value greater than or equal to -1
     And I should find that the gh_stargazers property has numeric value greater than or equal to -1

  @requires_access_to_graph_db
  Scenario: Check numeric values for Libio metadata for the package from the pypi ecosystem
    When I ask Gremlin to find the package clojure_py in the ecosystem pypi
    Then I should get 200 status code
     And I should find that the libio_dependents_projects property has numeric value greater than or equal to -1
     And I should find that the libio_dependents_repos property has numeric value greater than or equal to -1
     And I should find that the libio_latest_release property has numeric value greater than or equal to -1
     And I should find that the libio_latest_version property is set to 0.2.4 in the package properties
     And I should find that the libio_total_releases property has numeric value greater than or equal to -1

  @requires_access_to_graph_db
  Scenario: Check other numeric values for the package from the pypi ecosystem
    When I ask Gremlin to find the package clojure_py in the ecosystem pypi
    Then I should get 200 status code
     And I should find that the package_dependents_count property has numeric value greater than or equal to -1

  @requires_access_to_graph_db
  Scenario: Basic check for Gremlin ability to search for given package in the npm ecosystem
    Given System is running
    When I ask Gremlin to find the package sequence in the ecosystem npm
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should find that all found packages have valid timestamp with the last update time
     And I should find that the ecosystem property is set to npm in the package properties
     And I should find that the name property is set to sequence in the package properties
     And I should find that the latest_version property is set to 3.0.0 in the package properties

  @requires_access_to_graph_db
  Scenario: Check numeric values for GitHub metadata for given package in the npm ecosystem
    When I ask Gremlin to find the package sequence in the ecosystem npm
    Then I should get 200 status code
     And I should find that the gh_forks property has numeric value greater than or equal to -1
     And I should find that the gh_issues_last_month_opened property has numeric value greater than or equal to -1
     And I should find that the gh_issues_last_month_closed property has numeric value greater than or equal to -1
     And I should find that the gh_issues_last_year_opened property has numeric value greater than or equal to -1
     And I should find that the gh_issues_last_year_closed property has numeric value greater than or equal to -1
     And I should find that the gh_prs_last_month_opened property has numeric value greater than or equal to -1
     And I should find that the gh_prs_last_month_closed property has numeric value greater than or equal to -1
     And I should find that the gh_prs_last_year_opened property has numeric value greater than or equal to -1
     And I should find that the gh_prs_last_year_closed property has numeric value greater than or equal to -1
     And I should find that the gh_stargazers property has numeric value greater than or equal to -1

  @requires_access_to_graph_db
  Scenario: Check numeric values for Libio metadata for given package in the npm ecosystem
    When I ask Gremlin to find the package sequence in the ecosystem npm
    Then I should get 200 status code
     And I should find that the libio_dependents_projects property has numeric value greater than or equal to -1
     And I should find that the libio_dependents_repos property has numeric value greater than or equal to -1
     And I should find that the libio_latest_release property has numeric value greater than or equal to -1
     And I should find that the libio_latest_version property is set to 3.0.0 in the package properties
     And I should find that the libio_total_releases property has numeric value greater than or equal to -1

  @requires_access_to_graph_db
  Scenario: Basic check for Gremlin ability to search for given package in the Maven ecosystem
    Given System is running
    When I ask Gremlin to find the package io.vertx:vertx-core in the ecosystem maven
    Then I should get 200 status code
     And I should get valid Gremlin response
     And I should find that all found packages have valid timestamp with the last update time
     And I should find that the ecosystem property is set to maven in the package properties
     And I should find that the name property is set to io.vertx:vertx-core in the package properties
     And I should find that the latest_version property is set to 3.4.2 in the package properties

  @requires_access_to_graph_db
  Scenario: Check numeric values for GitHub metadata for given package in the Maven ecosystem
    When I ask Gremlin to find the package io.vertx:vertx-core in the ecosystem maven
    Then I should get 200 status code
     And I should find that the gh_forks property has numeric value greater than or equal to -1
     And I should find that the gh_issues_last_month_opened property has numeric value greater than or equal to -1
     And I should find that the gh_issues_last_month_closed property has numeric value greater than or equal to -1
     And I should find that the gh_issues_last_year_opened property has numeric value greater than or equal to -1
     And I should find that the gh_issues_last_year_closed property has numeric value greater than or equal to -1
     And I should find that the gh_prs_last_month_opened property has numeric value greater than or equal to -1
     And I should find that the gh_prs_last_month_closed property has numeric value greater than or equal to -1
     And I should find that the gh_prs_last_year_opened property has numeric value greater than or equal to -1
     And I should find that the gh_prs_last_year_closed property has numeric value greater than or equal to -1
     And I should find that the gh_stargazers property has numeric value greater than or equal to -1

  @requires_access_to_graph_db
  Scenario: Check numeric values for Libio metadata for given package in the Maven ecosystem
    When I ask Gremlin to find the package io.vertx:vertx-core in the ecosystem maven
    Then I should get 200 status code
     And I should find that the libio_dependents_projects property has numeric value greater than or equal to -1
     And I should find that the libio_dependents_repos property has numeric value greater than or equal to -1
     And I should find that the libio_latest_release property has numeric value greater than or equal to -1
     And I should find that the libio_latest_version property is set to 3.5.0.Beta1 in the package properties
     And I should find that the libio_total_releases property has numeric value greater than or equal to -1
