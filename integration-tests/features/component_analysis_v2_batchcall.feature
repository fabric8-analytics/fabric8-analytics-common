Feature: Component analysis V2 Batch Call API
    @cav2
    Scenario: Check the component analysis V2 REST API Batch Call for NPM ecosystem
        Given System is running
        Given Three scale preview service is running

        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I start CA batch call for test_npm.json with user_key
        Then I should get 202 status code
         And I should receive a valid JSON response
        Then I should be able to validate all the feilds or vulnerablities in the result
        And I should find package sequence 3.0.0 has no recommendation
        And I should find package ejs 1.0.0 has 3.1.3 recommended version
    
     @cav2
    Scenario: Check the component analysis V2 REST API Batch Call for Maven ecosystem
        Given System is running
        Given Three scale preview service is running

        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I start CA batch call for test_maven.json with user_key
        Then I should get 202 status code
         And I should receive a valid JSON response
        Then I should be able to validate all the feilds or vulnerablities in the result
        And I should find package org.apache.tomcat:tomcat-catalina 10.0.0-M5 has no recommendation
        And I should find package org.webjars.npm:openpgp 1.4.1 has 4.7.1 recommended version
    
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
