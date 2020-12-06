Feature: Stack analysis v2 API Golang Ecosystem Tests


    @sav2
    Scenario: Check the golang API without user key
        Given System is running
        When I send pypi package request with manifest golist.json to stack analysis v2 without valid user key
        Then I should get 403 status code

    
    @sav2
    Scenario: Check the golang API with invalid user key
        Given System is running
        Given Three scale preview service is running
        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I send pypi package request with manifest valid_golist.json to stack analysis v2 with invalid user key
        Then I should get 403 status code
    
    @sav2
    Scenario: Check the golang API with valid user key
        Given System is running
        Given Three scale preview service is running
        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I wait 10 seconds
        When I send pypi package request with manifest valid_golist.json to stack analysis v2 with valid user key
        Then I should get 200 status code
        And I should receive JSON response containing the status key
        And I should receive JSON response containing the id key
        And I should receive JSON response containing the submitted_at key
        And I should receive JSON response with the status key set to success
        And I should receive JSON response with the correct id
        And I should receive JSON response with the correct timestamp in attribute submitted_at

    @sav2
    Scenario Outline: Check the stack analysis v2 for invalid manifest data
        Given System is running
        Given Three scale preview service is running
        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I send go package request with manifest golist.json to stack analysis v2 with valid user key
        Then I should get 400 status code

    
    @sav2
    Scenario Outline: Check the stack analysis v2 request and response for proper data
        Given System is running
        Given Three scale preview service is running
        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I wait 10 seconds
        When I send golang package request with manifest golist.json to stack analysis v2 with valid user key
        Then I should get 200 status code
        When I wait for stack analysis v2 to finish with user key
        Then I should find the external request id equals to id returned by stack analysis v2 post request
        And I should get stack analyses v2 response with all attributes

    
    @sav2
    Scenario: Data validation checks for golang ecosystem - public vulnerabilities
        Given System is running
        Given Three scale preview service is running
        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I wait 10 seconds
        When I send npm package request with manifest valid_golist.json to stack analysis v2 with valid user key with transitives
        Then I should get 200 status code
        And I should receive JSON response containing the status key
        And I should receive JSON response containing the id key
        And I should receive JSON response containing the submitted_at key
        And I should receive JSON response with the status key set to success
        And I should receive JSON response with the correct id
        And I should receive JSON response with the correct timestamp in attribute submitted_at
        When I wait for stack analysis v2 to finish with user key
        Then I should get stack analyses v2 response with all attributes
        And I should find 0 unknown licenses for stack analyses v2
        And I should find 3 distinct licenses for stack analyses v2
        And I should find distinct license Apache-2.0 for license analysis
        And I should be able to validate github data for all dependencies
        And I should get 4 transitive dependencies for github.com/rancher/rancher/pkg/clusterrouter
        And I should get 4 transitive vulnerabilities for github.com/rancher/rancher/pkg/clusterrouter
        And I should find github.com/moby/moby with upstream/0.1.1 20.10.0-beta1 20.10.0-beta1 with SNYK-GOLANG-GITHUBCOMMOBYMOBY-72364 and 7.5 for public vulnerbilities
        And I should find Authentication Bypass and high for github.com/moby/moby in public vulnerbilities
        And I should find License Apache-2.0 for github.com/moby/moby in analyzed dependencies
        And I should find buefy with 0.7.10 0.9.4 0.8.19 with SNYK-JS-BUEFY-567814 and 7.3 for private vulnerbilities
        And I should find Cross-site Scripting (XSS) and high for buefy in private vulnerbilities
        And I should find License MIT for buefy in analyzed dependencies
    

    @sav2
    Scenario: Data validation checks for golang ecosystem - private vulnerabilities
        Given System is running
        Given Three scale preview service is running
        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I wait 10 seconds
        When I send npm package request with manifest valid_golist.json to stack analysis v2 with valid user key with transitives
        Then I should get 200 status code
        And I should receive JSON response containing the status key
        And I should receive JSON response containing the id key
        And I should receive JSON response containing the submitted_at key
        And I should receive JSON response with the status key set to success
        And I should receive JSON response with the correct id
        And I should receive JSON response with the correct timestamp in attribute submitted_at
        When I wait for stack analysis v2 to finish with user key
        Then I should get stack analyses v2 response with all attributes
        And I should find github.com/gravitational/teleport/lib/client with 0.2.1 5.0.0-de 5.0.0-de with SNYK-GOLANG-GITHUBCOMGRAVITATIONALTELEPORTLIBCLIENT-564514 and 7.5 for private vulnerbilities
        And I should find Improper Validation and high for buefy in private vulnerbilities
        And I should find License Apache-2.0 for buefy in analyzed dependencies

    
    @sav2
    Scenario: Data validation checks for golang ecosystem - pesudo version
        Given System is running
        Given Three scale preview service is running
        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I wait 10 seconds
        When I send npm package request with manifest valid_golist.json to stack analysis v2 with valid user key with transitives
        Then I should get 200 status code
        And I should receive JSON response containing the status key
        And I should receive JSON response containing the id key
        And I should receive JSON response containing the submitted_at key
        And I should receive JSON response with the status key set to success
        And I should receive JSON response with the correct id
        And I should receive JSON response with the correct timestamp in attribute submitted_at
        When I wait for stack analysis v2 to finish with user key
        Then I should get stack analyses v2 response with all attributes
        And I should find github.com/kubernetes/kube-proxy with 0.0.0-20191212015419-c559daffcb0f 0.20.0-beta.1 0.0.0-20191016015246-999188f3eff6 with SNYK-GOLANG-GITHUBCOMKUBERNETESKUBEPROXY-575534 and 5.4 for public vulnerbilities
        And I should find Privilege Escalation and mediun for github.com/kubernetes/kube-proxy in public vulnerbilities
        