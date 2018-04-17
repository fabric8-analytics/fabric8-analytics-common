Feature: Resilient storage

  @requires.openshift.console.access
  Scenario: Check if user is logged in the OpenShift
    Given The OpenShift Client is installed
    When I run OC command to show information about the current session
    Then I should get the user name

  @requires.openshift.console.access
  Scenario: Check if the f8a-server-backbone is deployed and running
    Given The OpenShift Client is installed
    When I ask for statuses of all deployments
    Then I should find that the deployment f8a-server-backbone exists
    When I ask for status of the f8a-server-backbone service
    Then I should find that the service f8a-server-backbone exists

  @requires.openshift.console.access
  Scenario: Check what happens to server when the f8a-server-backbone is restarted
    Given The OpenShift Client is installed
    When I access the /api/v1/ 30 times with 2 seconds delay
    Then I should get 200 status code for all calls
    When I delete all pods for the service f8a-server-backbone
     And I access the /api/v1/ 30 times with 2 seconds delay
    Then I should get 200 status code for all calls
