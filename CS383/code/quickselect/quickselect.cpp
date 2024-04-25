/*******************************************************************************
 * Name          : quickselect.cpp
 * Author        : Aidan Fischer
 * Pledge        : I pledge my honor that I have abided by the Stevens Honor System.
 * Date          : October 22, 2020
 * Description   : Implements the quickselect algorithm found on page 160 in
 *                 Algorithms, 3e by Anany Levitin.
 ******************************************************************************/
#include <iostream>
#include <sstream>
#include <algorithm>
#include <vector>

using namespace std;

void swap(int &a, int &b){
    int temp = a;
    a = b;
    b = temp;
}

size_t lomuto_partition(int array[], size_t left, size_t right) {
    // DO NOT change the function header in any way.
    int p = array[left];
    size_t s = left;
    for(size_t i = left + 1; i <= right; ++i){
        if(array[i] < p){
            s++;
            swap(array[s], array[i]);
        }
    }
    swap(array[left], array[s]);
    return s;
}

int quick_select(int array[], size_t left, size_t right, size_t k) {
    // DO NOT change the function header in any way.
    size_t s = lomuto_partition(array, left, right);
    int res = 0;
    if(s == k-1){
        res = array[s];
    } else if (s > k - 1){
        res = quick_select(array, left, s-1, k);
    }
    else{
        res = quick_select(array, s+1, right, k);
    }
    return res;
}

int quick_select(int array[], const size_t length, size_t k) {
    return quick_select(array, 0, length - 1, k);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        cerr << "Usage: " << argv[0] << " <k>" << endl;
        return 1;
    }

    int k;
    istringstream iss;
    iss.str(argv[1]);
    if ( !(iss >> k) || k <= 0 ) {
        cerr << "Error: Invalid value '" << argv[1] << "' for k." << endl;
        return 1;
    }

    cout << "Enter sequence of integers, each followed by a space: " << flush;
    int value, index = 0;
    vector<int> values;
    string str;
    str.reserve(11);
    char c;
    iss.clear();
    while (true) {
        c = getchar();
        const bool eoln = c == '\r' || c == '\n';
        if (isspace(c) || eoln) {
            if (str.length() > 0) {
                iss.str(str);
                if (iss >> value) {
                    values.push_back(value);
                } else {
                    cerr << "Error: Non-integer value '" << str
                         << "' received at index " << index << "." << endl;
                    return 1;
                }
                iss.clear();
                ++index;
            }
            if (eoln) {
                break;
            }
            str.clear();
        } else {
            str += c;
        }
    }

    int num_values = values.size();
    if (num_values == 0) {
        cerr << "Error: Sequence of integers not received." << endl;
        return 1;
    }


    if (k > num_values){
        cerr << "Error: Cannot find smallest element " << k << " with only " <<
             num_values << " value" << (num_values == 1 ? "." : "s.") << endl;
        return 0;
    }

    int *values_array = new int[num_values];
    int i = 0;
    for(auto val: values){
        values_array[i++] = val;
    }

    int solution = quick_select(values_array, num_values, k);

    cout << "Smallest element " << k << ": " << solution << endl;

    return 0;
}
