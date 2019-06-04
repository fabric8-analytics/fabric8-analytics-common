Feature: Visual Studio Code basic functionality

    Scenario: Basic check that use the common UI test steps
        Given The PyAutoGUI library is initialized
          And The screen resolution is at least 1024x768 pixels
          And The Visual Studio Code is set up

         When I start the Visual Studio Code with parameter --version
         Then I should find that version is set to 1.34.0
          And I should find that commit ID is a622c65b2c713c890fcf4fbf07cf34049d5fe758
