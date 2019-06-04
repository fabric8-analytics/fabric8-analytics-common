Feature: Visual Studio Code + the Analytics plugin basic functionality

    Scenario: Check that the Analytics plugin can be found in the Marketplace
        Given The PyAutoGUI library is initialized
          And The screen resolution is at least 1024x768 pixels
         When I start the Visual Studio Code
         Then I should find Visual Studio Code instance
         When I look at the whole screen
         Then I should find the activity bar
          And I should find the extension icon on the activity bar
         When I click on that region
          And I wait 2 seconds
          And I look at the whole screen
         Then I should find the Search extension in Marketplace input box
         When I click on that region
          And I type in Depencency Analytics
          And I wait 2 seconds
          And I look at the whole screen
         Then I should find the Dependency Analytics info region
         When I click on that region
          And I wait 2 seconds
          And I look at the whole screen
         Then I should find the OpenShift logo
          And I should find the Dependency Analytics header
          And I should find the Dependency Analytics title
          And I should find the Plugin install button
         When I look at the whole screen
          And I click on the File menu
          And I click on the Exit menu entry
          And I wait 2 seconds
         Then I should not find any Visual Studio Code instance
