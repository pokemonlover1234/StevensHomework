###############################################################################
# Author: Aidan Fischer
# Date: 2/9/2021
# Pledge: I pledge my honor that I have abided by the Stevens Honor System
# Description: junk.sh acts as a substitute for the rm command. "junk"ing provided
# files so they aren't deleted permanently at first run. Equivalent to recycle bin
# on Windows
###############################################################################
#!/bin/bash

help_flag=0
list_flag=0
purge_flag=0
readonly junk_dir="$HOME/.junk"

read -r -d '' usage <<ENDOFTEXT
Usage: $(basename "$0") [-hlp] [list of files]
   -h: Display help.
   -l: List junked files.
   -p: Purge all files.
   [List of files] with no other arguments to junk those files.
ENDOFTEXT

while getopts ":hlp" option; do
    case "$option" in
       h) help_flag=1
          ;;
       l) list_flag=1
          ;;
       p) purge_flag=1
          ;;
       ?) cat <<ENDOFTEXT
Error: Unknown option '-${OPTARG}'
${usage}
ENDOFTEXT
          exit 1
          ;;
    esac
done

total_flags=0
(( total_flags = $help_flag + $list_flag + $purge_flag ))

shift "$((OPTIND-1))"

# If more than one flag is enabled, or if one or more options are enabled with other inputs
# Fail with an error and print the usage message.
# Note that I shift before this if statement, otherwise the second condition wouldn't work
# properly.

# Note to self: -z $var checks if var is empty
if [[ "$total_flags" -gt "1" || ( !(-z $@) && "$total_flags" -gt "0" )]]; then
   cat <<ENDOFTEXT
Error: Too many options enabled.
${usage}
ENDOFTEXT
   exit 1
fi

#If either -h is provided, or no options and no filenames are provided
#print the usage message.

if [[ "$help_flag" -eq "1" || (-z $@ && "$total_flags" -eq "0" )]]; then
  echo "$usage"
  exit 0
fi

#Check for presence of $HOME/.junk. Create it if necessary.

if ! [ -d $junk_dir ]; then
   $(mkdir "$junk_dir")
fi
   

if [ "$list_flag" -eq "1" ]; then
  ls -lAF "$junk_dir"
  exit 0
fi

shopt -s dotglob
shopt -s globstar


if [ "$purge_flag" -eq "1" ]; then
  for f in "$junk_dir/*"; do
    rm -r $f 2>/dev/null
  done
  exit 0
fi

#Finally process each file

for f in "$@"; do
   mv "$f" "$junk_dir/" 2> /dev/null
   if [ "$?" -eq "1" ]; then
     echo Warning: \'$f\' not found.
   fi
done

exit 0