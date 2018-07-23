Feature: Checks for the license analysis service

  @smoketest @production
  Scenario: Basic check if the license analysis service is running
    Given System is running
     When I access the license analysis service
     # TODO: this is actually a bug - needs to be resolved later in the service
     Then I should get 200 status code
      And I should receive JSON response with the status key set to ok
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I access the license analysis service with authorization token
     Then I should get 200 status code
      And I should receive JSON response with the status key set to ok


  Scenario Outline: Smoketest if all JSON files with package+license info can be processes by license analysis
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I send the file <filename> to the license analysis service 
     Then I should get 200 status code

     Examples: filenames
     |filename                          |
     |maven_five_different_packages.json|
     |maven_one_package.json            |
     |maven_one_unknown_package.json    |
     |maven_three_wildfly_packages.json |


  Scenario: Test the license analysis for one known Maven package
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I send the file maven_one_package.json to the license analysis service
     Then I should get 200 status code
      And I should find that the license analysis status is successful
      And I should find that the stack license is apache 2.0
      And I should not see any conflict packages
      And I should not see any outlier packages
      And I should see one distinct license
      And I should find apache 2.0 license in distinct licenses
      And I should find license AL2 for the package org.wildfly.swarm:monitor version 2018.3.3
      And I should find that representative license has been found for package org.wildfly.swarm:monitor version 2018.3.3
      And I should find that license analysis was successful for package org.wildfly.swarm:monitor version 2018.3.3
      And I should not see any component conflicts
      And I should not see any really unknown licenses


  Scenario: Test the license analysis for three known Maven packages
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I send the file maven_three_wildfly_packages.json to the license analysis service
     Then I should get 200 status code
      And I should find that the license analysis status is successful
      And I should find that the stack license is apache 2.0
      And I should not see any conflict packages
      And I should not see any outlier packages
      And I should see one distinct license
      And I should find apache 2.0 license in distinct licenses
      And I should find license AL2 for the package org.wildfly.swarm:monitor version 2018.3.3
      And I should find that representative license has been found for package org.wildfly.swarm:monitor version 2018.3.3
      And I should find that license analysis was successful for package org.wildfly.swarm:monitor version 2018.3.3
      And I should find license AL2 for the package org.wildfly.swarm:cdi version 2018.3.3
      And I should find that representative license has been found for package org.wildfly.swarm:cdi version 2018.3.3
      And I should find that license analysis was successful for package org.wildfly.swarm:cdi version 2018.3.3
      And I should find license AL2 for the package org.wildfly.swarm:jaxrs version 2018.3.3
      And I should find that representative license has been found for package org.wildfly.swarm:jaxrs version 2018.3.3
      And I should find that license analysis was successful for package org.wildfly.swarm:jaxrs version 2018.3.3
      And I should not see any component conflicts
      And I should not see any really unknown licenses


  Scenario: Test the license analysis for one unknown Maven package
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I send the file maven_one_unknown_package.json to the license analysis service
     Then I should get 200 status code
      And I should find that the license analysis status is failure
      And I should find empty stack license
      And I should not see any conflict packages
      And I should not see any outlier packages
      And I should not see any distinct licenses
      And I should not find any license for package foo.bar:baz version 1.2.3.4
      And I should find that license analysis was not successful for package foo.bar:baz version 1.2.3.4
      And I should not see any component conflicts
      And I should not see any really unknown licenses


  Scenario Outline: Smoketest if all JSON files with package stack can be processes by the stack_license endpoint
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I send the file <filename> to the stack license analysis endpoint of license analysis service 
     Then I should get 200 status code

     Examples: filenames
     |filename|
     |packages_and_alternate_packages.json     |
     |packages_components_license_conflict.json|
     |packages_test_weird_failures.json        |
     |packages_with_compatible_licenses.json   |
     |packages_with_stack_license_conflict.json|
     |packages_with_unknown_license.json       |
     |package_with_no_license.json             |
