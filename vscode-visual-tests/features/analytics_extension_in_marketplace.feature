Feature: Visual Studio Code + the Analytics plugin basic functionality

    Scenario: Check that the Analytics plugin can be found in the Marketplace
        Given The PyAutoGUI library is initialized
          And The screen resolution is at least 1024x768 pixels
          And The Visual Studio Code is set up

         # Start the Visual Studio Code
         When I start the Visual Studio Code
         Then I should find Visual Studio Code instance
         When I look at the whole screen

         # Find the Analytics extension
         Then I should find the activity bar
          And I should find the extension icon on the activity bar
         When I click on that region
          And I wait 2 seconds
          And I look at the whole screen
         Then I should find the Search extension in Marketplace input box
         When I click on that region
          And I type in Dependency Analytics
          And I wait 2 seconds
          And I look at the whole screen
         Then I should find the Dependency Analytics info region

         # Install the Analytics extension
         When I click on that region
          And I wait 2 seconds
          And I look at the whole screen
         Then I should find the OpenShift logo
          And I should find the Dependency Analytics header
          And I should find the Dependency Analytics title
          And I should find the Plugin install button

         # Close the Visual Studio Code
         When I look at the whole screen
          And I click on the File menu
          And I click on the Exit menu entry
          And I wait for VSCode to close
         Then I should not find any Visual Studio Code instance
