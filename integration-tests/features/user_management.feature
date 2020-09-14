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
        
    Scenario: Request for an invalid user
        Given System is running
        Given Three scale preview service is running
        
            When I acquire the use_key for 3scale
            Then I should get the proper user_key
            When I try to get invalid user with user_key
            Then I should get 404 status code
            Then I should be able to validate the get request
            Then I should get user not found message

