Feature: Unknown licenses


  Scenario Outline: Check the component analysis REST API endpoint for components without recommendations
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token

     When I read <ecosystem>/<package>/<version> component analysis with authorization token
     Then I should get 200 status code
      And I should receive a valid JSON response
      And I should receive JSON response containing the result key
      And I should find one analyzed package in the component analysis
      And I should find the package <package> from <ecosystem> ecosystem in the component analysis
      And I should find the component <package> version <version> from <ecosystem> ecosystem in the component analysis
      And I should find no recommendations in the component analysis

     Examples: EPV
     | ecosystem  | package  | version |
     | npm | sequence | 3.0.0 |
     | npm | aargh | 1.1.0 |
     | npm | arrays | 0.1.1 |
     | npm | jquery | 3.4.0 |
     | npm | mocha | 6.1.4 |
     | npm | underscore | 1.9.1 |
     | npm | lodash | 4.17.11 |
     | npm | babel-core | 6.26.3 |
     | npm | babel-core | 6.26.2 |
     | npm | babel-core | 7.0.0-bridge.0 |
     | npm | babel-core | 7.0.0-beta.3 |
     | npm | babel-core | 7.0.0-beta.2 |
     | npm | babel-core | 7.0.0-beta.1 |
     | npm | babel-core | 7.0.0-beta.0 |
     | npm | babel-core | 7.0.0-alpha.20 |
     | npm | babel-core | 6.26.0 |
     | npm | babel-core | 7.0.0-alpha.19 |
     | npm | babel-core | 7.0.0-alpha.18 |
     | npm | babel-core | 7.0.0-alpha.17 |
     | npm | babel-core | 7.0.0-alpha.16 |
     | npm | babel-core | 7.0.0-alpha.15 |
     | npm | babel-core | 7.0.0-alpha.14 |
     | npm | babel-core | 6.25.0 |
     | npm | babel-core | 7.0.0-alpha.12 |
     | npm | babel-core | 7.0.0-alpha.11 |
     | npm | babel-core | 7.0.0-alpha.10 |
     | npm | babel-core | 7.0.0-alpha.9 |
     | npm | babel-core | 7.0.0-alpha.8 |
     | npm | babel-core | 6.24.1 |
     | npm | babel-core | 7.0.0-alpha.7 |
     | npm | babel-core | 7.0.0-alpha.6 |
     | npm | babel-core | 7.0.0-alpha.3 |
     | npm | babel-core | 6.24.0 |
     | npm | babel-core | 7.0.0-alpha.2 |
     | npm | babel-core | 7.0.0-alpha.1 |
     | npm | react | 16.8.6 |
     | npm | wisp | 0.11.1 |
     | maven | io.vertx:vertx-core | 3.7.0 |
     | maven | io.vertx:vertx-core | 3.6.3 |
     | maven | io.vertx:vertx-core | 3.6.2 |
     | maven | io.vertx:vertx-core | 3.6.1 |
     | maven | io.vertx:vertx-core | 3.6.0 |
     | maven | org.json:json | 20180813 |
     | maven | org.json:json | 20180130 |
     | maven | org.json:json | 20171018 |
     | maven | org.json:json | 20170516 |
     | maven | org.python:jython | 2.7.1b3 |
     | maven | org.python:jython | 2.7.1b2 |
     | maven | org.clojure:clojure | 1.10.1-beta2 |
     | maven | org.clojure:clojure | 1.10.1-beta1 |
     | maven | org.clojure:clojure | 1.10.0 |
     | pypi | clojure_py | 0.2.4 |
     | pypi | six | 1.10.0 |
     | pypi | ansicolors | 1.1.8 |
     | pypi | flask | 1.0.2 |
     | pypi | flask | 1.0.1 |
     | pypi | flask | 1.0 |
     | pypi | numpy | 1.16.3 |
     | pypi | scipy | 1.2.1 |
     | pypi | scipy | 1.2.0 |
     | pypi | pygame | 1.9.6rc1 |
     | pypi | pygame | 1.9.5 |
     | pypi | pyglet | 1.4.0a1 |
     | pypi | pyglet | 1.3.2 |
     | pypi | requests | 2.21.0 |
     | pypi | requests | 2.20.1 |
     | pypi | requests | 2.20.0 |
     | pypi | dash | 1.0.0a1 |
     | pypi | dash | 0.43.0rc3 |
     | pypi | dash | 0.43.0rc2 |
     | pypi | dash | 0.43.0rc1 |
     | pypi | pudb | 2018.1 |
     | pypi | pudb | 2017.1.4 |
     | pypi | pudb | 2017.1.3 |
     | pypi | pudb | 2017.1.2 |
     | pypi | pudb | 2017.1.1 |
     | pypi | pytest | 3.2.1 |
     | pypi | pytest | 3.2.2 |


  Scenario: Check the component analysis REST API endpoint for unknown ecosystem
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token

     When I start analysis for component really_unknown_ecosystem/foobar/1.0.0 with authorization token
     Then I should get 400 status code
      And I should receive a valid JSON response


  Scenario: Check the component analysis REST API endpoint for unknown component in NPM ecosystem
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token

     When I start analysis for component npm/really_unknown_component/1.0.0 with authorization token
     Then I should get 202 status code
      And I should receive a valid JSON response


  Scenario: Check the component analysis REST API endpoint for unknown component in PyPi ecosystem
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token

     When I start analysis for component pypi/really_unknown_component/1.0.0 with authorization token
     Then I should get 202 status code
      And I should receive a valid JSON response


  # There's an error on the stage, so let's let this test commented for a while
  #Scenario: Check the component analysis REST API endpoint for unknown component in Maven ecosystem
  #  Given System is running
  #   When I acquire the authorization token
  #   Then I should get the proper authorization token#

  #   When I start analysis for component maven/really_unknown_component/1.0.0 with authorization token
  #   Then I should get 202 status code
  #    And I should receive a valid JSON response


  Scenario Outline: Check the component analysis REST API endpoint for components with recommendation and one CVE
    Given System is running
     When I acquire the authorization token
     Then I should get the proper authorization token

     When I read <ecosystem>/<package>/<version> component analysis with authorization token
     Then I should get 200 status code
      And I should receive a valid JSON response
      And I should receive JSON response containing the result key
      And I should find the package <package> from <ecosystem> ecosystem in the component analysis
      And I should find the component <package> version <version> from <ecosystem> ecosystem in the component analysis
      And I should find recommendation to change to version <recommended-version> in the component analysis
      And I should find CVE report <cve> with score <score> in the component analysis

     Examples: EPV
     | ecosystem  | package             | version   | recommended-version | cve              | score |
     | npm        | lodash              | 4.17.2    | 4.17.15             | CVE-2018-16487   | 7.5   |
     | npm        | lodash              | 4.17.3    | 4.17.15             | CVE-2018-16487   | 7.5   |
     | npm        | lodash              | 4.17.4    | 4.17.15             | CVE-2018-16487   | 7.5   |
     | npm        | lodash              | 4.17.5    | 4.17.15             | CVE-2018-16487   | 7.5   |
     | npm        | lodash              | 4.17.9    | 4.17.15             | CVE-2018-16487   | 7.5   |
     | npm        | lodash              | 4.17.10   | 4.17.15             | CVE-2018-16487   | 7.5   |
     | maven      | io.vertx:vertx-core | 3.5.3     | 3.7.1               | CVE-2018-12541   | 5.0   |
     | maven      | io.vertx:vertx-core | 3.5.3.CR1 | 3.7.1               | CVE-2018-12541   | 5.0   |
     | maven      | io.vertx:vertx-core | 3.5.2     | 3.7.1               | CVE-2018-12541   | 5.0   |
     | maven      | io.vertx:vertx-core | 3.5.2.CR3 | 3.7.1               | CVE-2018-12541   | 5.0   |
     | maven      | io.vertx:vertx-core | 3.5.2.CR2 | 3.7.1               | CVE-2018-12541   | 5.0   |
     | maven      | io.vertx:vertx-core | 3.5.2.CR1 | 3.7.1               | CVE-2018-12541   | 5.0   |
     | pypi       | flask               | 0.12      | 1.0.3               | CVE-2018-1000656 | 5.0   |
     | pypi       | flask               | 0.12.1    | 1.0.3               | CVE-2018-1000656 | 5.0   |
     | pypi       | flask               | 0.12.2    | 1.0.3               | CVE-2018-1000656 | 5.0   |
     | pypi       | numpy               | 1.16.0    | 1.16.4              | CVE-2019-6446    | 7.5   |
     | pypi       | numpy               | 1.15.4    | 1.16.4              | CVE-2019-6446    | 7.5   |
     | pypi       | numpy               | 1.15.3    | 1.16.4              | CVE-2019-6446    | 7.5   |
     | pypi       | numpy               | 1.15.2    | 1.16.4              | CVE-2019-6446    | 7.5   |
     | pypi       | numpy               | 1.15.1    | 1.16.4              | CVE-2019-6446    | 7.5   |
     | pypi       | requests            | 2.19.1    | 2.22.0              | CVE-2018-18074   | 5.0   |
     | pypi       | requests            | 2.19.0    | 2.22.0              | CVE-2018-18074   | 5.0   |
     | pypi       | requests            | 2.18.4    | 2.22.0              | CVE-2018-18074   | 5.0   |
     | pypi       | requests            | 2.18.3    | 2.22.0              | CVE-2018-18074   | 5.0   |
     | pypi       | requests            | 2.18.2    | 2.22.0              | CVE-2018-18074   | 5.0   |
     | pypi       | requests            | 2.17.3    | 2.22.0              | CVE-2018-18074   | 5.0   |
