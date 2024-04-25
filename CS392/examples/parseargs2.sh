#!/bin/bash

permissions_flag=0
size_flag=0

while getopts ":ps" option; do
    case "$option" in
        p) permissions_flag=1
           ;;
        s) size_flag=1
           ;;
        ?) echo "Error: Unknown option '-$OPTARG'." >&2
           exit 1
           ;;
    esac
done

# Skip over all the arguments with flags processed in the loop above.
shift "$((OPTIND-1))"

# How many flags are there?
count=$(( permissions_flag + size_flag ))

# Loop over all positional arguments.
for f in "$@"; do
    # ls is being called in a subshell. The result is a string that will be
    # assigned to the variable file_listing.
    file_listing=$(ls -l "$f" 2>/dev/null)

    if [ ! -z "$file_listing" ]; then
        if [ $count -eq 0 ]; then
            echo "$f"
        else
            echo -n "$f: "
        fi
        if [ $permissions_flag -eq 1 ]; then
            # Use cut to split the string into pieces.
            permissions=$(cut -d' ' -f1 <<<$file_listing)
            if [ $count -eq 1 ]; then
                echo "$permissions"
            else
                echo -n "$permissions, "
            fi
        fi
        if [ $size_flag -eq 1 ]; then
            file_size=$(cut -d' ' -f5 <<<$file_listing)
            echo "$file_size bytes"
        fi
    fi
done

exit 0
