Feature: Check the implementation of test steps

  @selfcheck
  Scenario: Check the updated stack analysis response
    Given data directory exists
    When I mock API response by data/updated_stack_analysis_v2.json file
    Then I should get a valid request ID
     And I should receive JSON response containing the started_at key
     And I should receive JSON response containing the finished_at key
     And I should receive JSON response containing the request_id key
     And I should find that valid outliers are reported
     And I should get license_analysis field in stack report
     And I should find dependency named io.vertx:vertx-core with version 3.4.2 in the stack analysis
     And I should find dependency named io.vertx:vertx-web with version 3.4.2 in the stack analysis
     And I should find analyzed dependency named io.vertx:vertx-core with version 3.4.2 in the stack analysis
     And I should find analyzed dependency named io.vertx:vertx-web with version 3.4.2 in the stack analysis
     And I should find that alternate components replace user components
     And I should find the security node for all dependencies
     And I should find the security node for all alternate components
     And I should find that none analyzed package can be found in companion packages as well
     And I should find the following analyzed dependencies (io.vertx:vertx-core,io.vertx:vertx-web) in the stack analysis
     And I should find the value pom.xml under the path result/0/manifest_name in the JSON response
     And I should find the value 3 under the path result/0/user_stack_info/total_licenses in the JSON response
     And I should find the value 0 under the path result/0/user_stack_info/unknown_dependencies_count in the JSON response
     And I should find the value maven under the path result/0/user_stack_info/ecosystem in the JSON response

  @selfcheck
  Scenario: Check that the stack analysis response for the pom.xml that contains only one component
    Given data directory exists
    When I mock API response by data/mock_stack_analysis_v2_junit.json file
    Then I should find analyzed dependency named junit:junit with version 3.8.1 in the stack analysis
    Then I should find that none analyzed package can be found in companion packages as well
    Then I should receive JSON response with the correct timestamp in attribute started_at
    Then I should receive JSON response with the correct timestamp in attribute finished_at
    Then I should find the following licenses (Free Art, MPLv2.0) under the path result/0/user_stack_info/analyzed_dependencies/0/license_analysis/unknown_licenses
    Then I should find the following licenses (Free Art, MPLv2.0) under the path result/0/user_stack_info/analyzed_dependencies/0/licenses
    Then I should find the following licenses (Free Art, MPLv2.0) under the path result/0/user_stack_info/distinct_licenses

  @selfcheck
  Scenario: Check that the stack analysis response for the springboot.xml
    Given data directory exists
    When I mock API response by data/mock_stack_analysis_v2_springboot.json file
    Then I should receive JSON response with the correct timestamp in attribute started_at
    Then I should receive JSON response with the correct timestamp in attribute finished_at
    Then I should find that alternate components replace user components
    Then I should find that none analyzed package can be found in companion packages as well
    Then I should find analyzed dependency named org.springframework:spring-messaging with version 4.3.7.RELEASE in the stack analysis
    Then I should find analyzed dependency named org.springframework.boot:spring-boot-starter-web with version 1.5.2.RELEASE in the stack analysis
    Then I should find analyzed dependency named org.springframework:spring-websocket with version 4.3.7.RELEASE in the stack analysis
    Then I should find analyzed dependency named org.springframework.boot:spring-boot-starter with version 1.5.2.RELEASE in the stack analysis
    Then I should find the proper outlier record for the org.springframework:spring-messaging component
    Then I should find the proper outlier record for the org.springframework:spring-websocket component

  @selfcheck
  Scenario: Check that the stack analysis response for the vertx.xml
    Given data directory exists
    When I mock API response by data/mock_stack_analysis_v2_vertx.json file
    Then I should receive JSON response with the correct timestamp in attribute started_at
    Then I should receive JSON response with the correct timestamp in attribute finished_at
    Then I should find analyzed dependency named io.vertx:vertx-core with version 3.4.1 in the stack analysis
    Then I should find analyzed dependency named io.vertx:vertx-web-templ-freemarker with version 3.4.1 in the stack analysis
    Then I should find analyzed dependency named io.vertx:vertx-jdbc-client with version 3.4.1 in the stack analysis
    Then I should find analyzed dependency named io.vertx:vertx-web with version 3.4.1 in the stack analysis
    Then I should find analyzed dependency named io.vertx:vertx-web-templ-handlebars with version 3.4.1 in the stack analysis
    Then I should find analyzed dependency named io.vertx:vertx-rx-java with version 3.4.1 in the stack analysis
    Then I should find analyzed dependency named io.vertx:vertx-web-client with version 3.4.1 in the stack analysis

  @selfcheck
  Scenario: Check that the stack analysis response for the springboot.xml - CVEs
    Given data directory exists
    When I mock API response by data/mock_stack_analysis_v2_requirements.json file
    Then I should find the security node for all dependencies
    Then I should find the security node for all alternate components
    Then I should find the CVE-2010-3492 security issue for the dependency six
    Then I should find the CVE-2002-1119 security issue for the dependency six
    Then I should find the CVE-2006-1542 security issue for the dependency six
    Then I should find the CVE-2007-4559 security issue for the dependency six
    Then I should find the CVE-2008-1679 security issue for the dependency six
    Then I should find the CVE-2008-1721 security issue for the dependency six
    Then I should find the CVE-2008-1887 security issue for the dependency six
    Then I should find the CVE-2008-2315 security issue for the dependency six
    Then I should find the CVE-2008-3142 security issue for the dependency six
    Then I should find the CVE-2008-3143 security issue for the dependency six
    Then I should find the CVE-2008-5983 security issue for the dependency six
    Then I should find the CVE-2011-4940 security issue for the dependency six
    Then I should find the CVE-2012-0845 security issue for the dependency six
    Then I should find the CVE-2012-1150 security issue for the dependency six
    Then I should find the CVE-2013-7338 security issue for the dependency six
    Then I should find the CVE-2013-7440 security issue for the dependency six
    Then I should find the CVE-2014-7185 security issue for the dependency six
    Then I should find the CVE-2015-5652 security issue for the dependency six
    Then I should find the CVE-2016-0772 security issue for the dependency six
    Then I should find the CVE-2016-1494 security issue for the dependency six
    Then I should find the CVE-2016-5636 security issue for the dependency six
    Then I should find the CVE-2016-5699 security issue for the dependency six
    Then I should not find any security issue for the dependency clojure_py
    Then I should not find any security issue for the dependency setuptools
    Then I should not find any security issue for the dependency parsimonious

  @selfcheck
  Scenario: Check the package tests by using mocked data
    Given data directory exists
    When I mock S3 data by content of data/clojure_py_package/github_details.json file
    Then I should find the correct GitHub details metadata for package clojure_py from ecosystem pypi
     and I should find empty details about GitHub repository
    When I mock S3 data by content of data/clojure_py_package/keywords_tagging.json file
    Then I should find the correct keywords tagging metadata for package clojure_py from ecosystem pypi
     and I should find the weight for the word clojure in the package name
     and I should find the weight for the word py in the package name
     and I should find the weight for the word clojure in the repository description
     and I should find the weight for the word bytecode in the repository description
     and I should find the weight for the word python in the repository description
    When I mock S3 data by content of data/clojure_py_package/libraries_io.json file
    Then I should find the correct libraries io metadata for package clojure_py from ecosystem pypi
     and I should find that the latest package version 0.2.4 was published on Apr 10, 2012
     and I should find that the recent package version 0.1.0g was published on Mar 8, 2012
     and I should find that the recent package version 0.2.0 was published on Apr 10, 2012
     and I should find that the recent package version 0.2.1 was published on Apr 10, 2012
     and I should find that the recent package version 0.2.2 was published on Apr 10, 2012
     and I should find that the recent package version 0.2.3 was published on Apr 10, 2012
     and I should find 6 releases for this package
     and I should find 0 dependent repositories for this package
     and I should find 0 dependent projects for this package

  @selfcheck
  Scenario: Check the component tests by using mocked data
    Given data directory exists
    When I mock S3 data by content of data/clojure_py_core_data/0.2.4.json file
    Then I should find the correct component core data for package clojure_py version 0.2.4 from ecosystem pypi
     and I should find that the latest component version is 0.2.4
     and I should find the correct component toplevel metadata for package clojure_py version 0.2.4 ecosystem pypi with latest version 0.2.4
    When I mock S3 data by content of data/clojure_py_core_data/0.2.4/dependency_snapshot.json file
    Then I should find the correct dependency snapshot data for package clojure_py version 0.2.4 from ecosystem pypi
     and I should find 0 runtime details in dependency snapshot
     and I should find 0 dependencies in dependency snapshot summary
    When I mock S3 data by content of data/clojure_py_core_data/0.2.4/digests.json file
    Then I should find the correct digest data for package clojure_py version 0.2.4 from ecosystem pypi
     and I should find digest metadata path set to clojure_py-0.2.4.tar.gz
     and I should find digest metadata md5 set to db0025db3e80fae44f20efba1bab6e3c
     and I should find digest metadata sha1 set to 6703fc426ac60906c4c8c6e1bc6f8934ee097fc2
     and I should find digest metadata sha256 set to 688943c6e9fce571b81c5d0f4c09dd5d7ef4444e49d93b2e9a9e1bd4fa773abd
     and I should find digest metadata ssdeep set to 1536:nu4FNqGJWw7fFh2qI6c3o2TXYgpLCnnBlh3ZlsspxBJ9BZbbOzb1MjRY8Hh0YEyw:uaUw7fP2HfLIgYqijJ9Xeb1MjLhIXIm
    When I mock S3 data by content of data/clojure_py_core_data/0.2.4/keywords_tagging.json file
    Then I should find the correct keywords tagging data for package clojure_py version 0.2.4 from ecosystem pypi
     and I should find the weight for the word clojure in the description
     and I should find the weight for the word implementation in the description
     and I should find the weight for the word python in the description
     and I should find the weight for the word top in the description
    When I mock S3 data by content of data/clojure_py_core_data/0.2.4/metadata.json file
    Then I should find the correct metadata for package clojure_py version 0.2.4 from ecosystem pypi
     and I should find that author of this project is Timothy Baldridge
     and I should find that the project use GIT as a version control system
     and I should find that the repository can be found at https://github.com/halgari/clojure-py
     and I should find that the package description is Clojure implemented on top of Python
     and I should find that the project homepage can be found at https://github.com/halgari/clojure-py
     and I should find that the package name is clojure-py and version is 0.2.4
    When I mock S3 data by content of data/clojure_py_core_data/0.2.4/security_issues.json file
    Then I should find the correct security issues data for package clojure_py version 0.2.4 from ecosystem pypi
    When I mock S3 data by content of data/clojure_py_core_data/0.2.4/source_licenses.json file
    Then I should find the correct source licenses data for package clojure_py version 0.2.4 from ecosystem pypi
     and I should find that the package uses EPL 1.0 license
     and I should find that the package uses LGPL 2.1 or later license
     and I should find that the package uses MIT License license

  @selfcheck
  Scenario Outline: Check the we have all the required mock files
    Given data directory exists
    When I mock S3 data by content of data/<filename> file
    Then I should receive nonempty JSON response from S3

    Examples:
    | filename |
    | io.vertx_vertx_core_package_data/github_details.json |
    | io.vertx_vertx_core_package_data/git_stats.json |
    | io.vertx_vertx_core_package_data/io.vertx_vertx-core.json |
    | io.vertx_vertx_core_package_data/keywords_tagging.json |
    | io.vertx_vertx_core_package_data/libraries_io.json |
    | io.vertx_vertx_core_component_data/3.4.0.json |
    | io.vertx_vertx_core_component_data/3.5.1.json |
    | io.vertx_vertx_core_component_data/3.4.0/binary_data.json |
    | io.vertx_vertx_core_component_data/3.4.0/code_metrics.json |
    | io.vertx_vertx_core_component_data/3.4.0/crypto_algorithms.json |
    | io.vertx_vertx_core_component_data/3.4.0/dependency_snapshot.json |
    | io.vertx_vertx_core_component_data/3.4.0/digests.json |
    | io.vertx_vertx_core_component_data/3.4.0/languages.json |
    | io.vertx_vertx_core_component_data/3.4.0/metadata.json |
    | io.vertx_vertx_core_component_data/3.4.0/source_licenses.json |
    | io.vertx_vertx_core_component_data/3.5.1/dependency_snapshot.json |
    | io.vertx_vertx_core_component_data/3.5.1/digests.json |
    | io.vertx_vertx_core_component_data/3.5.1/keywords_tagging.json |
    | io.vertx_vertx_core_component_data/3.5.1/metadata.json |
    | io.vertx_vertx_core_component_data/3.5.1/security_issues.json |
    | io.vertx_vertx_core_component_data/3.5.1/source_licenses.json |


  @selfcheck
  Scenario: Check the package schema tests by using mocked data - toplevel metadata schema for package
    Given data directory exists
    When I mock S3 data by content of data/io.vertx_vertx_core_package_data/io.vertx_vertx-core.json file
    Then I should receive nonempty JSON response from S3
     And I should find that the metadata conformns to package_toplevel schema


  @selfcheck
  Scenario: Check the package schema tests by using mocked data - GitHub details schema for package
    Given data directory exists
    When I mock S3 data by content of data/io.vertx_vertx_core_package_data/github_details.json file
    Then I should receive nonempty JSON response from S3
     And I should find that the metadata conformns to package_github_details schema


  @selfcheck
  Scenario: Check the package schema tests by using mocked data - Git stats schema for package
    Given data directory exists
    When I mock S3 data by content of data/io.vertx_vertx_core_package_data/git_stats.json file
    Then I should receive nonempty JSON response from S3
     And I should find that the metadata conformns to package_git_stats schema


  @selfcheck
  Scenario: Check the package schema tests by using mocked data - libraries.io schema for package
    Given data directory exists
    When I mock S3 data by content of data/io.vertx_vertx_core_package_data/libraries_io.json file
    Then I should receive nonempty JSON response from S3
     And I should find that the metadata conformns to package_libraries_is schema


  @selfcheck
  Scenario: Check the package schema tests by using mocked data - keywords tagging schema for package
    Given data directory exists
    When I mock S3 data by content of data/io.vertx_vertx_core_package_data/keywords_tagging.json file
    Then I should receive nonempty JSON response from S3
     And I should find that the metadata conformns to package_keywords_tagging schema


  @selfcheck
  Scenario: Check the component schema tests by using mocked data - toplevel metadata schema for component
    Given data directory exists
    When I mock S3 data by content of data/io.vertx_vertx_core_component_data/3.4.0.json file
    Then I should receive nonempty JSON response from S3
     And I should find that the metadata conformns to component_toplevel schema


  @selfcheck
  Scenario: Check the component schema tests by using mocked data - toplevel metadata schema for component
    Given data directory exists
    When I mock S3 data by content of data/io.vertx_vertx_core_component_data/3.5.1.json file
    Then I should receive nonempty JSON response from S3
     And I should find that the metadata conformns to component_toplevel schema


  @selfcheck
  Scenario: Check the component schema tests by using mocked data - binary_data schema for component
    Given data directory exists
    When I mock S3 data by content of data/io.vertx_vertx_core_component_data/3.4.0/binary_data.json file
    Then I should receive nonempty JSON response from S3


  @selfcheck
  Scenario: Check the component schema tests by using mocked data - dependency snapshot metadata schema for component
    Given data directory exists
    When I mock S3 data by content of data/io.vertx_vertx_core_component_data/3.4.0/dependency_snapshot.json file
    Then I should receive nonempty JSON response from S3
     And I should find that the metadata conformns to component_dependency_snapshot schema


  @selfcheck
  Scenario: Check the component schema tests by using mocked data - dependency snapshot metadata schema for component
    Given data directory exists
    When I mock S3 data by content of data/io.vertx_vertx_core_component_data/3.5.1/dependency_snapshot.json file
    Then I should receive nonempty JSON response from S3
     And I should find that the metadata conformns to component_dependency_snapshot schema


  @selfcheck
  Scenario: Check the component schema tests by using mocked data - digests schema for component
    Given data directory exists
    When I mock S3 data by content of data/io.vertx_vertx_core_component_data/3.4.0/digests.json file
    Then I should receive nonempty JSON response from S3
     And I should find that the metadata conformns to component_digests schema


  @selfcheck
  Scenario: Check the component schema tests by using mocked data - digests schema for component
    Given data directory exists
    When I mock S3 data by content of data/io.vertx_vertx_core_component_data/3.5.1/digests.json file
    Then I should receive nonempty JSON response from S3
     And I should find that the metadata conformns to component_digests schema


  @selfcheck
  Scenario: Check the component schema tests by using mocked data - keywords tagging schema for component
    Given data directory exists
    When I mock S3 data by content of data/io.vertx_vertx_core_component_data/3.5.1/keywords_tagging.json file
    Then I should receive nonempty JSON response from S3
     And I should find that the metadata conformns to component_keywords_tagging schema


  @selfcheck
  Scenario: Check the component schema tests by using mocked data - code metrics schema for component
    Given data directory exists
    When I mock S3 data by content of data/io.vertx_vertx_core_component_data/3.4.0/code_metrics.json file
    Then I should receive nonempty JSON response from S3
     And I should find that the metadata conformns to component_code_metrics schema


  @selfcheck
  Scenario: Check the component schema tests by using mocked data - crypto algorithms schema for component
    Given data directory exists
    When I mock S3 data by content of data/io.vertx_vertx_core_component_data/3.4.0/crypto_algorithms.json file
    Then I should receive nonempty JSON response from S3


  @selfcheck
  Scenario: Check the component schema tests by using mocked data - languages schema for component
    Given data directory exists
    When I mock S3 data by content of data/io.vertx_vertx_core_component_data/3.4.0/languages.json file
    Then I should receive nonempty JSON response from S3


  @selfcheck
  Scenario: Check the component schema tests by using mocked data - metadata schema for component
    Given data directory exists
    When I mock S3 data by content of data/io.vertx_vertx_core_component_data/3.4.0/metadata.json file
    Then I should receive nonempty JSON response from S3
     And I should find that the metadata conformns to component_metadata schema


  @selfcheck
  Scenario: Check the component schema tests by using mocked data - metadata schema for component
    Given data directory exists
    When I mock S3 data by content of data/io.vertx_vertx_core_component_data/3.5.1/metadata.json file
    Then I should receive nonempty JSON response from S3
     And I should find that the metadata conformns to component_metadata schema


  @selfcheck
  Scenario: Check the component schema tests by using mocked data - security issues metadata schema for component
    Given data directory exists
    When I mock S3 data by content of data/io.vertx_vertx_core_component_data/3.5.1/security_issues.json file
    Then I should receive nonempty JSON response from S3
     And I should find that the metadata conformns to component_security_issues schema


  @selfcheck
  Scenario: Check the component schema tests by using mocked data - source licenses schema for component
    Given data directory exists
    When I mock S3 data by content of data/io.vertx_vertx_core_component_data/3.4.0/source_licenses.json file
    Then I should receive nonempty JSON response from S3
     And I should find that the metadata conformns to component_source_licenses schema


  @selfcheck
  Scenario: Check the component schema tests by using mocked data - source licenses schema for component
    Given data directory exists
    When I mock S3 data by content of data/io.vertx_vertx_core_component_data/3.5.1/source_licenses.json file
    Then I should receive nonempty JSON response from S3
     And I should find that the metadata conformns to component_source_licenses schema

