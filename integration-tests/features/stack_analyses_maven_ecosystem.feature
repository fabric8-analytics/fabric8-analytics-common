Feature: Thorough stack analysis v3 API tests for Maven ecosystem


  Scenario: Check that the API entry point requires authorization token
    Given System is running
    When I send Maven package manifest pom.xml to stack analysis version 3 without authorization token
    Then I should get 401 status code


  @requires_authorization_token
  Scenario: Check that the API entry point requires authorization token
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Maven package manifest pom.xml to stack analysis version 3 with authorization token
    Then I should get 200 status code


  @requires_authorization_token
  Scenario: Check that the stack analysis response for the pom.xml that contains only one component
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Maven package manifest pom.xml to stack analysis version 3 with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response containing the id key
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response

    # Timestamp checks
    When I look at recent stack analysis
    Then I should receive JSON response containing the started_at key
     And I should receive JSON response containing the finished_at key
     And I should receive JSON response with the correct timestamp in attribute started_at
     And I should receive JSON response with the correct timestamp in attribute finished_at

    # Request ID check
    When I look at recent stack analysis
    Then I should receive JSON response containing the request_id key

    # Analyzed component check
    When I look at recent stack analysis
    Then I should find analyzed dependency named junit:junit with version 3.8.1 in the stack analysis


  @requires_authorization_token
  Scenario: Check that the stack analysis response for the springboot.xml
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Maven package manifest springboot.xml to stack analysis version 3 with authorization token
    Then I should get 200 status code
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response containing the id key
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code

    # Timestamp checks
    When I look at recent stack analysis
    Then I should receive JSON response containing the started_at key
     And I should receive JSON response containing the finished_at key
     And I should receive JSON response with the correct timestamp in attribute started_at
     And I should receive JSON response with the correct timestamp in attribute finished_at

    # Request ID check
    When I look at recent stack analysis
    Then I should receive JSON response containing the request_id key

    # Analyzed component check
    When I look at recent stack analysis
    Then I should find analyzed dependency named org.springframework:spring-messaging with version 4.3.7.RELEASE in the stack analysis
     And I should find analyzed dependency named org.springframework.boot:spring-boot-starter-web with version 1.5.2.RELEASE in the stack analysis
     And I should find analyzed dependency named org.springframework:spring-websocket with version 4.3.7.RELEASE in the stack analysis
     And I should find analyzed dependency named org.springframework.boot:spring-boot-starter with version 1.5.2.RELEASE in the stack analysis


  @requires_authorization_token
  Scenario: Check that the stack analysis response for the vertx.xml
    Given System is running
    When I acquire the authorization token
    Then I should get the proper authorization token
    When I send Maven package manifest vertx.xml to stack analysis version 3 with authorization token
    Then I should get 200 status code
     And I should receive a valid JSON response
     And I should receive JSON response containing the id key
    When I wait for stack analysis version 3 to finish with authorization token
    Then I should get 200 status code

    # Timestamp checks
    When I look at recent stack analysis
    Then I should receive JSON response containing the started_at key
     And I should receive JSON response containing the finished_at key
     And I should receive JSON response with the correct timestamp in attribute started_at
     And I should receive JSON response with the correct timestamp in attribute finished_at

    # Request ID check
    When I look at recent stack analysis
    Then I should receive JSON response containing the request_id key

    # Analyzed component check
    When I look at recent stack analysis
    Then I should find analyzed dependency named io.vertx:vertx-core with version 3.4.1 in the stack analysis
     And I should find analyzed dependency named io.vertx:vertx-web-templ-freemarker with version 3.4.1 in the stack analysis
     And I should find analyzed dependency named io.vertx:vertx-jdbc-client with version 3.4.1 in the stack analysis
     And I should find analyzed dependency named io.vertx:vertx-web with version 3.4.1 in the stack analysis
     And I should find analyzed dependency named io.vertx:vertx-web-templ-handlebars with version 3.4.1 in the stack analysis
     And I should find analyzed dependency named io.vertx:vertx-rx-java with version 3.4.1 in the stack analysis
     And I should find analyzed dependency named io.vertx:vertx-web-client with version 3.4.1 in the stack analysis

