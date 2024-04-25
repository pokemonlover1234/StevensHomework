/*******************************************************************************
 * Name        : stairclimber.cpp
 * Author      : Aidan Fischer
 * Date        : September 27, 2020
 * Description : Lists the number of ways to climb n stairs.
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/
#include <iostream>
#include <vector>
#include <algorithm>
#include <sstream>
#include <iomanip>

using namespace std;

vector< vector<int> > get_ways(int num_stairs) {
    // Return a vector of vectors of ints representing
    // the different combinations of ways to climb num_stairs
    // stairs, moving up either 1, 2, or 3 stairs at a time.
    vector<vector<int>> ways;
    if(num_stairs <= 0){
        ways.push_back(vector<int>());
    }
    else{
        for(int i = 1; i < 4; i++){
            if(num_stairs >= i){
                vector<vector<int>> result = get_ways(num_stairs - i);
                for(long unsigned int j = 0; j < result.size(); j++){
                    result[j].insert(result[j].cbegin(), i);
                }
                ways.insert(ways.cend(),result.cbegin(),result.cend());
            }
        }
    }
    return ways;
}

//Taken from sieve project.
int num_digits(int num) {
    // Start the count at one (all numbers have at least one digit), then
    // keep dividing by 10 and adding a digit until the number is less than
    // 10.
    int count = 1;
    while(num >= 10){
        count++;
        num /= 10;
    }
    return count;
}

void display_ways(const vector< vector<int> > &ways) {
    // Display the ways to climb stairs by iterating over
    // the vector of vectors and printing each combination.
    int label_length = num_digits(ways.size());
    for(long unsigned int i = 0; i < ways.size(); i++){
        cout << setw(label_length) << i + 1 << ". [";
        for(long unsigned int j = 0; j < ways[i].size(); j++){
            cout << ways[i][j];
            if(j < ways[i].size() - 1){
                cout << ", ";
            }
            else{
                cout << "]" << endl;
            }
        }
    }
}

int main(int argc, char * const argv[]) {
    int stairs;

    if(argc != 2){
        cerr << "Usage: " << argv[0] << " <number of stairs>" << endl;
        return 1;
    }

    istringstream iss(argv[1]);

    if(!(iss >> stairs)){
        cerr << "Error: Number of stairs must be a positive integer." << endl;
        return 1;
    }

    if(stairs <= 0){
        cerr << "Error: Number of stairs must be a positive integer." << endl;
        return 1;
    }
    vector<vector<int>> ways = get_ways(stairs);
    if(stairs == 1){
        cout << ways.size() << " way to climb " << stairs << " stair";
    }
    else{
        cout << ways.size() << " ways to climb " << stairs << " stairs";
    }
    cout << "." << endl;
    display_ways(ways);
    return 0;
}
