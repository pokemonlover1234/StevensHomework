/*******************************************************************************
 * Name          : algorithms.cpp
 * Author        : Brian S. Borowski
 * Version       : 1.0
 * Date          : September 18, 2014
 * Last modified : November 1, 2015
 * Description   : Numerous algorithms discussed in CS 385.
 ******************************************************************************/
#include <iostream>
#include <algorithm>
#include <sstream>
#include <string>
#include <vector>
#include <cmath>
#include <cstdlib>

using namespace std;

int two_increasing(int permutation[], int size) {
    for (int i = size - 1; i >= 1; --i) {
        if (permutation[i] > permutation[i - 1]) {
            return i - 1;
        }
    }
    return -1;
}

int find_largest_starting_at(int index, int permutation[], int size) {
    int val = permutation[index - 1];
    for (int i = size - 1; i >= index; --i) {
        if (permutation[i] > val) {
            return i;
        }
    }
    return -1;
}

string perm_to_string(int permutation[], int size) {
    ostringstream oss;
    oss << "[";
    for (int i = 0; i < size; ++i) {
        if (i != 0) {
            oss << ", ";
        }
        oss << permutation[i];
    }
    oss << "]";
    return oss.str();
}

void lexicographic_permute(int n) {
    int *permutation = new int[n];
    for (int i = 0; i < n; ++i) {
        permutation[i] = i + 1;
    }
    cout << "[" << perm_to_string(permutation, n);
    int i;
    while ((i = two_increasing(permutation, n)) != -1) {
        cout << ", ";
        int j = find_largest_starting_at(i + 1, permutation, n);
        swap(permutation[i], permutation[j]);
        reverse(permutation + i + 1, permutation + n);
        cout << perm_to_string(permutation, n);
    }
    cout << "]" << endl;
    delete [] permutation;
}

string chars_to_string(char permutation[], int size) {
    ostringstream oss;
    oss << "\"";
    for (int i = 0; i < size; i++) {
        oss << permutation[i];
    }
    oss << "\"";
    return oss.str();
}

int two_increasing(char permutation[], int size) {
    for (int i = size - 1; i >= 1; i--) {
        if (permutation[i] > permutation[i - 1]) {
            return i - 1;
        }
    }
    return -1;
}

int find_largest_starting_at(int index, char permutation[], int size) {
    char val = permutation[index - 1];
    for (int i = size - 1; i >= index; i--) {
        if (permutation[i] > val) {
            return i;
        }
    }
    return -1;
}

void string_permute(const string &s) {
    int n = s.length();
    char *permutation = new char[n];
    for (int i = 0; i < n; i++) {
        permutation[i] = s[i];
    }
    sort(permutation, permutation + n);
    cout << "[" << chars_to_string(permutation, n);
    int i;
    while ((i = two_increasing(permutation, n)) != -1) {
        cout << ", ";
        int j = find_largest_starting_at(i + 1, permutation, n);
        swap(permutation[i], permutation[j]);
        reverse(permutation + i + 1, permutation + n);
        cout << chars_to_string(permutation, n);
    }
    cout << "]" << endl;
    delete [] permutation;
}

vector< vector<int> > powerset(int *set, int length) {
    if (length == 0) {
        vector< vector<int> > outer;
        vector<int> inner;
        outer.push_back(inner);
        return outer;
    }
    vector< vector<int> > lose_it = powerset(set + 1, length - 1);
    vector< vector<int> > use_it(lose_it.begin(), lose_it.end());
    for (vector< vector<int> >::iterator it = use_it.begin(); it != use_it.end(); ++it) {
        it->push_back(set[0]);
    }
    lose_it.insert(lose_it.end(), use_it.begin(), use_it.end());
    return lose_it;
}

void display_vector_of_vectors(const vector< vector<int> > &v) {
    cout << "[";
    for (vector< vector<int> >::const_iterator it = v.begin(); it != v.end(); ++it) {
        if (it != v.begin()) {
            cout << ", ";
        }
        cout << "[";
        for (vector<int>::const_iterator it2 = it->begin(); it2 != it->end(); ++it2) {
            if (it2 != it->begin()) {
                cout << ", ";
            }
            cout << *it2;
        }
        cout << "]";
    }
    cout << "]" << endl;
}

unsigned long russian_peasant_multiplication(unsigned int m, unsigned int n) {
    if (n > m) {
        swap(m, n);
    }
    unsigned long sum = 0, big_m = m;
    while (n > 0) {
        if (n & 1) {
            sum += big_m;
        }
        n >>= 1;
        big_m <<= 1;
    }
    return sum;
}

vector<string> brgc(unsigned int n) {
    if (n == 0) {
        vector<string> code;
        code.push_back("0");
        return code;
    }
    if (n == 1) {
        vector<string> code;
        code.push_back("0");
        code.push_back("1");
        return code;
    }
    vector<string> v1 = brgc(n - 1);
    v1.reserve(v1.size() << 1);
    vector<string> v2;
    v2.reserve(v1.size());
    reverse_copy(v1.begin(), v1.end(), back_inserter(v2));
    for (vector<string>::iterator it = v1.begin(); it != v1.end(); ++it) {
        *it = "0" + *it;
    }
    for (vector<string>::iterator it = v2.begin(); it != v2.end(); ++it) {
        *it = "1" + *it;
    }
    v1.insert(v1.end(), v2.begin(), v2.end());
    return v1;
}

