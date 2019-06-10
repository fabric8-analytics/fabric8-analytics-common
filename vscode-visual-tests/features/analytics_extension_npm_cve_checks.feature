Feature: Visual Studio Code + the Analytics plugin basic functionality: displaying problems on status bar

    Scenario: Check that the Analytics plugin has been installed
        Given The Visual Studio Code is set up
         When I start the Visual Studio Code with parameter --list-extensions
         Then I should find that extension redhat.fabric8-analytics is installed


    Scenario: Analysis result for a NPM project with zero dependencies and thus zero CVEs
        Given The PyAutoGUI library is initialized
          And The Visual Studio Code is set up

         # Start the Visual Studio Code
         When I start the Visual Studio Code with parameter projects/npm_0_dependencies_0_CVEs/package.json
         Then I should find Visual Studio Code instance

         # Check the code area
         When I wait 2 seconds
          And I look at the whole screen
         Then I should find the region with dependencies in package json

         # Check that number of problems is zero before the analysis is performed
         When I look at the whole screen
         Then I should find the icon with info about zero problems in the status bar

         # Display context menu
         When I look at the whole screen
         Then I should find the region with dependencies in package json
         When I right click on that region
          And I wait 2 seconds
          And I look at the whole screen
         Then I should find the Dependency Analysis Report menu entry in context menu

         # Run the analysis and check the results
         When I click on that region
          And I wait 5 seconds
          And I look at the whole screen
         Then I should find the icon with info about zero problems in the status bar

         # Close the editor
         When I press Ctrl+W
          And I wait 2 seconds
          And I look at the whole screen
         Then I should find the empty window or Welcome tab

         # Close the Visual Studio Code
         When I look at the whole screen
          And I click on the File menu
          And I click on the Exit menu entry
          And I wait 2 seconds
         Then I should not find any Visual Studio Code instance
