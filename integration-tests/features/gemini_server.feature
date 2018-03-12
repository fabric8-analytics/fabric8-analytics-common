Feature: Gemini Server API

    Scenario: Check the POST API endpoint register returns the required information

        Given gemini-server staging pod is running
        When I make a post call to register
        Then I should get 200 status code
         And I should get proper register response

        Given gemini-server staging pod is running
        When I make a post call to register with missing information
        Then I should get 400 status code
         And I should get proper error response




