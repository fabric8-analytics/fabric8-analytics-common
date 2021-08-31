Feature: User Management API
    
    Scenario: Get UUID via post call
     Given System is running
        Given Three scale preview service is running
        
            When I acquire the use_key for 3scale
            Then I should get the proper user_key
            When I request user api for new UUID with user_key
            Then I should get 200 status code
            Then I should be able to validate post or put request
    
    Scenario: Trying out the API without user key
      Given System is running
        Given Three scale preview service is running
        
            When I acquire the use_key for 3scale
            Then I should get the proper user_key
            When I request user api for new UUID without user_key
            Then I should get 403 status code
            When I try the put call with snyk token and id without user_key
            Then I should get 403 status code
            When I try to get user without user_key
            Then I should get 403 status code 
    
    Scenario: Test PUT call via valid synk token
     Given System is running
        Given Three scale preview service is running
        
            When I acquire the use_key for 3scale
            Then I should get the proper user_key
            When I request user api for new UUID with user_key
            Then I should get 200 status code
            Then I should be able to validate post or put request
            When I try the put call with snyk token and id with user_key
            Then I should get 200 status code
            Then I should be able to validate post or put request
            When I try to get user with user_key
            Then I should be able to validate the get request
            Then I should get status as registered
    
    Scenario: Trying with a invalid synk token
     Given System is running
        Given Three scale preview service is running
        
            When I acquire the use_key for 3scale
            Then I should get the proper user_key
            When I request user api for new UUID with user_key
            Then I should get 200 status code
            Then I should be able to validate post or put request
            When I try the put call with invalid snyk token with user_key
            Then I should get 400 status code
    @skip  
    Scenario: Request for an invalid user
        Given System is running
        Given Three scale preview service is running
        
            When I acquire the use_key for 3scale
            Then I should get the proper user_key
            When I try to get invalid user with user_key
            Then I should get 404 status code
            Then I should be able to validate the get request
            Then I should get user not found message
    @skip
    Scenario: Request for an Free Tier user
        Given System is running
        Given Three scale preview service is running
        
            When I acquire the use_key for 3scale
            Then I should get the proper user_key
            When I request user api for new UUID with user_key
            Then I should get 200 status code
            Then I should be able to validate post or put request
            When I try to get user with user_key
            Then I should get 404 status code
            Then I should be able to validate the get request
            Then I should get user not found message
    
    Scenario: Test Component analysis batch call with user mmannagement 
         Given System is running
            Given Three scale preview service is running
        
            When I acquire the use_key for 3scale
            Then I should get the proper user_key
            When I request user api for new UUID with user_key
            Then I should get 200 status code
            Then I should be able to validate post or put request
            When I try the put call with snyk token and id with user_key
            Then I should get 200 status code
            Then I should be able to validate post or put request
            When I try to get user with user_key
            Then I should be able to validate the get request
            Then I should get status as registered
            When I start CA registered user batch call for test_npm.json with user_key
            Then I should get 200 status code
            And I should receive a valid JSON response
            Then I should be able to validate all the feilds or vulnerablities in the result with userid
            And I should find package sequence 3.0.0 has no recommendation
            And I should find package ejs 1.0.0 has 3.1.6 recommended version
            Then I should find snyk id SNYK-JS-EJS-10218 and 8.1 for package ejs and version 1.0.0
            Then I should find snyk id SNYK-JS-ANGULAR-471882 for package angular and version 1.0.0 as private
            Then I should find all the registered user fields in result
            Then I should find package marked 0.3.4 has 1 expolits and https://snyk.io/vuln/npm:marked vendor link
    
    Scenario: Component analysis batch call with UUID without token
        Given System is running
        Given Three scale preview service is running
        
            When I acquire the use_key for 3scale
            Then I should get the proper user_key
            When I request user api for new UUID with user_key
            Then I should get 200 status code
            Then I should be able to validate post or put request
            When I start CA registered user batch call for test_npm.json with user_key
            Then I should get 200 status code
            And I should receive a valid JSON response
            Then I should be able to validate all the feilds or vulnerablities in the result
            And I should find package sequence 3.0.0 has no recommendation
            And I should find package ejs 1.0.0 has 3.1.6 recommended version
            Then I should find snyk id SNYK-JS-EJS-10218 and 8.1 for package ejs and version 1.0.0
            Then I should find snyk id SNYK-JS-ANGULAR-471882 for package angular and version 1.0.0 as private
            And I should not find any registered user fields
    
    Scenario: Testing Component Analysis Batch Call with valid UUID for all ecosystems
        Given System is running
            Given Three scale preview service is running
        
            When I acquire the use_key for 3scale
            Then I should get the proper user_key
            When I request user api for new UUID with user_key
            Then I should get 200 status code
            Then I should be able to validate post or put request
            When I try the put call with snyk token and id with user_key
            Then I should get 200 status code
            Then I should be able to validate post or put request
            When I try to get user with user_key
            Then I should be able to validate the get request
            Then I should get status as registered
            When I start CA registered user batch call for test_npm.json with user_key
            Then I should get 200 status code
            And I should receive a valid JSON response
            Then I should be able to validate all the feilds or vulnerablities in the result with userid
            Then I should find all the registered user fields in result
            When I start CA registered user batch call for test_maven.json with user_key
            Then I should get 200 status code
            And I should receive a valid JSON response
            Then I should be able to validate all the feilds or vulnerablities in the result with userid
            Then I should find all the registered user fields in result
            When I start CA registered user batch call for test_pypi.json with user_key
            Then I should get 200 status code
            And I should receive a valid JSON response
            Then I should be able to validate all the feilds or vulnerablities in the result with userid
            Then I should find all the registered user fields in result
    
    Scenario: Testing Component analysis batch call with invalid UUID
        Given System is running
        Given Three scale preview service is running
        
            When I acquire the use_key for 3scale
            Then I should get the proper user_key
            When I start CA registered user batch call for test_npm.json with user_key with invalid uuid
            Then I should get 400 status code
            And I should receive a valid JSON response
    
    Scenario Outline: Test Stack Analysis Call with user management for all ecosystems
         Given System is running
            Given Three scale preview service is running
        
            When I acquire the use_key for 3scale
            Then I should get the proper user_key
            When I request user api for new UUID with user_key
            Then I should get 200 status code
            Then I should be able to validate post or put request
            When I try the put call with snyk token and id with user_key
            Then I should get 200 status code
            Then I should be able to validate post or put request
            When I try to get user with user_key
            Then I should be able to validate the get request
            Then I should get status as registered
            When I send <ecosystem> package request with manifest <manifest> to stack analysis v2 with valid user key with uuid
            Then I should get 200 status code
            And I should receive JSON response containing the status key
            And I should receive JSON response containing the id key
            And I should receive JSON response containing the submitted_at key
            And I should receive JSON response with the status key set to success
            And I should receive JSON response with the correct id
            And I should receive JSON response with the correct timestamp in attribute submitted_at
            When I wait for stack analysis v2 to finish with user key with uuid
            Then I should find premium vulnerablities in result
        
            Examples: Stack analyses POST params
            | ecosystem | manifest               |
            #| pypi      | pylist.json            |
            | npm       | valid_npmlist.json     |
            | maven     | vertx_dependencies.txt |
    
    
    Scenario: Test Stack Analysis with an invalid UUID
        Given System is running
        Given Three scale preview service is running
        
            When I acquire the use_key for 3scale
            Then I should get the proper user_key
            When I send npm package request with manifest valid_npmlist.json to stack analysis v2 with valid user key with invalid uuid 
            Then I should get 400 status code
            And I should receive a valid JSON response
    
    Scenario: Test Stack Analysis with an UUID which is not associated with any token
        Given System is running
        Given Three scale preview service is running
        
            When I acquire the use_key for 3scale
            Then I should get the proper user_key
            When I request user api for new UUID with user_key
            Then I should get 200 status code
            Then I should be able to validate post or put request
             When I send npm package request with manifest valid_npmlist.json to stack analysis v2 with valid user key with uuid
            Then I should get 200 status code
            And I should receive JSON response containing the status key
            And I should receive JSON response containing the id key
            And I should receive JSON response containing the submitted_at key
            And I should receive JSON response with the status key set to success
            And I should receive JSON response with the correct id
            And I should receive JSON response with the correct timestamp in attribute submitted_at
            When I wait for stack analysis v2 to finish with user key with uuid
            Then I should get stack analyses v2 response with all attributes







