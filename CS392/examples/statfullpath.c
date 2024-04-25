#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>

int main(int argc, char *argv[]){
    if(argc != 2){
        printf("Usage: %s <directory>\n", argv[0]);
        return EXIT_FAILURE;
    }
    char path[PATH_MAX];
    if(realpath(argv[1],path) == NULL){
        fprintf(stderr, "Error: Cannot get full path of file '%s'. %s.\n",
                argv[1],strerror(errno));
        return EXIT_FAILURE;
    }
    DIR *dir;
    if((dir = opendir(path)) == NULL){
        fprintf(stderr, "Error: Cannot open directory '%s'. %s.\n",
                path, strerror(errno));
    }

    struct dirent *entry;
    struct stat sb;
    char full_filename[PATH_MAX + 1];
    size_t pathlen = 0;

    //Set the initial character to the NULL byte;
    //If the path is '/', you can now take the strlen of a properly
    //terminated empty string.
    full_filename[0] = '\0';
    if(strcmp(path,"/")){
        //If path is not the root '/', then ...

        //If there is no NULL byte among the first n bytes of path,
        //the full_filename will not be terminated. So, copy up to and
        //including PATH_MAX characters.
        strncpy(full_filename, path, PATH_MAX);
    }
    //Add + 1 to the trailing '/' that we're going to add.
    pathlen = strlen(full_filename) + 1;
    full_filename[pathlen - 1] = '/';
    full_filename[pathlen] = '\0';

    while((entry = readdir(dir)) != NULL){
        if(strcmp(entry->d_name, ".") == 0 ||
        strcmp(entry->d_name, "..") == 0){
            continue;
        }
        strncpy(full_filename + pathlen, entry->d_name, PATH_MAX - pathlen);
        if(lstat(full_filename, &sb) < 0){
            fprintf(stderr, "Error: Cannot stat file '%s'. %s.\n",
                    full_filename, strerror(errno));
                    continue;
        }
        if(entry->d_type == DT_DIR){
            printf("%s [directory]\n", full_filename);
        } else {
            printf("%s\n", full_filename);
        }
    }
    closedir(dir);
    return EXIT_SUCCESS;
}