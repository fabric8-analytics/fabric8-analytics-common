Feature: Installation and uninstallation of Analytics pluging for the Visual Code Studio

    Scenario: Check that the Analytics plugin has not been installed
        Given The Visual Studio Code is set up
         When I start the Visual Studio Code with parameter --list-extensions
         Then I should find that extension redhat.fabric8-analytics is not installed


    Scenario: Check that the Analytics plugin can be installed from the Marketplace
        Given The PyAutoGUI library is initialized
          And The screen resolution is at least 1024x768 pixels
          And The Visual Studio Code is set up

         # Start the Visual Studio Code
         When I start the Visual Studio Code
         Then I should find Visual Studio Code instance

         # Find the Analytics extension
         When I click on the extension icon on the activity bar
         Then I should find the Search extension in Marketplace input box

         # Check the analytics info page
         When I search for Dependency Analytics plugin
          And I select the plugin
         Then I should find the OpenShift logo
          And I should find the Dependency Analytics header
          And I should find the Dependency Analytics title
          And I should find the Plugin install button

         # Install the Analytics extension
         When I start the installation by clicking on the Plugin install button
         Then I should find the Installed icon and Gear button
          And I should find the Installed icon and Uninstall button

         # Close the Visual Studio Code
         When I close the Visual Studio Code
         Then I should not find any Visual Studio Code instance


    Scenario: Check that the Analytics plugin has been installed
        Given The Visual Studio Code is set up
         When I start the Visual Studio Code with parameter --list-extensions
         Then I should find that extension redhat.fabric8-analytics is installed


    Scenario: Check that the Analytics plugin can be uninstalled
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

         # Go to the analytics info page
         When I click on that region
          And I wait 2 seconds
          And I look at the whole screen
         Then I should find the Plugin uninstall button

         # Uninstall plugin
         When I click on that region
          And I wait 2 seconds
          And I look at the whole screen
         Then I should find the Uninstalled label

         # Close the Visual Studio Code
         When I look at the whole screen
          And I click on the File menu
          And I click on the Exit menu entry
          And I wait for VSCode to close
         Then I should not find any Visual Studio Code instance


    Scenario: Check that the Analytics plugin has not been installed
        Given The Visual Studio Code is set up
         When I start the Visual Studio Code with parameter --list-extensions
         Then I should find that extension redhat.fabric8-analytics is not installed
