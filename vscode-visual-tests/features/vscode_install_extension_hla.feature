Feature: Visual Studio Code + the Analytics plugin basic functionality

    Scenario: Check that the Analytics plugin can be found in the Marketplace
        Given The PyAutoGUI library is initialized
          And The screen resolution is at least 1024x768 pixels

         When I start the Visual Studio Code
         Then I should find Visual Studio Code instance
         When I look at the whole screen

         When I click on the extension icon on the activity bar
         Then I should find the Search extension in Marketplace input box

         When I search for Dependency Analytics plugin
          And I select the plugin
         Then I should find the OpenShift logo
          And I should find the Dependency Analytics header
          And I should find the Dependency Analytics title
          And I should find the Plugin install button

         When I start the installation by clicking on the Plugin install button
         Then I should find the Reload and Uninstall buttons
          And I should find the Reload button and Gear icon

         When I close the Visual Studio Code
         Then I should not find any Visual Studio Code instance
