/*******************************************************************************
 * Name        : precurse.c
 * Author      : Aidan Fischer
 * Date        : 3/13/2021
 * Description : precurse implementation for project
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System. 
 ******************************************************************************/

#include "precurse.h"
#include "permstring.h"
#include <stdio.h>
#include <dirent.h>
#include <sys/stat.h>
#include <errno.h>
#include <string.h>

//Recurse through the directory specified by dir, finding 
//items with perm value perm and print out their paths. 
void pdir(DIR *dir, int perm, char *rootpath){
    struct dirent *entry;
    char entrypath[PATH_MAX+1];
    struct stat sb;
    while((entry = readdir(dir)) != NULL){
        if(strcmp(entry->d_name, ".") == 0 || 
           strcmp(entry->d_name, "..") == 0){
           continue;
        }
        //Construct the path for this entry.
        //Step 1: Copy the current path into entrypath
        //Step 2: Place a leading /
        //Step 3: Put the entry's name at the end
        //Step 4: Put a null byte after that. 
        //Since we copy to the start and add a null byte, no
        //need to reset entry path at each run of the while loop. 
        strcpy(entrypath, rootpath);
        int slash = 0;
        //Prevent adding a slash if the end of the string is already a slash.
        if(rootpath[strlen(rootpath)-1] != '/'){
            entrypath[strlen(rootpath)] = '/';
            slash = 1;
        }
        strcpy(entrypath + strlen(rootpath) + slash, entry->d_name);
        entrypath[strlen(rootpath) + strlen(entry->d_name) + slash] = '\0';

        //Stat the current entry
        if((lstat(entrypath, &sb)) < 0){
            //Skip on an error.
            fprintf(stderr, "Error: Cannot stat '%s'. %s.\n",
                    entrypath, strerror(errno));
            continue;
        }

        //Print entry if permissions match.
        if(permint_matches_stat(sb.st_mode, perm)){
            printf("%s\n", entrypath);
        }
        //If entry is a directory, recurse.
        if(S_ISDIR(sb.st_mode) > 0){
            //Attempt to open the directory.
            DIR *dir;
            //Skip on error.
            if((dir = opendir(entrypath)) == NULL){
                fprintf(stderr, "Error: Cannot open directory '%s'. %s.\n",
                entrypath,strerror(errno));
                continue;
            }
            pdir(dir, perm, entrypath);
            closedir(dir);
        }
    }
}
void printres(char *name){
    printf("%s\n",name);
}
