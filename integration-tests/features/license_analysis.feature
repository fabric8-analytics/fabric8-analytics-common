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
      And I should receive a valid JSON response
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
      And I should receive a valid JSON response
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
      And I should receive a valid JSON response
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
     |filename                                 |
     |package_with_one_license.json            |
     |package_with_two_licenses_A.json         |
     |package_with_two_licenses_B.json         |
     |package_with_no_license.json             |
     |packages_and_alternate_packages.json     |
     |packages_components_license_conflict.json|
     |packages_test_weird_failures.json        |
     |packages_with_compatible_licenses.json   |
     |packages_with_stack_license_conflict.json|
     |packages_with_unknown_license.json       |


  Scenario Outline: Check the stack license computation for all correct input files
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I send the file <filename> to the stack license analysis endpoint of license analysis service 
     Then I should get 200 status code
      And I should receive a valid JSON response
      And I should find that the stack license is <license>

     Examples: filenames with stack computation results
     |filename                                          |license |
     |package_with_one_license.json                     |mit     |
     |package_with_two_licenses_A.json                  |mit     |
     |package_with_two_licenses_B.json                  |gplv2   |
     |packages_and_alternate_packages.json              |gplv2   |
     |packages_with_compatible_licenses.json            |gplv2   |
     |package_with_four_licenses.json                   |gplv2   |
     |package_with_three_licenses_A.json                |bsd-new |
     |package_with_three_licenses_B.json                |gplv2   |


  Scenario Outline: Check the stack license computation for all input files where the stack license can't be figured out
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I send the file <filename> to the stack license analysis endpoint of license analysis service 
     Then I should get 200 status code
      And I should receive a valid JSON response
      And I should find empty stack license

     Examples: filenames
     |filename                                  |
     |package_with_no_license.json              |
     |packages_components_license_conflict.json |
     |packages_with_stack_license_conflict.json |
     |packages_with_unknown_license.json        |


  Scenario: Test the stack license analysis for one package with one license
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I send the file package_with_one_license.json to the stack license analysis endpoint of license analysis service 
     Then I should get 200 status code

      # overall status
      And I should receive a valid JSON response
      And I should find that the license analysis status is successful
      And I should not see any conflict packages
      And I should see one distinct license
      And I should find mit license in distinct licenses
      And I should not see any outlier packages

      # stack license
      And I should find that the stack license is mit

      # package p1 version 1.1
      And I should find license MIT for the package p1 version 1.1
      And I should find that representative license has been found for package p1 version 1.1
      And I should find that license analysis was successful for package p1 version 1.1


  Scenario: Test the stack license analysis for one package with two licenses
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I send the file package_with_two_licenses_A.json to the stack license analysis endpoint of license analysis service 
     Then I should get 200 status code

      # overall status
      And I should receive a valid JSON response
      And I should find that the license analysis status is successful
      And I should not see any conflict packages
      And I should not see any outlier packages

      # stack license
      And I should find that the stack license is mit

      # distinct licenses check
      And I should see 2 distinct licenses
      And I should find mit license in distinct licenses
      And I should find public domain license in distinct licenses

      # package p1 version 1.1
      And I should find license MIT for the package p1 version 1.1
      And I should find license PD for the package p1 version 1.1
      And I should find that representative license has been found for package p1 version 1.1
      And I should find that license analysis was successful for package p1 version 1.1


  Scenario: Test the stack license analysis for one package with two licenses
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I send the file package_with_two_licenses_B.json to the stack license analysis endpoint of license analysis service 
     Then I should get 200 status code
      And I should receive a valid JSON response
      And I should find that the license analysis status is successful
      And I should not see any conflict packages
      And I should not see any outlier packages

      # stack license
      And I should find that the stack license is gplv2

      # distinct licenses check
      And I should see 2 distinct licenses
      And I should find gplv2 license in distinct licenses
      And I should find bsd-new license in distinct licenses

      # package p2 version 1.1
      And I should find license BSD for the package p2 version 1.1
      And I should find license GPL V2 for the package p2 version 1.1
      And I should find that representative license has been found for package p2 version 1.1
      And I should find that license analysis was successful for package p2 version 1.1


  Scenario: Test the stack license analysis for one package with three licenses, variant A
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I send the file package_with_three_licenses_A.json to the stack license analysis endpoint of license analysis service 
     Then I should get 200 status code

      # overall status
      And I should receive a valid JSON response
      And I should find that the license analysis status is successful
      And I should not see any conflict packages
      And I should not see any outlier packages

      # stack license
      And I should find that the stack license is bsd-new

      # distinct licenses check
      And I should see 3 distinct licenses
      And I should find mit license in distinct licenses
      And I should find public domain license in distinct licenses
      And I should find bsd-new license in distinct licenses

      # package p1 version 1.1
      And I should find license MIT for the package p1 version 1.1
      And I should find license BSD for the package p1 version 1.1
      And I should find license PD for the package p1 version 1.1
      And I should find that representative license has been found for package p1 version 1.1
      And I should find that license analysis was successful for package p1 version 1.1


  Scenario: Test the stack license analysis for one package with three licenses, variant B
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I send the file package_with_three_licenses_B.json to the stack license analysis endpoint of license analysis service 
     Then I should get 200 status code

      # overall status
      And I should receive a valid JSON response
      And I should find that the license analysis status is successful
      And I should not see any conflict packages
      And I should not see any outlier packages

      # stack license
      And I should find that the stack license is gplv2

      # distinct licenses check
      And I should see 3 distinct licenses
      And I should find gplv2 license in distinct licenses
      And I should find public domain license in distinct licenses
      And I should find bsd-new license in distinct licenses

      # package p1 version 1.1
      And I should find license GPL V2 for the package p1 version 1.1
      And I should find license BSD for the package p1 version 1.1
      And I should find license PD for the package p1 version 1.1
      And I should find that representative license has been found for package p1 version 1.1
      And I should find that license analysis was successful for package p1 version 1.1


  Scenario: Test the stack license analysis for one package without any license
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I send the file package_with_no_license.json to the stack license analysis endpoint of license analysis service 
     Then I should get 200 status code

      # overall status
      And I should receive a valid JSON response
      And I should find that the license analysis status is failure
      And I should not see any conflict packages
      And I should not see any distinct licenses
      And I should not see any outlier packages
      And I should find that representative license has not been found for package p1 version 1.1 with the reason Input is invalid

      # stack license
      And I should find empty stack license


  Scenario: Test the stack license analysis for two packages with compatible licenses
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I send the file packages_with_compatible_licenses.json to the stack license analysis endpoint of license analysis service 
     Then I should get 200 status code

      # overall status
      And I should receive a valid JSON response
      And I should find that the license analysis status is successful
      And I should not see any conflict packages
      And I should not see any outlier packages

      # stack license
      And I should find that the stack license is gplv2

      # distinct licenses check
      And I should see 4 distinct licenses
      And I should find public domain license in distinct licenses
      And I should find mit license in distinct licenses
      And I should find gplv2 license in distinct licenses
      And I should find bsd-new license in distinct licenses

      # package p1 version 1.1
      And I should find license MIT for the package p1 version 1.1
      And I should find license PD for the package p1 version 1.1
      And I should find that representative license has been found for package p1 version 1.1
      And I should find that license analysis was successful for package p1 version 1.1

      # package p2 version 1.1
      And I should find license BSD for the package p2 version 1.1
      And I should find license GPL V2 for the package p2 version 1.1
      And I should find that representative license has been found for package p2 version 1.1
      And I should find that license analysis was successful for package p2 version 1.1


  Scenario: Test the stack license analysis for two packages that have license conflict
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I send the file packages_components_license_conflict.json to the stack license analysis endpoint of license analysis service 
     Then I should get 200 status code

      # overall status
      And I should receive a valid JSON response
      And I should find that the license analysis failed because of component conflict
      And I should see that the analysis message says "No declared licenses found for 0 component(s)."
      And I should not see any conflict packages
      And I should not see any outlier packages

      # stack license
      And I should find empty stack license

      # distinct licenses check
      And I should see 4 distinct licenses
      And I should find public domain license in distinct licenses
      And I should find gplv2 license in distinct licenses
      And I should find gplv3+ license in distinct licenses
      And I should find apache 2.0 license in distinct licenses

      # package p1 version 1.1
      And I should find license APACHE for the package p1 version 1.1
      And I should find license PD for the package p1 version 1.1
      And I should find that representative license has been found for package p1 version 1.1
      And I should find that license analysis was successful for package p1 version 1.1

      # package p2 version 1.1
      And I should find license GPL V2 for the package p2 version 1.1
      And I should find license GPL V3+ for the package p2 version 1.1
      And I should find that representative license has not been found for package p2 version 1.1 with the reason Some licenses are in conflict
      And I should find that license analysis was conflict for package p2 version 1.1
      And I should find the gplv2 license in conflict licenses for the package p2 version 1.1
      And I should find the gplv3+ license in conflict licenses for the package p2 version 1.1


  Scenario: Test the stack license analysis for two packages that have stack conflict
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token
     When I send the file packages_with_stack_license_conflict.json to the stack license analysis endpoint of license analysis service 
     Then I should get 200 status code

      # overall status
      And I should receive a valid JSON response
      And I should find that the license analysis failed because of stack conflict
      And I should not see any outlier packages

      # stack license
      And I should find empty stack license

      # distinct licenses check
      And I should see 4 distinct licenses
      And I should find gplv2 license in distinct licenses
      And I should find gplv3+ license in distinct licenses
      And I should find bsd-new license in distinct licenses
      And I should find apache 2.0 license in distinct licenses

      # conflict packages check
      And I should see one group of conflict packages
      And I should see the license gplv3+ for package p1 in the first group of conflict packages
      And I should see the license gplv2 for package p2 in the first group of conflict packages

      # package p1 version 1.1
      And I should find license APACHE for the package p1 version 1.1
      And I should find license GPL V3+ for the package p1 version 1.1
      And I should find that representative license has been found for package p1 version 1.1
      And I should find that license analysis was successful for package p1 version 1.1

      # package p2 version 1.1
      And I should find license BSD for the package p2 version 1.1
      And I should find license GPL V2 for the package p2 version 1.1
      And I should find that representative license has been found for package p1 version 1.1
      And I should find that license analysis was successful for package p2 version 1.1
