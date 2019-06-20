Feature: Visual Studio Code basic functionality - ability to start and stop

    Scenario: Basic check if tests are able to start and stop the Visual Studio Code
        Given The PyAutoGUI library is initialized
          And The screen resolution is at least 1024x768 pixels
          And The Visual Studio Code is set up

         # Start the Visual Studio Code
         When I start the Visual Studio Code
         Then I should find Visual Studio Code instance

         # Close the Visual Studio Code via File->Exit
         When I look at the whole screen
          And I click on the File menu
          And I click on the Exit menu entry
          And I wait 2 seconds
         Then I should not find any Visual Studio Code instance
