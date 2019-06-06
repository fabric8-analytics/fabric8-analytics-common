Feature: Visual Studio Code basic functionality - check for version on CLI

    Scenario: Check the Visual Studio code via CLI
        Given The Visual Studio Code is set up
         When I start the Visual Studio Code with parameter --version
         Then I should find that version is set to 1.34.0
          And I should find that commit ID is a622c65b2c713c890fcf4fbf07cf34049d5fe758
