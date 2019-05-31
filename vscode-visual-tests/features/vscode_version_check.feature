Feature: Smoke test

    Scenario: Basic check that use the common UI test steps
        Given The PyAutoGUI library is initialized
          And The screen resolution is at least 1024x768 pixels
          And The Visual Studio Code is set up

         When I start the Visual Studio Code
         Then I should find Visual Studio Code instance
         When I look at the whole screen
         Then I should find the activity bar

         When I look at the whole screen
         Then I should find the region with help menu header
         When I click on that region
          And I look at the whole screen
         Then I should find the region with about menu item

         When I click on that region
          And I look at the whole screen
         Then I should find the region with about dialog
          And I should find the region with vscode version
          And I should find the region with commit id

         When I press Enter
          And I close the Visual Studio Code
         Then I should not find any Visual Studio Code instance
