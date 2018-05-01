directories="dashboard db-integrity-tests integration-tests perf-tests reproducers ui-tests"

# checks for the whole directories
for directory in $directories
do
    grep -r -n "TODO: " $directory
done
