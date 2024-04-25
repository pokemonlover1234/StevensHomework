#!/bin/bash
###############################################################################
# filecheck.sh
# Takes in a list of files and an optional -s flag.
# Prints the files that exist, and if -s is supplied, the size of the file.
# Example: ./filecheck.sh -s ~/*
###############################################################################

size_flag=0

# Parse command line arguments with getopts
# The leading : suppressed built-in error handling.
# A : after an option means that flag requires and argument.
while getopts ":s" option; do
    case "$option" in
        s) size_flag=1
           ;;
        ?) printf "Error: Unknown option '-%s'.\n" $OPTARG >&2
           exit 1
           ;;
    esac
done

declare -a filenames
# Slide the command line arguments over so that the first non-flag
# argument is at $1.
shift "$(( OPTIND-1 ))"
index=0
for f in "$@"; do
    # Put the file name in the array, only if the regular file exists.
    if [ -f "$f" ]; then
        filenames[$index]="$f"
        (( ++index ))
    fi
done

index=0
if [ $size_flag -eq 1 ]; then
    for f in "${filenames[@]}"; do
        size=$(ls -l "$f" | cut -d' ' -f5)
        filenames[$index]="${f}: ${size} bytes"
        (( ++index ))
    done
fi

# Use @ instead of * so that white space in array element does not
# further break down into smaller elements.
for f in "${filenames[@]}"; do
    echo "$f"
done
