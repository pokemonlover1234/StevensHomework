/**
 * Name: Aidan Fischer
 * Lab 5
 * 3/12/2021
 * I pledge my honor that I have abided by the Stevens Honor System.
 */

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

int perms[] = {S_IRUSR, S_IWUSR, S_IXUSR,
               S_IRGRP, S_IWGRP, S_IXGRP,
               S_IROTH, S_IWOTH, S_IXOTH};

void display_usage(char *progname) {
    printf("Usage: %s <filename>\n", progname);
}

/**
 * 
 * Returns a string (pointer to char array) containing the permissions of the
 * file referenced in statbuf.
 * Allocates enough space on the heap to hold the 10 printable characters.
 * The first char is always a - (dash), since all files must be regular files.
 * The remaining 9 characters represent the permissions of user (owner), group,
 * and others: r, w, x, or -.
 */
char* permission_string(struct stat *statbuf) {
    //Allocate space to hold 10 printable characters and the terminating null byte.
    char *permstr = (char *)malloc(sizeof(char) * 11);
    //Set the initial - and the terminating null byte.
    permstr[0] = '-';
    permstr[10] = '\0';
    //Construct the rest of the string
    for(int i=0; i < 9; i+=3){
        if((statbuf->st_mode & perms[i]) > 0){
            permstr[i+1] = 'r';
        }else{
            permstr[i+1] = '-';
        }
        if((statbuf->st_mode & perms[i+1]) > 0){
            permstr[i+2] = 'w';
        }else{
            permstr[i+2] = '-';
        }
        if((statbuf->st_mode & perms[i+2]) > 0){
            permstr[i+3] = 'x';
        }else{
            permstr[i+3] = '-';
        }
    }
    return permstr;
}


int main(int argc, char *argv[]) {
    if (argc != 2) {
        display_usage(argv[0]);
        return EXIT_FAILURE;
    }

    struct stat statbuf;
    if (stat(argv[1], &statbuf) < 0) {
        fprintf(stderr, "Error: Cannot stat '%s'. %s.\n", argv[1],
                strerror(errno));
        return EXIT_FAILURE;
    }

    /* 
     * If the argument supplied to this program is not a regular file,
     * print out an error message to standard error and return EXIT_FAILURE.
     * For example:
     * $ ./permstat iamdir
     * Error: 'iamdir' is not a regular file.
     */

    //Note: man 2 stat suggested man 7 inode for more info on st_mode, which
    //provided a similar if statement that tested for regularity rather than
    //for a non regular file.
    if((statbuf.st_mode & S_IFMT) != S_IFREG){
        fprintf(stderr,"Error: '%s' is not a regular file.\n", argv[1]);
        return EXIT_FAILURE;
    }

    char *perms = permission_string(&statbuf);
    printf("Permissions: %s\n", perms);
    free(perms);

    return EXIT_SUCCESS;
}
