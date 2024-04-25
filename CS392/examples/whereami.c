#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main() {
    FILE *fp = popen("pd 2>/dev/null", "r");
    if (fp == NULL) {
        fprintf(stderr, "Error: popen() failed. %s.\n", strerror(errno));
        exit(EXIT_FAILURE);
    }

    char path[PATH_MAX];
    size_t count = read(fileno(fp), path, PATH_MAX - 1);
    if (count == -1) {
        fprintf(stderr, "Error: read() failed.\n");
        exit(EXIT_FAILURE);
    }
    char *eoln = strchr(path, '\n');
    if (eoln != NULL) {
        *eoln = '\0';
    } else {
        path[count] = '\0';
    }

    int status = pclose(fp);
    if (status == -1) {
        fprintf(stderr, "Error: pclose() failed. %s.\n", strerror(errno));
        exit(EXIT_FAILURE);
    }    
    
    /* Use macros described under wait() to inspect 'status' in order
       to determine success/failure of command executed by popen(). */
    if (WIFEXITED(status) && WEXITSTATUS(status) == EXIT_SUCCESS) {
        printf("You are in %s\n", path);
        return EXIT_SUCCESS;
    }
    return EXIT_FAILURE;
}
