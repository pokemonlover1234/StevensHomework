// // Declare a 2-dimensional array with 'some_size' rows.
// int some_size = 0;
// int some_other_size = 0;
// bool **array = new bool*[some_size];

// // For each row, make an array of 'some_other_size' booleans.
// for(int i = 0; i < some_size; ++i) {
//     array[i] = new bool[some_other_size];
//     // Fill the array with zeros.
//     fill(array[i], array[i] + some_other_size, false);
// }

// // Delete each array, that is, all the columns, first.
// for (int i = 0; i < some_size; ++i) {
//     delete [] array[i];
// }
// // Delete the array itself.
// delete [] array;

 