#!/bin/bash

directories="dashboard db-integrity-tests integration-tests perf-tests reproducers ui-tests taas baf e2e_tests_bot vscode-visual-tests"

# checks for the whole directories
for directory in $directories
do
    grep -r -n "TODO: " "$directory"
done
