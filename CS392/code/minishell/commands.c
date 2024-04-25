/*******************************************************************************
 * Name        : precurse.h
 * Author      : Aidan Fischer
 * Date        : 4/11/2021
 * Description : commands implementation for minishell 
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System. 
 ******************************************************************************/

#include "commands.h"
#include "structs.h"
#include <errno.h>
#include <stdio.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

struct argsdata;
typedef struct argsdata arg_t;

int cd(char *path, char *cwd){
    if(strlen(path) == 0){
        free(path);
        return EXIT_FAILURE;
    }
    if(chdir(path) == -1){
        fprintf(stderr, "Error: Cannot change directory to '%s'. %s.\n", path, strerror(errno));
        fflush(NULL);
        free(path);
        return EXIT_FAILURE;
    }
    free(path);
    if((cwd = getcwd(cwd, PATH_MAX * sizeof(char))) == NULL){
        fprintf(stderr, "Error: Cannot get current working directory. %s.\n",strerror(errno));
        fflush(NULL);
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}
