Feature: Crowdsourcing API

    Scenario: Check if get master tags list requires authorization
        Given Master tag list api is running
        When I access master tag list API point for ecosystem maven without authorization token
        Then I should get 401 status code as response for master tag list

    @requires_authorization_token
    Scenario: Check the get master tags list API entry point for ecosystem maven
        Given Master tag list api is running
        When I acquire the authorization token
        Then I should get the proper authorization token
        When I access master tag list API point for ecosystem maven with authorization token
        Then I should get json object contains tag_list which is an array of strings


    Scenario: Check get next untagged component API entry point without authorization token
        Given get next untagged component api is running
        When I access get next untagged component for ecosystem maven without authorization token
        Then I should get 401 status code as response for next untagged component

    @requires_authorization_token
    Scenario Outline: Check the get next untagged component API entry point with authorization token
        Given get next untagged component api is running
        When I acquire the authorization token
        Then I should get the proper authorization token
        When I access get next untagged component for ecosystem <ecosystem> with authorization token
        Then I should get a 200 status code and component as <response> type

        Examples: ecosystems
            |ecosystem      |  response |
            |maven          |  str      |
            |node           |  dict     |
            |pypi           |  dict     |


    Scenario: Check set tags API entry point without authorization token
        Given System is running
        When I access set tags api endpoint without authorization token
        Then I should get 401 status code as response for set tags api endpoint

    @requires_authorization_token
    Scenario: Check the set tags API entry point
        Given System is running
        When I acquire the authorization token
        Then I should get the proper authorization token
        When I post invalid json input to the set tags endpoint
        Then I should get a 400 status code as response
