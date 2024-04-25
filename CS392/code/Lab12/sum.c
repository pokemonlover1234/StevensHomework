/*******************************************************************************
 * Name        : quicksort.c
 * Author      : Aidan Fischer
 * Date        : 5/7/2021
 * Description : Shared library reference.
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/

#include "sum.h"

/**
 * TODO:
 * Takes in an array of integers and its length.
 * Returns the sum of integers in the array.
 */
int sum_array(int *array, const int length) {
    int sum = 0;
    for(int i = 0; i < length; i++){
        sum += array[i];
    }
    return sum;
}
