Feature: Visual Studio Code + the Analytics plugin extended functionality: stack report

    Scenario: Check that the Analytics plugin has been installed
        Given The Visual Studio Code is set up
         When I start the Visual Studio Code with parameter --list-extensions
         Then I should find that extension redhat.fabric8-analytics is installed


    Scenario: Analysis result for a NPM project with one dependency and one CVE
        Given The PyAutoGUI library is initialized
          And The Visual Studio Code is set up

         # Start the Visual Studio Code
         When I start the Visual Studio Code with project projects/npm_1_dependency_1_CVE
         Then I should find Visual Studio Code instance

         # Check the code area
         When I wait for VSCode text editor to open
          And I look at the whole screen
         Then I should find region dependencies in package json or dependencies in package json 2

         # Display context menu
         When I right click on that region
          And I wait for context menu
          And I look at the whole screen
         Then I should find the Dependency Analysis Report menu entry in context menu

         # Run the analysis and check the results
         When I click on that region
          And I wait for the detailed analysis to finish
          And I look at the whole screen
         Then I should find Analytics page with Issues header
         Then I should find Analytics page with Insights header
         Then I should find Analytics page with Licenses header
         Then I should find Analytics page with Dependency details header

         # Close the analysis
         When I press Ctrl+W
          And I wait 2 seconds

         # Close the editor
          And I press Ctrl+W
          And I wait for VSCode text editor to close
          And I look at the whole screen
         Then I should find the empty window or Welcome tab

         # Close the Visual Studio Code
         When I look at the whole screen
          And I click on the File menu
          And I click on the Exit menu entry
          And I wait for VSCode to close
         Then I should not find any Visual Studio Code instance
