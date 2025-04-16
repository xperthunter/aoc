#!/bin/bash

# For AoC Day 3 Part 1
# the pattern to use is: "mul\([0-9]{1,3},[0-9]{1,3}\)"

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <file> <pattern>"
    exit 1
fi

FILE=$1
PATTERN=$2

# Check if the file exists
if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' not found!"
    exit 1
fi

# Use grep to search for the pattern in the file
MATCHES=$(grep -oE "$PATTERN" "$FILE")
SUM=0

# Check if there are any matches
if [ -z "$MATCHES" ]; then
    echo "No matches found for '$PATTERN' in '$FILE'."
else
    echo "Matches found:"
    for MATCH in $MATCHES; do
    	if [[ $MATCH == "mul"* ]]; then
    		#echo "$MATCH"
    		read FIRST SECOND <<< $(echo "$MATCH" | awk -F'[(),]' '{print $2, $3}')
    		PRODUCT=$((FIRST * SECOND))
    		#echo "$PRODUCT"
    		SUM=$((SUM + PRODUCT))
    	fi
    	
    done
fi

echo "$SUM"

