/*******************************************************************************
 * Name          : pointers.cpp
 * Author        : Brian S. Borowski
 * Version       : 1.2
 * Date          : May 20, 2015
 * Last modified : August 30, 2019
 * Description   : Fun with pointers
 ******************************************************************************/
#include <iostream>

using namespace std;

/**
 * Displays an array of integers using conventional indexing.
 */
void display_array(int array[], const int length) {
    cout << "[";
    if (length > 0) {
        cout << array[0];
    }
    for (int i = 1; i < length; ++i) {
        cout << ", " << array[i];
    }
    cout << "]" << endl;
}

/**
 * Displays an array of integers using pointer arithmetic.
 */
void display_array_ptr(int array[], const int length) {
    cout << "[";
    if (length > 0) {
        cout << *array;
    }
    for (int *ptr = array + 1, *end = array + length; ptr < end; ++ptr) {
        cout << ", " << *ptr;
    }
    cout << "]" << endl;
}

void pass_by_value(int x) {
    x = 10;
}

void pass_by_pointer(int *x) {
    *x = 10;
}

void pass_by_reference(int &x) {
    x = 10;
}

int main() {
    int x = 5, y = 6, *z = &x;
    cout << z << endl;  // Displays the address of what z points.
    cout << *z << endl; // Displays the value of what z points to.
    cout << "x = " << x << ", y = " << y << endl;

    *z = 7;
    cout << "x = " << x << ", y = " << y << endl;

    z = &y;
    *z = 7;
    cout << "x = " << x << ", y = " << y << endl;

    /* This whole section is commented out, due to bad practices.

    cout << ++z << endl; // BAD IDEA: We're not sure what z points to now.
    cout << *z << endl;
    z += 30000;          // TERRIBLE IDEA: z points outside the address space
                         // of this process.
    *z = 30;             // Assigning a new value to the place z points will
                         // cause a segmentation fault.

    */

    int* values = new int[y];  // Allocates an array of integers on the heap.
    for (int i = 0; i < y; i++) {
        values[i] = i;
    }
    display_array(values, y);
    display_array_ptr(values, y);
    delete [] values;

    x = 5;
    pass_by_value(x);
    cout << "x = " << x << endl;

    x = 5;
    pass_by_pointer(&x);
    cout << "x = " << x << endl;

    x = 5;
    pass_by_reference(x);
    cout << "x = " << x << endl;

    return 0;
}
