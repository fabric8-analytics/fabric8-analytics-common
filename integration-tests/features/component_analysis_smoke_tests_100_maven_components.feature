Feature: Smoke tests for the component analysis REST API


  Scenario Outline: Check the component analysis REST API endpoint for 100 most popular PyPi components
   Given System is running
    Given Three scale preview service is running
    When I wait 2 seconds
    When I acquire the use_key for 3scale
    Then I should get the proper user_key

     When I start component analyses <ecosystem>/<package>/<version> with user_key
     Then I should get 200 status code
      And I should receive a valid JSON response

     When I look at the component analysis duration
     Then I should see that the component analysis duration is less than 10 second

     When I look at recent component analysis
     Then I should receive JSON response containing the result key
      And I should find at least one analyzed package in the component analysis
      And I should find the package <package> from <ecosystem> ecosystem in the component analysis
      And I should find the component <package> version <version> from <ecosystem> ecosystem in the component analysis
      And I should find new recommended version in case the CVE is detected for an analyzed component
      And I should find CVE report in case the CVE is detected for an analyzed component

     Examples: EPV
     | ecosystem  | package                                                 | version              |
     | maven      | junit:junit                                             | 4.13-beta-3          | #1
     | maven      | org.slf4j:slf4j-api                                     | 2.0.0-alpha0         | #2
     | maven      | com.android.tools.build:gradle                          | 2.3.0                | #3
     | maven      | log4j:log4j                                             | 1.2.17               | #4
     | maven      | com.google.guava:guava                                  | 28.0-jre             | #5
     | maven      | org.mockito:mockito-core                                | 3.0.0                | #6
     | maven      | org.slf4j:slf4j-log4j12                                 | 2.0.0-alpha0         | #7
     | maven      | org.mockito:mockito-all                                 | 2.0.2-beta           | #8
     | maven      | org.scala-lang:scala-library                            | 2.13.0               | #9
     | maven      | commons-io:commons-io                                   | 2.6                  | #10
     | maven      | commons-logging:commons-logging                         | 1.2                  | #11
     | maven      | commons-lang:commons-lang                               | 2.6                  | #12
     | maven      | javax.servlet:servlet-api                               | 3.0-alpha-1          | #13
     | maven      | ch.qos.logback:logback-classic                          | 1.3.0-alpha4         | #14
     | maven      | org.apache.hadoop:hadoop-common                         | 3.2.0                | #15
     | maven      | javax.servlet:javax.servlet-api                         | 4.0.1                | #16
     | maven      | org.testng:testng                                       | 7.0.0-beta7          | #17
     | maven      | org.apache.commons:commons-lang3                        | 3.9                  | #18
     | maven      | org.hamcrest:hamcrest-library                           | 2.1                  | #19
     | maven      | com.fasterxml.jackson.core:jackson-databind             | 2.10.0.pr1           | #20
     | maven      | commons-codec:commons-codec                             | 1.13                 | #21
     | maven      | org.springframework:spring-context                      | 5.1.9.RELEASE        | #22
     | maven      | com.google.code.findbugs:jsr305                         | 3.0.2                | #23
     | maven      | org.springframework.boot:spring-boot-starter-test       | 2.1.7.RELEASE        | #24
     | maven      | org.apache.httpcomponents:httpclient                    | 4.5.9                | #25
     | maven      | org.springframework.boot:spring-boot-starter-web        | 2.1.7.RELEASE        | #26
     | maven      | mysql:mysql-connector-java                              | 8.0.17               | #27
     | maven      | com.google.code.gson:gson                               | 2.8.5                | #28
     | maven      | org.springframework:spring-core                         | 5.1.9.RELEASE        | #29
     | maven      | junit:junit-dep                                         | 4.11                 | #30
     | maven      | org.springframework:spring-test                         | 5.1.9.RELEASE        | #31
     | maven      | org.easymock:easymock                                   | 4.0.2                | #32
     | maven      | joda-time:joda-time                                     | 2.10.3               | #33
     | maven      | org.slf4j:slf4j-simple                                  | 2.0.0-alpha0         | #34
     | maven      | org.hamcrest:hamcrest-core                              | 2.1                  | #35
     | maven      | org.hamcrest:hamcrest-all                               | 1.3                  | #36
     | maven      | org.slf4j:jcl-over-slf4j                                | 2.0.0-alpha0         | #37
     | maven      | org.springframework:spring-web                          | 5.1.9.RELEASE        | #38
     | maven      | org.apache.hadoop:hadoop-hdfs                           | 3.2.0                | #39
     | maven      | commons-collections:commons-collections                 | 20040616             | #40
     | maven      | org.assertj:assertj-core                                | 3.13.2               | #41
     | maven      | org.projectlombok:lombok                                | 1.18.8               | #42
     | maven      | com.h2database:h2                                       | 1.4.199              | #43
     | maven      | org.springframework:spring-beans                        | 5.1.9.RELEASE        | #44
     | maven      | org.springframework:spring-webmvc                       | 5.1.9.RELEASE        | #45
     | maven      | commons-cli:commons-cli                                 | 1.4                  | #46
     | maven      | com.fasterxml.jackson.core:jackson-core                 | 2.10.0.pr1           | #47
     | maven      | javax.ws.rs:jsr311-api                                  | 1.1.1                | #48
     | maven      | org.codehaus.jackson:jackson-mapper-asl                 | 1.9.11               | #49
     | maven      | com.fasterxml.jackson.core:jackson-annotations          | 2.10.0.pr1           | #50
     | maven      | org.apache.felix:org.apache.felix.scr.ds-annotations    | 1.2.10               | #51
     | maven      | com.google.api-client:google-api-client                 | 1.30.2               | #52
     | maven      | org.apache.logging.log4j:log4j-core                     | 2.12.1               | #53
     | maven      | org.hibernate:hibernate-core                            | 6.0.0.Alpha2         | #54
     | maven      | org.springframework:spring-jdbc                         | 5.1.9.RELEASE        | #55
     | maven      | org.apache.hadoop:hadoop-client                         | 3.2.0                | #56
     | maven      | org.hsqldb:hsqldb                                       | 2.5.0                | #57
     | maven      | org.scalatest:scalatest_2.11                            | 3.2.0-SNAP10         | #58
     | maven      | org.springframework:spring-tx                           | 5.1.9.RELEASE        | #59
     | maven      | org.slf4j:jul-to-slf4j                                  | 2.0.0-alpha0         | #60
     | maven      | org.springframework.boot:spring-boot-starter-data-jpa   | 2.1.7.RELEASE        | #61
     | maven      | com.google.inject:guice                                 | 4.2.2                | #62
     | maven      | org.clojure:clojure                                     | 1.10.1               | #63
     | maven      | org.hibernate:hibernate-validator                       | 6.1.0.Alpha6         | #64
     | maven      | javax.inject:javax.inject                               | 1                    | #65
     | maven      | com.google.protobuf:protobuf-java                       | 3.9.1                | #66
     | maven      | org.codehaus.jackson:jackson-core-asl                   | 1.9.11               | #67
     | maven      | javax.xml.bind:jaxb-api                                 | 2.4.0-b180830.0359   | #68
     | maven      | org.springframework:spring-context-support              | 5.1.9.RELEASE        | #69
     | maven      | org.jmock:jmock-junit4                                  | 2.12.0               | #70
     | maven      | org.osgi:org.osgi.core                                  | 6.0.0                | #71
     | maven      | org.scala-lang:scala-reflect                            | 2.13.0               | #72
     | maven      | org.springframework:spring-aop                          | 5.1.9.RELEASE        | #73
     | maven      | org.scalatest:scalatest_2.10                            | 3.2.0-SNAP10         | #74
     | maven      | javax.validation:validation-api                         | 2.0.1.Final          | #75
     | maven      | com.amazonaws:aws-java-sdk-core                         | 1.11.607             | #76
     | maven      | org.hibernate:hibernate-entitymanager                   | 5.4.4.Final          | #77
     | maven      | org.apache.hadoop:hadoop-mapreduce-client-core          | 3.2.0                | #78
     | maven      | org.eclipse.jetty:jetty-server                          | 10.0.0-alpha0        | #79
     | maven      | org.wso2.carbon:org.wso2.carbon.core                    | 5.2.8                | #80
     | maven      | org.springframework:spring-orm                          | 5.1.9.RELEASE        | #81
     | maven      | org.apache.httpcomponents:httpcore                      | 4.4.11               | #82
     | maven      | org.apache.zookeeper:zookeeper                          | 3.5.5                | #83
     | maven      | org.apache.logging.log4j:log4j-slf4j-impl               | 2.12.1               | #84
     | maven      | org.json:json                                           | 20190722             | #85
     # | maven      | org.codehaus.groovy:groovy-all                          | 3.0.0-beta-3         | #86
     | maven      | org.powermock:powermock-module-junit4                   | 2.0.2                | #87
     | maven      | org.apache.hadoop:hadoop-annotations                    | 3.2.0                | #88
     | maven      | com.google.gms:google-services                          | 3.1.1                | #89
     | maven      | org.apache.logging.log4j:log4j-api                      | 2.12.1               | #90
     # | maven      | org.wso2.carbon:org.wso2.carbon.logging                 | 5.1.0-m2             | #91
     | maven      | io.vertx:vertx-core                                     | 3.4.1                | #92
     | maven      | io.vertx:vertx-jdbc-client                              | 3.4.1                | #93
     | maven      | io.vertx:vertx-rx-java                                  | 3.4.1                | #94
     | maven      | io.vertx:vertx-web-client                               | 3.4.1                | #95
     | maven      | io.vertx:vertx-web-templ-freemarker                     | 3.4.1                | #96
     | maven      | io.vertx:vertx-web-templ-handlebars                     | 3.4.1                | #97
     | maven      | io.vertx:vertx-web                                      | 3.4.1                | #98
     | maven      | org.springframework:spring-messaging                    | 4.3.7.RELEASE        | #99
     | maven      | org.springframework:spring-websocket                    | 4.3.7.RELEASE        | #100
