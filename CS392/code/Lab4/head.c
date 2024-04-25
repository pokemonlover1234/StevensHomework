/**
 * Name: Aidan Fischer
 * No Partner
 * 3/5/2021 
 * I pledge my honor that I have abided by the Stevens Honor System.
 * File: head.c
 */

#include <ctype.h>
#include <errno.h>
#include <fcntl.h>
#include <getopt.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define BUFSIZE 16384
#define DEFAULT_LINE_COUNT 10

/**
 * Determines whether or not the input string represents a valid integer.
 * A valid integer has an optional minus sign, followed by a series of digits
 * [0-9].
 */
bool is_integer(char *input) {
    int start = 0, len = strlen(input);

    if (len >= 1 && input[0] == '-') {
        if (len < 2) {
            return false;
        }
        start = 1;
    }
    for (int i = start; i < len; i++) {
        if (!isdigit(input[i])) {
            return false;
        }
    }
    return true;
}

/**
 * Takes as input a string and an in-out parameter value.
 * If the string can be parsed, the integer value is assigned to the value
 * parameter and true is returned.
 * Otherwise, false is returned and the best attempt to modify the value
 * parameter is made.
 */
bool get_integer(char *input, int *value) {
    long long long_long_i;
    if (sscanf(input, "%lld", &long_long_i) != 1) {
        return false;
    }
    *value = (int)long_long_i;
    if (long_long_i != (long long)*value) {
        fprintf(stderr, "Warning: Integer overflow with '%s'.\n", input);
        return false;
    }
    return true;
}

/**
 * Displays the usage string for the program.
 */
void display_usage(char *progname) {
    printf("Usage: %s [-n num_lines] <filename>\n", progname);
}

/**
 * This program is a simplified version of head, which prints the first n lines
 * of a file.
 */
int main(int argc, char *argv[]) {
    if (argc == 1) {
        display_usage(argv[0]);
        return EXIT_FAILURE;
    }

    int opt = 0, line_count = DEFAULT_LINE_COUNT;
    char *n_value = NULL, *src_file = NULL;

    while ((opt = getopt(argc, argv, ":n:")) != -1) {
        switch (opt) {
            case 'n':
                n_value = optarg;
                break;
            case '?':
                if (optopt == 'n') {
                    fprintf(stderr,
                            "Error: Option '-%c' requires an argument.\n",
                            optopt);
                } else {
                    fprintf(stderr, "Error: Unknown option '-%c' received.\n",
                            optopt);
                }
                display_usage(argv[0]);
                return EXIT_FAILURE;
            default:
                return EXIT_FAILURE;
        }
    }

    if (n_value) {
        if (!is_integer(n_value) || !get_integer(n_value, &line_count) ||
            line_count < 0) {
            printf("Warning: Invalid line count '%s' supplied. "
                   "Using default of %d instead.\n",
                   n_value, DEFAULT_LINE_COUNT);
            line_count = DEFAULT_LINE_COUNT;
        }
    }
    if (optind + 1 < argc) {
        fprintf(stderr, "Error: Too many file names have been supplied.\n");
        return EXIT_FAILURE;
    } else if (optind + 1 > argc) {
        fprintf(stderr, "Error: No file name has been supplied.\n");
        return EXIT_FAILURE;
    }
    src_file = argv[optind];

    /* TODO - Use the system call open() to open the src_file for reading.
     * If it cannot be opened, print an error message with the following format:
     * "Error: Cannot open source file '%s': %s.\n"
     * The second %s should use strerror.
     */

    int src_fd;

    if((src_fd = open(src_file, O_RDONLY)) == -1){
        fprintf(stderr, "Error: Cannot open source file '%s': %s.\n",
        src_file, strerror(errno));
        return EXIT_FAILURE;
    }

    printf("==> %s (%d line%s) <==\n", src_file, line_count,
           (line_count == 1 ? "" : "s"));
    fflush(stdout);

    /* TODO - Use read() and write() to display the first n lines on the screen.
     * If n exceeds the line count of the file, display the whole file.
     * Do not use printf()!
     */

    //Make a buffer. Initialize everything to 0. Create a tracking pointer loc 
    //for use of pointer arithmetic.
    char *BUF = malloc(sizeof(char) * BUFSIZE);
    memset(BUF, '\0', BUFSIZE);
    char *loc = BUF;
    size_t chars = 0;
    int i = 0;
    int res;
    //Read one character at a time into BUF through the tracker pointer loc.
    //In order to not have wierd loop logic, do everything in a while loop
    //and track the number of lines printed with i. 
    while((res = read(src_fd, loc++, 1) > 0) && i < line_count){
        chars++;
        //Make sure we don't end up in unallocated memory, write what we have and flush the buffer.
        if(loc == BUF + BUFSIZE){
            write(1, BUF, BUFSIZE);
            loc = BUF;
            memset(BUF, '\0', chars);
            chars = 0;
        }
        //If we encounter a newline, print what we have (including the newline) and flush the buffer
        //then increment the current line count printed and continue.
        if(*(loc-1) == '\n'){
            write(1, BUF, chars);
            loc = BUF;
            memset(BUF, '\0', chars);
            chars = 0;
            i++;
        }
    }

    //If we still have chars to print, if the last char read wasn't a newline, then print them. 
    //No need to reset the other vars since we don't need them after this.

    //This only happens if the last number of lines specified is longer than the file and
    //the last line of the file is not a newline, because res is only 0 if we reach EOF.
    //In this case, the last line ends up on the same line as the terminal prompt, so 
    //for visuals, add a newline.

    if(res == 0 && loc > BUF){
        write(1, BUF, chars);
        write(1, "\n", 1);
    }

    if(res == -1){
        fprintf(stderr, "Error: Failed to continue reading input file '%s'. %s.\n",
        src_file, strerror(errno));
    }

    /* TODO - Close the file. Free up resources, if necessary. */

    close(src_fd);
    free(BUF);

    return EXIT_SUCCESS;
}