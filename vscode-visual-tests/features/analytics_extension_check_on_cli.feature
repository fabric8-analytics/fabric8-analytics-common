Feature: Visual Studio Code + the Analytics plugin basic functionality

    Scenario: Check that the Analytics plugin can be found in the Marketplace
        Given The PyAutoGUI library is initialized
          And The screen resolution is at least 1024x768 pixels
          And The Visual Studio Code is set up

         When I start the Visual Studio Code with parameter --list-extensions
         Then I should find that extension redhat.fabric8-analytics is installed
