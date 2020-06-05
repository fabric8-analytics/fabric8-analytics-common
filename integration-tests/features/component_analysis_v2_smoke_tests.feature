Feature: Smoke Tests Component Analysis v2

   Scenario Outline: Check the component analysis REST API endpoint for 20 most popular NPM components
    Given System is running
    Given Three scale preview service is running
      
      When I acquire the use_key for 3scale
      Then I should get the proper user_key
       When I wait 2 seconds
      When I start v2 component analyses <ecosystem>/<package>/<version> with user_key
      Then I should get 200 status code
        And I should receive a valid JSON response

      When I look at the component analysis duration
      Then I should see that the component analysis duration is less than 5 second
      
      Then I should get no result or recommendation with report
      

      Examples: EPV
     | ecosystem  | package             | version              |
     | npm        | ejs                 | 1.0.0                | #1
     | npm        | request             | 2.88.0               | #2
     | npm        | chalk               | 2.4.2                | #3
     | npm        | commander           | 2.20.0               | #4
     | npm        | express             | 4.17.1               | #5
     | npm        | async               | 3.1.0                | #6
     | npm        | react               | 16.8.6               | #7
     | npm        | debug               | 4.1.1                | #8
     | npm        | underscore          | 1.9.1                | #9
     | npm        | bluebird            | 3.5.5                | #10
     | npm        | moment              | 2.24.0               | #11
     | npm        | fs-extra            | 8.1.0                | #12
     | npm        | react-dom           | 16.8.6               | #13
     | npm        | mkdirp              | 0.5.1                | #14
     | npm        | prop-types          | 15.7.2               | #15
     | npm        | colors              | 1.3.3                | #16
     | npm        | glob                | 7.1.4                | #17
     | npm        | body-parser         | 1.19.0               | #18
     | npm        | yargs               | 13.3.0               | #19
     | npm        | minimist            | 1.2.0                | #20


  Scenario Outline:  Check the component analysis V2 REST API endpoint for 20 most popular PyPi components
    Given System is running
    Given Three scale preview service is running
        
        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I wait 2 seconds
        When I start v2 component analyses <ecosystem>/<package>/<version> with user_key
        Then I should get 200 status code
            And I should receive a valid JSON response

        When I look at the component analysis duration
        Then I should see that the component analysis duration is less than 5 second
      
        Then I should get no result or recommendation with report

         Examples: EPV
        | ecosystem  | package             | version              |
        | pypi       | pip                 | 19.2.1               | #1
        | pypi       | urllib3             | 1.25.3               | #2
        | pypi       | botocore            | 1.12.202             | #3
        | pypi       | six                 | 1.12.0               | #4
        | pypi       | python-dateutil     | 2.8.0                | #5
        | pypi       | s3transfer          | 0.2.1                | #6
        | pypi       | pyyaml              | 5.1.2                | #7
        | pypi       | docutils            | 0.15.2               | #8
        | pypi       | pyasn1              | 0.4.6                | #9
        | pypi       | requests            | 2.22.0               | #10
        | pypi       | setuptools          | 41.0.1               | #11
        | pypi       | jmespath            | 0.9.4                | #12
        | pypi       | certifi             | 2019.6.16            | #13
        | pypi       | awscli              | 1.16.212             | #14
        | pypi       | rsa                 | 4.0                  | #15
        | pypi       | futures             | 3.3.0                | #16
        | pypi       | idna                | 2.8                  | #17
        | pypi       | colorama            | 0.4.1                | #18
        | pypi       | wheel               | 0.33.4               | #19
        | pypi       | chardet             | 3.0.4                | #20
    

   Scenario Outline: Check the component analysis V2 REST API endpoint for 20 most popular maven components
    Given System is running
    Given Three scale preview service is running
        
        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I wait 2 seconds
        When I start v2 component analyses <ecosystem>/<package>/<version> with user_key
        Then I should get 200 status code
            And I should receive a valid JSON response

        When I look at the component analysis duration
        Then I should see that the component analysis duration is less than 5 second
      
        Then I should get no result or recommendation with report

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