Feature: Check the implementation of test steps

  @selfcheck
  Scenario: Check that the stack analysis response for the pom.xml that contains only one component
    Given System is running
    When I mock API response by data/mock_stack_analysis_v2_junit.json file
    Then I should find analyzed dependency named junit:junit with version 3.8.1 in the stack analysis
    Then I should find that none analyzed package can be found in companion packages as well
    Then I should receive JSON response with the correct timestamp in attribute started_at
    Then I should receive JSON response with the correct timestamp in attribute finished_at
    Then I should find proper timestamp under the path result/0/_audit/started_at
    Then I should find proper timestamp under the path result/0/_audit/ended_at
    Then I should find the proper sentiment values in the stack analysis response
    Then I should find the following licenses (Apache 2.0, EPL 1.0, MIT License, ASL 2.0, Free Art, MITNFA, Forbidden Phrase) under the path result/0/recommendations/companion

  @selfcheck
  Scenario: Check that the stack analysis response for the springboot.xml
    Given System is running
    When I download and parse outlier probability threshold value
    Then I should have outlier probability threshold value between 0.0 and 1.0
    When I mock API response by data/mock_stack_analysis_v2_springboot.json file
    Then I should receive JSON response with the correct timestamp in attribute started_at
    Then I should receive JSON response with the correct timestamp in attribute finished_at
    Then I should find proper timestamp under the path result/0/_audit/started_at
    Then I should find proper timestamp under the path result/0/_audit/ended_at
    Then I should find the proper sentiment values in the stack analysis response
    Then I should find that alternate components replace user components
    Then I should find that none analyzed package can be found in companion packages as well
    Then I should find analyzed dependency named org.springframework:spring-messaging with version 4.3.7.RELEASE in the stack analysis
    Then I should find analyzed dependency named org.springframework.boot:spring-boot-starter-web with version 1.5.2.RELEASE in the stack analysis
    Then I should find analyzed dependency named org.springframework:spring-websocket with version 4.3.7.RELEASE in the stack analysis
    Then I should find analyzed dependency named org.springframework.boot:spring-boot-starter with version 1.5.2.RELEASE in the stack analysis
    Then I should find the proper outlier record for the org.springframework:spring-messaging component
    Then I should find the proper outlier record for the org.springframework.boot:spring-boot-starter component
    Then I should find the proper outlier record for the org.springframework.boot:spring-boot-starter-web component

  @selfcheck
  Scenario: Check that the stack analysis response for the vertx.xml
    Given System is running
    When I download and parse outlier probability threshold value
    Then I should have outlier probability threshold value between 0.0 and 1.0
    When I mock API response by data/mock_stack_analysis_v2_vertx.json file
    Then I should receive JSON response with the correct timestamp in attribute started_at
    Then I should receive JSON response with the correct timestamp in attribute finished_at
    Then I should find proper timestamp under the path result/0/_audit/started_at
    Then I should find proper timestamp under the path result/0/_audit/ended_at
    Then I should find analyzed dependency named io.vertx:vertx-core with version 3.4.1 in the stack analysis
    Then I should find analyzed dependency named io.vertx:vertx-web-templ-freemarker with version 3.4.1 in the stack analysis
    Then I should find analyzed dependency named io.vertx:vertx-jdbc-client with version 3.4.1 in the stack analysis
    Then I should find analyzed dependency named io.vertx:vertx-web with version 3.4.1 in the stack analysis
    Then I should find analyzed dependency named io.vertx:vertx-web-templ-handlebars with version 3.4.1 in the stack analysis
    Then I should find analyzed dependency named io.vertx:vertx-rx-java with version 3.4.1 in the stack analysis
    Then I should find analyzed dependency named io.vertx:vertx-web-client with version 3.4.1 in the stack analysis

