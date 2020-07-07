Feature: Smoke tests for the component analysis REST API


  Scenario Outline: Check the component analysis REST API endpoint for selected components with and without recommendations
    Given System is running
    Given Three scale preview service is running
    
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
     | ecosystem  | package             | version        |
     | npm        | sequence            | 3.0.0          |
     | npm        | aargh               | 1.1.0          |
     | npm        | arrays              | 0.1.1          |
     | npm        | jquery              | 3.4.0          |
     | npm        | mocha               | 6.1.4          |
     | npm        | underscore          | 1.9.1          |
     | npm        | lodash              | 4.17.11        |
     | npm        | babel-core          | 6.26.3         |
     | npm        | babel-core          | 6.26.2         |
     | npm        | babel-core          | 7.0.0-bridge.0 |
     | npm        | babel-core          | 7.0.0-beta.3   |
     | npm        | babel-core          | 7.0.0-beta.2   |
     | npm        | babel-core          | 7.0.0-beta.1   |
     | npm        | babel-core          | 7.0.0-beta.0   |
     | npm        | babel-core          | 7.0.0-alpha.20 |
     | npm        | babel-core          | 6.26.0         |
     | npm        | babel-core          | 7.0.0-alpha.19 |
     | npm        | babel-core          | 7.0.0-alpha.18 |
     | npm        | babel-core          | 7.0.0-alpha.17 |
     | npm        | babel-core          | 7.0.0-alpha.16 |
     | npm        | babel-core          | 7.0.0-alpha.15 |
     | npm        | babel-core          | 7.0.0-alpha.14 |
     | npm        | babel-core          | 6.25.0         |
     | npm        | babel-core          | 7.0.0-alpha.12 |
     | npm        | babel-core          | 7.0.0-alpha.11 |
     | npm        | babel-core          | 7.0.0-alpha.10 |
     | npm        | babel-core          | 7.0.0-alpha.9  |
     | npm        | babel-core          | 7.0.0-alpha.8  |
     | npm        | babel-core          | 6.24.1         |
     | npm        | babel-core          | 7.0.0-alpha.7  |
     | npm        | babel-core          | 7.0.0-alpha.6  |
     | npm        | babel-core          | 7.0.0-alpha.3  |
     | npm        | babel-core          | 6.24.0         |
     | npm        | babel-core          | 7.0.0-alpha.2  |
     | npm        | babel-core          | 7.0.0-alpha.1  |
     | npm        | react               | 16.8.6         |
     | npm        | wisp                | 0.11.1         |
     | maven      | io.vertx:vertx-core | 3.7.0          |
     | maven      | io.vertx:vertx-core | 3.6.3          |
     | maven      | io.vertx:vertx-core | 3.6.2          |
     | maven      | io.vertx:vertx-core | 3.6.1          |
     | maven      | io.vertx:vertx-core | 3.6.0          |
     | maven      | org.json:json       | 20180813       |
     | maven      | org.json:json       | 20180130       |
     | maven      | org.json:json       | 20171018       |
     | maven      | org.json:json       | 20170516       |
     | maven      | org.python:jython   | 2.7.1b3        |
     | maven      | org.python:jython   | 2.7.1b2        |
     | maven      | org.clojure:clojure | 1.10.1-beta2   |
     | maven      | org.clojure:clojure | 1.10.1-beta1   |
     | maven      | org.clojure:clojure | 1.10.0         |
     | pypi       | clojure_py          | 0.2.4          |
     | pypi       | six                 | 1.10.0         |
     | pypi       | ansicolors          | 1.1.8          |
     | pypi       | flask               | 1.0.2          |
     | pypi       | flask               | 1.0.1          |
     | pypi       | flask               | 1.0            |
     | pypi       | numpy               | 1.16.3         |
     | pypi       | scipy               | 1.2.1          |
     | pypi       | scipy               | 1.2.0          |
     | pypi       | pygame              | 1.9.6rc1       |
     | pypi       | pygame              | 1.9.5          |
     | pypi       | pyglet              | 1.4.0a1        |
     | pypi       | pyglet              | 1.3.2          |
     | pypi       | requests            | 2.21.0         |
     | pypi       | requests            | 2.20.1         |
     | pypi       | requests            | 2.20.0         |
     | pypi       | dash                | 1.0.0a1        |
     | pypi       | dash                | 0.43.0rc3      |
     | pypi       | dash                | 0.43.0rc2      |
     | pypi       | dash                | 0.43.0rc1      |
     | pypi       | pudb                | 2018.1         |
     | pypi       | pudb                | 2017.1.4       |
     | pypi       | pudb                | 2017.1.3       |
     | pypi       | pudb                | 2017.1.2       |
     | pypi       | pudb                | 2017.1.1       |
     | pypi       | pytest              | 3.2.1          |
     | pypi       | pytest              | 3.2.2          |
     | npm        | lodash              | 4.17.2         |
     | npm        | lodash              | 4.17.3         |
     | npm        | lodash              | 4.17.4         |
     | npm        | lodash              | 4.17.5         |
     | npm        | lodash              | 4.17.9         |
     | npm        | lodash              | 4.17.10        |
     | maven      | io.vertx:vertx-core | 3.5.3          |
     | maven      | io.vertx:vertx-core | 3.5.3.CR1      |
     | maven      | io.vertx:vertx-core | 3.5.2          |
     | maven      | io.vertx:vertx-core | 3.5.2.CR3      |
     | maven      | io.vertx:vertx-core | 3.5.2.CR2      |
     | maven      | io.vertx:vertx-core | 3.5.2.CR1      |
     | pypi       | flask               | 0.12           |
     | pypi       | flask               | 0.12.1         |
     | pypi       | flask               | 0.12.2         |
     | pypi       | numpy               | 1.16.0         |
     | pypi       | numpy               | 1.15.4         |
     | pypi       | numpy               | 1.15.3         |
     | pypi       | numpy               | 1.15.2         |
     | pypi       | numpy               | 1.15.1         |
     | pypi       | requests            | 2.19.1         |
     | pypi       | requests            | 2.19.0         |
     | pypi       | requests            | 2.18.4         |
     | pypi       | requests            | 2.18.3         |
     | pypi       | requests            | 2.18.2         |
     | pypi       | requests            | 2.17.3         |
