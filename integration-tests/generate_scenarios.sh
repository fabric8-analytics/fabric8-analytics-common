#!/bin/bash

# Script to generate Markdown files for all scenarios
# Author: Pavel Tisnovsky <ptisnovs@redhat.com>

# need to be set to be able to read the grepped scenarios
IFS=$'\n'

# process all input feature files
for file in features/*.feature
do
    echo "$file"
    # define the output file name
    outfile="${file/features\//scenarios\/}"
    outfile="${outfile/\.feature/\.md}"

    # find the feature line in the input file
    feature=$(grep "Feature: " "$file")
    feature="${feature/Feature:/\# Feature:}"
    echo "$feature" | tee "$outfile"

    # find all scenarios and scenario outlines
    scenarios=$(grep "^\s\+Scenario" "$file")
    for line in $scenarios
    do
        stripped=$(echo "$line" | sed -e "s/^\s\+//")
        echo "- $stripped" | tee -a "$outfile"
    done
    echo
done
