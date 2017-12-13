Feature: 3scale API

    Scenario: Check if 3scale staging url requires authentication
        Given 3scale staging pod is running
        When I access get_route API end point for 3scale without authorization
        Then I should get 404 status code as response

    @requires_authorization_token
    Scenario: Check the POST API  endpoint get-route returns the required information
        When I acquire the authorization token
        Then I should get the proper authorization token
        Given 3scale staging pod is running
        When I make a post call with proper authentication token
        Then I should get json object