#!/bin/bash

file=sqrt.cpp

if [ ! -f "$file" ]; then
    echo -e "Error: File '$file' not found.\nTest failed."
    exit 1
fi

num_right=0
total=0
line="________________________________________________________________________"
compiler=
interpreter=
language=
extension=${file##*.}
if [ "$extension" = "py" ]; then
    if [ ! -z "$PYTHON_PATH" ]; then
        interpreter=$(which python.exe)
    else
        interpreter=$(which python3.2)
    fi
    command="$interpreter $file"
    echo -e "Testing $file\n"
elif [ "$extension" = "java" ]; then
    language="java"
    command="java ${file%.java}"
    echo -n "Compiling $file..."
    javac $file
    echo -e "done\n"
elif [ "$extension" = "c" ] || [ "$extension" = "cpp" ]; then
    language="c"
    command="./${file%.*}"
    echo -n "Compiling $file..."
    results=$(make 2>&1)
    if [ $? -ne 0 ]; then
        echo -e "\n$results"
        exit 1
    fi
    echo -e "done\n"
fi

run_test_args() {
    (( ++total ))
    echo -n "Running test $total..."
    expected=$2
    received=$( $command $1 2>&1 | tr -d '\r' )
    if [ "$expected" = "$received" ]; then
        echo "success"
        (( ++num_right ))
    else
        echo -e "failure\n\nExpected$line\n$expected\nReceived$line\n$received\n"
    fi
}

run_test_args "" "Usage: ./sqrt <value> [epsilon]"
run_test_args "10 11 12" "Usage: ./sqrt <value> [epsilon]"
run_test_args "x" "Error: Value argument must be a double."
run_test_args "10 x" "Error: Epsilon argument must be a positive double."
run_test_args "10 0" "Error: Epsilon argument must be a positive double."
run_test_args "10 -1" "Error: Epsilon argument must be a positive double."
run_test_args "-1" "nan"
run_test_args "0" "0.00000000"
run_test_args "1" "1.00000000"
run_test_args "4" "2.00000000"
run_test_args "1048576" "1024.00000000"
run_test_args "10" "3.16227766"
run_test_args "734658345" "27104.58162378"
run_test_args "734658345.000" "27104.58162378"
run_test_args "734658345 1000" "27107.99975188"
run_test_args "734658345 100" "27104.58183928"
run_test_args "734658345 10" "27104.58183928"
run_test_args "734658345 1" "27104.58162378"
run_test_args "20.0 1" "4.47831445"
run_test_args "20.0 0.1" "4.47214022"
run_test_args "20.0 0.01" "4.47214022"
run_test_args "20.2 0.0001" "4.49444101"

echo -e "\nTotal tests run: $total"
echo -e "Number correct : $num_right"
echo -n "Percent correct: "
echo "scale=2; 100 * $num_right / $total" | bc

if [ "$language" = "java" ]; then
   echo -e -n "\nRemoving class files..."
   rm -f *.class
   echo "done"
fi
