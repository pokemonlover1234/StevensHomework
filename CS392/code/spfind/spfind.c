/*******************************************************************************
 * Name        : spfind.c
 * Author      : Aidan Fischer
 * Date        : 3/31/2021
 * Description : spfind implementation.
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdbool.h>

bool starts_with(const char *str, const char *prefix) {
    /* Return true if the string starts with prefix, false otherwise.
       Note that prefix might be longer than the string itself.
     */
    if(strlen(prefix) > strlen(str)){
      return false;
    } else {
      return (strncmp(str, prefix, strlen(prefix)) == 0);
    }
}

int main(int argc, char *argv[]) {
    int pfind_to_sort[2], sort_to_parent[2];
    if (pipe(pfind_to_sort) < 0) {
        fprintf(stderr, "Error: Cannot create pipe ps_to_grep. %s.\n",
                strerror(errno));
        return EXIT_FAILURE;
    }
    if (pipe(sort_to_parent) < 0) {
        fprintf(stderr, "Error: Cannot create pipe grep_to_parent. %s.\n",
                strerror(errno));
        return EXIT_FAILURE;
    }

    pid_t pid[2];
    if ((pid[0] = fork()) == 0) {
        // pfind
        close(pfind_to_sort[0]);
        dup2(pfind_to_sort[1], STDOUT_FILENO);

        // Close all unrelated file descriptors.
        close(sort_to_parent[0]);
        close(sort_to_parent[1]);

        if (execv("pfind",argv) < 0) {
            fprintf(stderr, "Error: pfind failed.\n");
            exit(EXIT_FAILURE);
        }
    }

    if ((pid[1] = fork()) == 0) {
        // sort
        close(pfind_to_sort[1]);
        dup2(pfind_to_sort[0], STDIN_FILENO);
        close(sort_to_parent[0]);
        dup2(sort_to_parent[1], STDOUT_FILENO);

        if (execlp("sort", "sort", NULL) < 0) {
            fprintf(stderr, "Error: sort failed.\n");
            exit(EXIT_FAILURE);
        }
    }

    close(sort_to_parent[1]);
    dup2(sort_to_parent[0], STDIN_FILENO);

    // Close all unrelated file descriptors.
    close(pfind_to_sort[0]);
    close(pfind_to_sort[1]);

    char buffer[4096];
    long lines = 0;
    bool printl = true;
    while (1) {
        ssize_t count = read(STDIN_FILENO, buffer, sizeof(buffer));
        if (count == -1) {
            if (errno == EINTR) {
                continue;
            } else {
                perror("read()");
                exit(EXIT_FAILURE);
            }
        } else if (count == 0) {
            break;
        } else {
            char *offset = strchr(buffer, '\n');
            while(offset != NULL && offset < buffer + count){
                lines++;
                offset = strchr(offset+1, '\n');
            }
            printl = printl & !starts_with(buffer, "Usage: ");
            write(STDOUT_FILENO, buffer, count);
        }
    }
    close(sort_to_parent[0]);
    // Don't forget to wait for both children.
    wait(NULL);
    wait(NULL);

    if(printl && lines > 0){
        printf("Total matchs: %ld\n", lines);
    }

    return EXIT_SUCCESS;
}
