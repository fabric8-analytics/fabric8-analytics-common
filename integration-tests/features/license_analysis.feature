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
     |filename|
     |maven_five_different_packages.json|
     |maven_one_package.json|
     |maven_three_wildfly_packages.json|
