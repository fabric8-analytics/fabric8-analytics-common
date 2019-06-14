Feature: Smoke tests

    Scenario: Basic check that use the common UI test steps to perform sort of selftest
        Given The PyAutoGUI library is initialized
          And The screen resolution is at least 1024x768 pixels
          And The Visual Studio Code is set up

         When I start the Visual Studio Code
         Then I should find Visual Studio Code instance
         When I look at the whole screen
         Then I should find the activity bar

         When I look at the whole screen
         Then I should find the region with file menu header
         When I click on that region
          And I look at the whole screen
         Then I should find the region with file menu exit
         When I click on that region
          And I wait for VSCode close
         Then I should not find any Visual Studio Code instance


    Scenario: Basic check that use the HLA UI test steps to perform sort of selftest
        Given The PyAutoGUI library is initialized
          And The screen resolution is at least 1024x768 pixels
          And The Visual Studio Code is set up

         When I start the Visual Studio Code
         Then I should find Visual Studio Code instance

         When I look at the whole screen
          And I click on the File menu
          And I click on the Exit menu entry
          And I wait for VSCode close
         Then I should not find any Visual Studio Code instance
