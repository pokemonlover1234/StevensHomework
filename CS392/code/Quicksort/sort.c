/*******************************************************************************
 * Name        : sort.c
 * Author      : Aidan Fischer
 * Date        : 2/27/2021
 * Description : Uses quicksort to sort a file of either ints, doubles, or
 *               strings.
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/
#include <errno.h>
#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "quicksort.h"

#define MAX_STRLEN     64 // Not including '\0'
#define MAX_ELEMENTS 1024

typedef enum {
    STRING,
    INT,
    DOUBLE
} elem_t;

/**
 * Reads data from filename into an already allocated 2D array of chars.
 * Exits the entire program if the file cannot be opened.
 */
size_t read_data(char *filename, char **data) {
    // Open the file.
    FILE *fp = fopen(filename, "r");
    if (fp == NULL) {
        fprintf(stderr, "Error: Cannot open '%s'. %s.\n", filename,
                strerror(errno));
        free(data);
        exit(EXIT_FAILURE);
    }

    // Read in the data.
    size_t index = 0;
    char str[MAX_STRLEN + 2];
    char *eoln;
    while (fgets(str, MAX_STRLEN + 2, fp) != NULL) {
        eoln = strchr(str, '\n');
        if (eoln == NULL) {
            str[MAX_STRLEN] = '\0';
        } else {
            *eoln = '\0';
        }
        // Ignore blank lines.
        if (strlen(str) != 0) {
            data[index] = (char *)malloc((MAX_STRLEN + 1) * sizeof(char));
            strcpy(data[index++], str);
        }
    }

    // Close the file before returning from the function.
    fclose(fp);

    return index;
}

/**
 * Basic structure of sort.c:
 *
 * Parses args with getopt.
 * Opens input file for reading.
 * Allocates space in a char** for at least MAX_ELEMENTS strings to be stored,
 * where MAX_ELEMENTS is 1024.
 * Reads in the file
 * - For each line, allocates space in each index of the char** to store the
 *   line.
 * Closes the file, after reading in all the lines.
 * Calls quicksort based on type (int, double, string) supplied on the command
 * line.
 * Frees all data.
 * Ensures there are no memory leaks with valgrind. 
 */
int main(int argc, char **argv) {
    int opt;
    int int_flag = 0;
    int dbl_flag = 0;

    const char *usage = 
"Usage: ./sort [-i|-d] filename\n\
   -i: Specifies the file contains ints.\n\
   -d: Specifies the file contains doubles.\n\
   filename: The file to sort.\n\
   No flags defaults to sorting strings.";
    if(argc <= 1){
        fprintf(stderr, "%s\n", usage);
        return EXIT_FAILURE;
    }

    while((opt = getopt(argc, argv, ":id")) != -1){
        switch(opt){
            case 'i':
                int_flag = 1;
                break;
            case 'd':
                dbl_flag = 1;
                break;
            case '?':
                fprintf(stderr, "Error: Unknown option '-%c' received.\n%s\n",optopt,usage);
                return EXIT_FAILURE;
        }
    }
    if(argc - optind == 0){
        fprintf(stderr, "Error: No input file specified.\n");
        return EXIT_FAILURE;
    }else if(argc - optind > 1){
        fprintf(stderr, "Error: Too many files specified.\n");
        return EXIT_FAILURE;
    }else if(int_flag + dbl_flag == 2){
        fprintf(stderr, "Error: Too many flags specified.\n");
        return EXIT_FAILURE;
    }

    //Determine the size of the data type we are processing in the file based on provided flag.
    size_t typesize = int_flag == 1 ? sizeof(int) : (dbl_flag == 1 ? sizeof(double) : sizeof(char *));

    //Get the data from the file
    char **data = (char **)calloc(MAX_ELEMENTS, sizeof(char *));
    size_t num_elements = read_data(argv[optind], data);

    //Maximum 1024 lines to process. 
    void *array = calloc(MAX_ELEMENTS, typesize);

    //Move data to array and convert if necessary
    if(int_flag == 1){
        for(size_t i = 0; i < num_elements; i++){
            ((int *)array)[i] = atoi(data[i]);
        }
    }else if(dbl_flag == 1){
        for(size_t i = 0; i < num_elements; i++){
            ((double *)array)[i] = atof(data[i]);
        }
    }else{
        for(size_t i = 0; i < num_elements; i++){
            ((char **)array)[i] = data[i];
        }
    }
    //Do the sorting
    quicksort(array, num_elements, typesize, int_flag == 1 ? &int_cmp : (dbl_flag == 1 ? &dbl_cmp : &str_cmp));
    //Output the result

    for(size_t i = 0; i < num_elements; i++){
        if(int_flag == 1){
            printf("%i\n",((int *)array)[i]);
        }else if(dbl_flag == 1){
            printf("%f\n",((double *)array)[i]);
        }else{
            printf("%s\n",((char **)array)[i]);
        }
    }
    if(int_flag == 1){
        free((int *)array);
    }else if(dbl_flag == 1){
        free((double *)array);
    }else{
        free((char **)array);
    }

    for(size_t i=0;i < num_elements; i++){
        free(data[i]);
    }
    free(data);
    return EXIT_SUCCESS;
}