vector<string> inorder(unsigned int n) {
    if (n == 0) {
        vector<string> code;
        code.push_back("0");
        return code;
    }
    if (n == 1) {
        vector<string> code;
        code.push_back("0");
        code.push_back("1");
        return code;
    }
    vector<string> v1 = inorder(n - 1);
    v1.reserve(v1.size() << 1);
    vector<string> v2(v1);
    for (vector<string>::iterator it = v1.begin(); it != v1.end(); ++it) {
        *it = "0" + *it;
    }
    for (vector<string>::iterator it = v2.begin(); it != v2.end(); ++it) {
        *it = "1" + *it;
    }
    v1.insert(v1.end(), v2.begin(), v2.end());
    return v1;
}

vector< vector<int> > power_set(
        const vector<int> &set, bool use_gray_code = false) {

    vector<string> code;
    if (use_gray_code) {
        code = brgc(set.size());
    } else {
        code = inorder(set.size());
    }
    vector< vector<int> > ps;
    for (vector<string>::iterator it = code.begin();
            it != code.end(); ++it) {
        string &s = *it;
        vector<int> element;
        for (int i = 0, len = s.length(); i < len; ++i) {
            if (s[i] == '1') {
                element.push_back(set[i]);
            }
        }
        ps.push_back(element);
    }
    return ps;
}

void display_array(int array[], const int length) {
    cout << "[";
    for (int i = 0; i < length; ++i) {
        if (i != 0) {
            cout << ", ";
        }
        cout << array[i];
    }
    cout << "]" << endl;
}

int lomuto_partition(int array[], int left, int right) {
    int p = array[left], s = left;
    for (int i = left + 1; i <= right; ++i) {
        if (array[i] < p) {
            ++s;
            swap(array[s], array[i]);
        }
    }
    swap(array[left], array[s]);
    return s;
}

int quick_select(int array[], int left, int right, int k) {
    int s = lomuto_partition(array, left, right);
    if (s - left == k - 1) {
        return array[s];
    }
    if (s > left + k - 1) {
        return quick_select(array, left, s - 1, k);
    }
    return quick_select(array, s+1, right, k - 1 - s);
}

int randomized_select(int array[], int l, int r, int i) {
    if (l == r) {
        return array[l];
    }
    int random = l + (rand() % (int)(r - l + 1));
    swap(array[l], array[random]);
    int q = lomuto_partition(array, l, r),
        k = q - l + 1;
    if (i == k) {
        return array[q];
    }
    if (i < k) {
        return randomized_select(array, l, q - 1, i);
    }
    return randomized_select(array, q + 1, r, i - k);
}

void quicksort(int array[], int left, int right) {
    if (left < right) {
        size_t s = lomuto_partition(array, left, right);
        quicksort(array, left, s - 1);
        quicksort(array, s + 1, right);
    }
}

long left_right_binary_exp(int a, unsigned int b) {
    if (b == 0) {
        return 1;
    }
    int num_bits = (int)(log(b)/log(2)) + 1;
    long product = a;
    for (int i = num_bits - 2; i >= 0; --i) {
        product *= product;
        if (((b >> i) & 1) == 1) {
            product *= a;
        }
    }
    return product;
}

void display_vector(const vector<int> &v) {
    cout << "[";
    for (size_t i = 0; i < v.size(); ++i) {
        if (i != 0) {
            cout << ", ";
        }
        cout << v[i];
    }
    cout << "]" << endl;
}

vector< vector<int> > all_permutations(vector<int> &v1, vector<int> &v2) {
    vector< vector<int> > temp;
    if (v1.size() == 0) {
        temp.push_back(v2);
        return temp;
    }
    for (size_t i = 0; i < v1.size(); ++i) {
        // Choose an element to remove
        int choice = v1[i];
        v1.erase(v1.begin() + i);
        v2.push_back(choice);

        // Explore the remaining elements recursively
        vector< vector<int> > subset;
        subset = all_permutations(v1, v2);
        temp.insert(temp.end(), subset.begin(), subset.end());

        // Un-choose the element
        v1.insert(v1.begin() + i, choice);
        v2.erase(v2.begin() + v2.size() - 1);
    }
    return temp;
}

vector< vector<int> > all_permutations(vector<int> &values) {
    vector<int> v2;
    return all_permutations(values, v2);
}

int main(int argc, char * const argv[]) {
    lexicographic_permute(1);
    lexicographic_permute(3);
    lexicographic_permute(4);
    cout << endl;

    string_permute("dog");
    cout << endl;

    unsigned int m = 45, n = 67;
    cout << m << " x " << n << " = " <<
            russian_peasant_multiplication(m, n) << endl << endl;

    cout << "Binary reflected gray codes:" << endl;
    vector<string> gray_code = brgc(4);
    for (vector<string>::iterator it = gray_code.begin();
            it != gray_code.end(); ++it) {
        cout << *it << endl;
    }
    cout << endl;

    int ints[] = {1, 5, 34, 76};
    vector<int> v(ints, ints + sizeof(ints) / sizeof(int));
    vector< vector<int> > ps = power_set(v);
    cout << "Power set of ";
    display_array(ints, 4);
    display_vector_of_vectors(ps);
    cout << endl;

    m = 2;
    n = 14;
    cout << m << "^" << n << " = " << left_right_binary_exp(m, n)
         << endl << endl;

    cout << "Permutations: ";
    vector< vector<int> > perms = all_permutations(v);
    display_vector_of_vectors(perms);
    cout << endl;

    int array2[] = {90, 12, 45, 62, 13, 56, 56, 2, 91, 42, 67, 88};
    int k;
    cout << "Enter k(1-12): ";
    cin >> k;
    cout << "k(" << k << ") = " << randomized_select(array2, 0, 11, k)
         << endl << endl;

    quicksort(array2, 0, 11);
    display_array(array2, 12);
    return 0;
}
