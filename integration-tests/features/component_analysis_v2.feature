Feature: Component analysis v2 API

  Scenario Outline: Check the component analysis V2 REST API endpoint for components with recommendation
    Given System is running
    Given Three scale preview service is running

      When I acquire the use_key for 3scale
      Then I should get the proper user_key
    
      When I start v2 component analyses <ecosystem>/<package>/<version> with user_key
      Then I should get 200 status code
        And I should receive a valid JSON response
      Then I should find essential fields present in the result
      Then I should find recommended version <recommended-version> in the component analysis
      Then I should find one or more vulnerabilities in result with valid attributes
      And I should find CVE report <cve> with score <score> in the component v2 analysis
      And I should check for snyk url cvss3 severity and title in result
      And I should find <cve> with <severity> severity and <title> title in result
      Then I should see no registered user fields are exposed in result


     Examples: EPV
     | ecosystem  | package                           | version   | recommended-version | cve                                  | score  | severity | title                                        |
     | npm        | ejs                               | 1.0.0     | 3.1.3               | SNYK-JS-EJS-10218                    | 8.1    | high     | Arbitrary Code Execution                     |
     | npm        | marked                            | 0.3.5     | 1.1.0               | SNYK-JS-MARKED-10377                 | 7.5    | high     | Cross-site Scripting (XSS)                   |
     | npm        | st                                | 0.2.4     | 2.0.0               | SNYK-JS-ST-10820                     | 4.3    | medium   | Open Redirect                                |
     | npm        | npmconf                           | 0.0.24    | 2.1.3               | SNYK-JS-NPMCONF-12143                | 7.4    | high     | Uninitialized Memory Exposure                |
     | npm        | moment                            | 2.15.1    | 2.27.0              | SNYK-JS-MOMENT-10841                 | 3.7    | low      | Regular Expression Denial of Service (ReDoS) |
     | npm        | mongoose                          | 4.2.4     | 5.9.19              | SNYK-JS-MONGOOSE-10081               | 5.1    | medium   | Remote Memory Exposure                       |
     | maven      | io.vertx:vertx-core               | 3.5.3     | 4.0.0-milestone5    | SNYK-JAVA-IOVERTX-72443              | 6.5    | medium   | Denial of Service (DoS)                      |
     | maven      | org.webjars.bower:jquery          | 3.4.1     | 3.5.1               | SNYK-JAVA-ORGWEBJARSBOWER-567881     | 6.5    | medium   | Cross-site Scripting (XSS)                   |
     | maven      | org.webjars:bootstrap-select      | 1.7.3     | 1.13.15             | SNYK-JAVA-ORGWEBJARS-479517          | 7.0    | high     | Cross-site Scripting (XSS)                   |
     | maven      | org.apache.camel:camel-rabbitmq   | 2.22.0    | 3.3.0               | SNYK-JAVA-ORGAPACHECAMEL-569123      | 6.5    | medium   | Insecure Default                             |
     | maven      | org.apache.tomcat:tomcat-catalina | 7.0.0     | 10.0.0-M6           | SNYK-JAVA-ORGAPACHETOMCAT-32110      | 6.5    | medium   | Directory Traversal                          |
     | maven      | org.webjars.npm:openpgp           | 1.4.1     | 4.7.1               | SNYK-JAVA-ORGWEBJARSNPM-480073       | 7.0    | high     | Invalid Curve Attack                         |
     | pypi       | flask                             | 0.12      | 2.0.1               | SNYK-PYTHON-FLASK-42185              | 7.5    | high     | Improper Input Validation                    |
     | pypi       | fastapi                           | 0.36.0    | 0.58.0              | SNYK-PYTHON-FASTAPI-569038           | 5.3    | medium   | information leakage                          |
     | pypi       | sceptre                           | 2.2.1     | 2.3.0               | SNYK-PYTHON-SCEPTRE-569070           | 6.5    | medium   | Cross-site Scripting (XSS)                   |
     | pypi       | syft                              | 0.2.0a1   | 0.2.6               | SNYK-PYTHON-SYFT-568873              | 5.9    | medium   | Arbitrary Code Injection                     |
     | pypi       | numpy                             | 1.15.4    | 1.20.3              | SNYK-PYTHON-NUMPY-73513              | 9.8    | critical | Arbitrary Code Execution                     |


  Scenario Outline: Check the component analysis V2 REST API endpoint for components without recommendations
      Given System is running
      Given Three scale preview service is running

      When I acquire the use_key for 3scale
      Then I should get the proper user_key

      When I start v2 component analyses <ecosystem>/<package>/<version> with user_key
      Then I should get 200 status code
        And I should receive a valid JSON response
      Then I should find no recommendation


      Examples: EPV
     | ecosystem  | package  | version |
     | npm | sequence | 3.0.0 |
     | npm | aargh | 1.1.0 |
     | npm | arrays | 0.1.1 |
     | npm | jquery | 3.5.0 |
     | npm | mocha | 6.1.4 |
     | npm | underscore | 1.9.1 |
     | npm | babel-core | 7.0.0-alpha.1 |
     | npm | react | 16.8.6 |
     | npm | wisp | 0.11.1 |
     | maven | io.vertx:vertx-core | 3.7.0 |
     | maven | org.webjars.npm:openpgp | 4.7.1 |
     | maven | org.apache.tomcat:tomcat-catalina | 10.0.0-M5 |
     | maven | org.apache.camel:camel-rabbitmq | 3.3.0 |
     | maven | com.android.tools.build:gradle | 2.3.0 |
     | maven | org.json:json | 20180813 |
     | maven | org.python:jython | 2.7.1b3 |
     | maven | org.clojure:clojure | 1.10.1-beta2 |
     | pypi | clojure_py | 0.2.4 |
     | pypi | six | 1.10.0 |
     | pypi | ansicolors | 1.1.8 |
     | pypi | flask | 1.0.2 |
     | pypi | numpy | 1.16.3 |
     | pypi | scipy | 1.2.1 |
     | pypi | pygame | 1.9.6rc1 |
     | pypi | pyglet | 1.4.0a1 |
     | pypi | requests | 2.21.0 |
     | pypi | dash | 1.0.0a1 |
     | pypi | pudb | 2017.1.4 |
     | pypi | pytest | 3.2.2 |


     Scenario: Check the component analysis V2 REST API endpoint for unknown ecosystem
        Given System is running
          Given Three scale preview service is running

          When I acquire the use_key for 3scale
          Then I should get the proper user_key


          When I start v2 component analyses really_unknown_ecosystem/foobar/1.0.0 with user_key
          Then I should get 400 status code
          And I should receive a valid JSON response

  
  Scenario: Check the component analysis REST V2 API endpoint for unknown component in NPM ecosystem
    Given System is running
      Given Three scale preview service is running
      
      When I acquire the use_key for 3scale
      Then I should get the proper user_key
      

     When I start v2 component analyses npm/really_unknown_component/1.0.0 with user_key
      Then I should get 404 status code
      And I should receive a valid JSON response

  
  Scenario: Check the component analysis V2 REST API endpoint for unknown component in PyPi ecosystem
    Given System is running
     Given Three scale preview service is running

      When I acquire the use_key for 3scale
      Then I should get the proper user_key


     When I start v2 component analyses pypi/really_unknown_component/1.0.0 with user_key
     Then I should get 404 status code
      And I should receive a valid JSON response


  Scenario: Check one npm package for private vulnerabilities
    Given System is running
    Given Three scale preview service is running

      When I acquire the use_key for 3scale
      Then I should get the proper user_key


      When I start v2 component analyses npm/lodash/4.17.4 with user_key
      Then I should get 200 status code
        And I should receive a valid JSON response
      Then I should find one or more vulnerabilities in result with valid attributes
        And I should check for snyk url cvss3 severity and title in result
      Then I should find a private vulnerability in v2 component analysis

  Scenario: Check one pypi package for private vulnerabilities
    Given System is running
    Given Three scale preview service is running

      When I acquire the use_key for 3scale
      Then I should get the proper user_key


      When I start v2 component analyses pypi/markdown2/2.2.0 with user_key
      Then I should get 200 status code
        And I should receive a valid JSON response
      Then I should find one or more vulnerabilities in result with valid attributes
        And I should check for snyk url cvss3 severity and title in result
      Then I should find a private vulnerability in v2 component analysis


  Scenario: Check one maven package for private vulnerabilities
    Given System is running
    Given Three scale preview service is running

      When I acquire the use_key for 3scale
      Then I should get the proper user_key


      When I start v2 component analyses maven/org.webjars.npm:electron/0.4.1 with user_key
      Then I should get 200 status code
        And I should receive a valid JSON response
      Then I should find one or more vulnerabilities in result with valid attributes
        And I should check for snyk url cvss3 severity and title in result
      Then I should find a private vulnerability in v2 component analysis


   @skip
   Scenario: Check that component analysis v2 returns limits exceeded
    Given System is running
    Given Three scale preview service is running

      When I acquire the use_key for 3scale
      Then I should get the proper user_key


      When I start v2 component analyses npm/sequence/2.2.0 120 times in a minute with user_key
      Then I should get 429 status code
        And I should get Usage limit exceeded text response
       When I wait 60 seconds


   Scenario Outline: Check if no recommended version comes when package has private vulnerabilities
    Given System is running
    Given Three scale preview service is running

      When I acquire the use_key for 3scale
      Then I should get the proper user_key

      
      When I start v2 component analyses <ecosystem>/<package>/<version> with user_key
      Then I should get 200 status code
        And I should receive a valid JSON response


      Then I should find a private vulnerability in v2 component analysis
      Then I should not have any recommended version

      Examples: EPV
     | ecosystem  | package                         | version |
     | pypi       | zulip                           | 0.6.4   |
     | maven      | org.webjars.npm:markdown-to-jsx | 6.6.6   |
     | npm        | markdown                        | 0.5.0  |
