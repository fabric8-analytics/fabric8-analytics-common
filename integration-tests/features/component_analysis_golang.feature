Feature: Component analysis V2 Batch Call API for Go lang ecosystem
    @cav2
    Scenario: Check the component analysis V2 REST API Batch Call for Golang ecosystem
        Given System is running
        Given Three scale preview service is running

        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I start CA batch call for test_golang_3.json with user_key
        Then I should get 200 status code
        And I should receive a valid JSON response
        Then I should be able to validate all the feilds or vulnerablities in the result
        And I should find package github.com/vmware-tanzu/velero/pkg/restore 1.5.2 has no recommendation
        And I should find package github.com/rancher/rancher/pkg/controllers/user/rbac 2.1.3 has v2.5.2-rc6 recommended version
        Then I should find snyk id SNYK-GOLANG-GITHUBCOMULIKUNITZXZ-598892 and 7.5 for package github.com/ulikunitz/xz and version 0.5.4
        Then I should find snyk id SNYK-GOLANG-GITHUBCOMGRAVITATIONALTELEPORTLIBCLIENT-564514 for package github.com/gravitational/teleport/lib/client and version 0.2.1 as private
        And I should not find any registered user fields



    @cav2
    Scenario: Check the component analysis V2 REST API Batch Call for unknown packages for golang ecosystem
        Given System is running
        Given Three scale preview service is running

        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I start CA batch call for test_golang_2.json with user_key
        Then I should get 202 status code
        And I should receive a valid JSON response

    @cav2
    Scenario: Check the component analysis V2 REST API Batch Call for 1 known 1 unknown package for golang ecosystem
        Given System is running
        Given Three scale preview service is running

        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I start CA batch call for test_golang_2.json with user_key
        Then I should get 202 status code
        And I should receive a valid JSON response
        Then I should be able to validate all the feilds or vulnerablities in the result
        And I should find one or more unknown packages in result
        And I should find package github.com/goharbor/harbor 1.8.4 has v2.1.1 recommended version
        And I should not find any registered user fields

    @cav2
    Scenario: Check the component analysis V2 REST API Batch Call for No vulnerablities for golang ecosystem
        Given System is running
        Given Three scale preview service is running

        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I start CA batch call for test_golang_1.json with user_key
        Then I should get 200 status code
        And I should receive a valid JSON response
        Then I should be able to validate all the feilds or vulnerablities in the result
        And I should not find any vulnerablities in result


    @cav2
    Scenario: Check the component analysis V2 REST API Batch Call without user key for golang ecosystem
        Given System is running
        Given Three scale preview service is running

        When I acquire the use_key for 3scale
        Then I should get the proper user_key
        When I start CA batch call for test_golang_1.json without user_key
        Then I should get 403 status code
