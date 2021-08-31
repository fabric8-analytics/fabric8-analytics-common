Feature: Component analysis V2 Batch Call API
    @cav2
    Scenario: Check the component analysis V2 REST API Batch Call for NPM ecosystem
        Given System is running
        Given Three scale preview service is running

        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I start CA batch call for test_npm.json with user_key
        Then I should get 200 status code
         And I should receive a valid JSON response
        Then I should be able to validate all the feilds or vulnerablities in the result
        And I should find package sequence 3.0.0 has no recommendation
        And I should find package ejs 1.0.0 has 3.1.6 recommended version
        Then I should find snyk id SNYK-JS-EJS-10218 and 8.1 for package ejs and version 1.0.0
        Then I should find snyk id SNYK-JS-ANGULAR-471882 for package angular and version 1.0.0 as private
         And I should not find any registered user fields
    
     @cav2
    Scenario: Check the component analysis V2 REST API Batch Call for Maven ecosystem
        Given System is running
        Given Three scale preview service is running

        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I start CA batch call for test_maven.json with user_key
        Then I should get 200 status code
         And I should receive a valid JSON response
        Then I should be able to validate all the feilds or vulnerablities in the result
        And I should find package org.apache.tomcat:tomcat-catalina 10.0.0-M5 has no recommendation
        And I should find package org.webjars.npm:openpgp 1.4.1 has 4.7.1 recommended version
        Then I should find snyk id SNYK-JAVA-ORGWEBJARSBOWER-567881 and 6.5 for package org.webjars.bower:jquery and version 3.4.1
        Then I should find snyk id SNYK-JAVA-ORGWEBJARS-479517 for package org.webjars:bootstrap-select and version 1.7.3 as private
         And I should not find any registered user fields
    
    @cav2
    Scenario: Check the component analysis V2 REST API Batch Call for Pypi ecosystem
        Given System is running
        Given Three scale preview service is running

        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I start CA batch call for test_pypi.json with user_key
        Then I should get 200 status code
         And I should receive a valid JSON response
        Then I should be able to validate all the feilds or vulnerablities in the result
        And I should find package numpy 1.16.3 has no recommendation
        And I should find package flask 0.12 has 1.1.2 recommended version
        Then I should find snyk id SNYK-PYTHON-FLASK-42185 and 7.5 for package flask and version 0.12
        Then I should find snyk id SNYK-PYTHON-FASTAPI-569038 for package fastapi and version 0.36.0 as private
         And I should not find any registered user fields
    
    

    @cav2
    Scenario: Check the component analysis V2 REST API Batch Call for unknown ecosystem
        Given System is running
        Given Three scale preview service is running

        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I start CA batch call for invalid_ecosystem.json with user_key
        Then I should get 400 status code
         And I should receive a valid JSON response

    
    @cav2
    Scenario: Check the component analysis V2 REST API Batch Call for unknown packages
        Given System is running
        Given Three scale preview service is running

        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I start CA batch call for invalid_packages.json with user_key
        Then I should get 202 status code
         And I should receive a valid JSON response

     @cav2 @skip
    Scenario: Check the component analysis V2 REST API Batch Call for 1 known 1 unknown package
        Given System is running
        Given Three scale preview service is running

        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I start CA batch call for one_known_one_unknown.json with user_key
        Then I should get 202 status code
         And I should receive a valid JSON response
        Then I should be able to validate all the feilds or vulnerablities in the result
         And I should find one or more unknown packages in result
         And I should find package angular 1.0.0 has 1.8.0 recommended version
          And I should not find any registered user fields

     @cav2
    Scenario: Check the component analysis V2 REST API Batch Call for No vulnerablities
        Given System is running
        Given Three scale preview service is running

        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I start CA batch call for no_vulnerablities.json with user_key
        Then I should get 200 status code
         And I should receive a valid JSON response
        Then I should be able to validate all the feilds or vulnerablities in the result
         And I should not find any vulnerablities in result
    

    @cav2
    Scenario: Check the component analysis V2 REST API Batch Call for an invalid request
        Given System is running
        Given Three scale preview service is running

        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I start CA batch call for invalid_request.json with user_key
        Then I should get 400 status code
         And I should receive a valid JSON response
    
    @cav2
    Scenario: Check the component analysis V2 REST API Batch Call without user key
        Given System is running
        Given Three scale preview service is running

        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I start CA batch call for no_vulnerablities.json without user_key
        Then I should get 403 status code
