Feature: Visual Studio Code + the Marketplace basic functionality

    Scenario: Check that the Analytics plugin can be found in the Marketplace
        Given The PyAutoGUI library is initialized
          And The screen resolution is at least 1024x768 pixels
          And The Visual Studio Code is set up

         # Start the Visual Studio Code
         When I start the Visual Studio Code
         Then I should find Visual Studio Code instance

         # Open the Search extension view
         When I click on the extension icon on the activity bar
         Then I should find the Search extension in Marketplace input box

         # Search for the Dependency plugin
         When I search for Dependency Analytics plugin
          And I select the plugin
         Then I should find the OpenShift logo
          And I should find the Dependency Analytics header
          And I should find the Dependency Analytics title
          And I should find the Plugin install button

         # Close the Visual Studio Code
         When I close the Visual Studio Code
         Then I should not find any Visual Studio Code instance
