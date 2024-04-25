/*******************************************************************************
 * Name        : unique.cpp
 * Author      : Aidan Fischer
 * Date        : September 19, 2020
 * Description : Determining uniqueness of chars with int as bit vector.
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/
#include <iostream>
#include <cctype>

using namespace std;

bool is_all_lowercase(const string &s) {
    // returns true if all characters in string are lowercase
    // letters in the English alphabet; false otherwise.
    for(const auto c : s){
        //Note that islower also makes sure that the character is alphabetical
        if(!islower(c)){
            return false;
        }
    }
    return true;
}

bool all_unique_letters(const string &s) {
    // returns true if all letters in string are unique, that is
    // no duplicates are found; false otherwise.
    // You may use only a single int for storage and work with bitwise
    // and bitshifting operators.
    // No credit will be given for other solutions.
    unsigned int bitset = 0;
    for(const auto c : s){
        if(bitset & (1 << (c - 'a'))){
            return false;
        }
        bitset = bitset | (1 << (c - 'a'));
    }
    return true;
}

int main(int argc, char * const argv[]) {
    // reads and parses command line arguments.
    // Calls other functions to produce correct output.
    string input;

    if(argc != 2){
        cerr << "Usage: " << argv[0] << " <string>" << endl;
        return 1;
    }

    input = argv[1];
    
    if(!is_all_lowercase(input)){
        cerr << "Error: String must contain only lowercase letters." << endl;
        return 1;
    }

    if(all_unique_letters(input)){
        cout << "All letters are unique." << endl;
    }else{
        cout << "Duplicate letters found." << endl;
    }
}
