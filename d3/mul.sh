#!/bin/bash

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
    		echo "$MATCH"
    		read FIRST SECOND <<< $(echo "$MATCH" | awk -F'[(),]' '{print $2, $3}')
    		PRODUCT=$((FIRST * SECOND))
    		echo "$PRODUCT"
    		SUM=$((SUM + PRODUCT))
    	elif [[ ]]
    	fi
    	
    done
    
    # Additional processing: Save matches to a new file
    #echo "$MATCHES" > matches.txt
    #echo "Matches saved to 'matches.txt'."
fi

echo "$SUM"

