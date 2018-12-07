#!/bin/bash

directories="dashboard db-integrity-tests integration-tests perf-tests reproducers ui-tests taas baf"

# checks for the whole directories
for directory in $directories
do
    grep -r -n "TODO: " "$directory"
done
