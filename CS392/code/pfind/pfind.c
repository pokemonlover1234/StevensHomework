/*******************************************************************************
 * Name        : pfind.c
 * Author      : Aidan Fischer
 * Date        : 3/13/2021
 * Description : pfind main c for project
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System. 
 ******************************************************************************/

#include "precurse.h"
#include "permstring.h"
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>
#include <sys/stat.h>
#include <dirent.h>

void display_usage(char *progname){
    printf("Usage: %s -d <directory> -p <permissions string> [-h]\n",progname);
}

int main(int argc, char *argv[]){
    if(argc == 1){
        display_usage(argv[0]);
        return EXIT_FAILURE;
    }

    int opt = 0;    
    char *dirname, *permstr;

    //Flag trackers
    int d_present = 0, p_present = 0;

    while ((opt = getopt(argc, argv, ":hd:p:")) != -1) {
        switch (opt) {
            case 'h':
                display_usage(argv[0]);
                return EXIT_SUCCESS;
                break;
            case 'd':
                d_present = 1;
                dirname = optarg;
                break;
            case 'p':
                p_present = 1;
                permstr = optarg;
                break;
            case ':':
                if(optopt == 'd' || optopt == 'p') {
                    continue;
                } else{
                    fprintf(stderr, "Error: Unknown option '-%c' received.\n",
                            optopt);
                }
                return EXIT_FAILURE;
            case '?':
                fprintf(stderr, "Error: Unknown option '-%c' received.\n",
                        optopt);
                return EXIT_FAILURE;
            default:
                return EXIT_FAILURE;
        }
    }

    if(!d_present){
        fprintf(stderr, "Error: Required argument -d <directory> not found.\n");
        return EXIT_FAILURE;
    }
    if(!p_present){
        fprintf(stderr, "Error: Required argument -p <permissions string> not found.\n");
        return EXIT_FAILURE;
    }

    struct stat sb; 

    if(lstat(dirname, &sb) < 0){
        fprintf(stderr, "Error: Cannot stat '%s'. %s.\n",
                dirname, strerror(errno));
        return EXIT_FAILURE;
    }

    if(perm_invalid(permstr)){
        fprintf(stderr, "Error: Permissions string '%s' is invalid.\n", permstr);
        return EXIT_FAILURE;
    }

    int permint = permstr_to_int(permstr);

    //Note, since we don't add a trailing /, no need to have the extra logic from 
    //statfullpath.c regarding what happens if dirname is the root dir '/'
    char fullpath[PATH_MAX + 1];
    fullpath[0] = '\0';
    if((realpath(dirname, fullpath)) == NULL){
        fprintf(stderr, "Error: Could not resolve realpath of '%s'. %s.\n",
                dirname, strerror(errno));
    };

    DIR *start;

    if((start = opendir(dirname)) == NULL){
        fprintf(stderr, "Error: Cannot open directory '%s'. %s.\n",
                fullpath,strerror(errno));
        return EXIT_FAILURE;
    }

    pdir(start, permint, fullpath);
    closedir(start);
    return EXIT_SUCCESS;
}