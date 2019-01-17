Feature: 3scale API

    Scenario: Check if 3scale staging url requires authentication
       Given 3scale staging pod is running
        When I access get_route API end point for 3scale without authorization
        Then I should get 404 status code
         And I should get proper 3scale error message

    @requires_authorization_token
    Scenario: Check the POST API endpoint get-route returns the required information
       Given 3scale staging pod is running
        When I acquire the authorization token
        Then I should get the proper authorization token
        When I make a post call to 3scale with proper authentication token
        Then I should get 200 status code
         And I should get proper 3scale response

    @requires_authorization_token
    Scenario: Check the POST API endpoint get-route behaviour in case of improper payload
       Given 3scale staging pod is running
        When I acquire the authorization token
        Then I should get the proper authorization token
        When I make a post call to 3scale with proper authentication token and improper payload
        Then I should get 404 status code
         And I should get proper 3scale error message

    @requires_authorization_token
    Scenario: Check the POST API endpoint get-route behaviour in case of empty payload
       Given 3scale staging pod is running
        When I acquire the authorization token
        Then I should get the proper authorization token
        When I make a post call to 3scale with proper authentication token and empty payload
        Then I should get 404 status code
         And I should get proper 3scale error message
