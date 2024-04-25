/**
 * This program trivially copies a file from one location to another.
 */
#include <errno.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>
#include <stdio.h>
#include <sys/stat.h>
#include <unistd.h>

#define BUFSIZE 128

void display_usage(char *progname){
    printf("Usage: %s <source> <destination>\n", progname);
}

int main(int argc, char *argv[]){
    if (argc != 3) {
        display_usage(argv[0]);
        return EXIT_FAILURE;
    }
    struct stat src_sb;
    if(stat(argv[1], &src_sb) < 0){
        fprintf(stderr, "Error: Error: Cannot stat source file '%s'. %s.\n",
                argv[1], strerror(errno));
        return EXIT_FAILURE;
    }

    struct stat dst_sb;
    int retval = stat(argv[2], &dst_sb);
    if(retval == 0 && src_sb.st_ino == dst_sb.st_ino){
        fprintf(stderr,"Error: Source and destination files are the same.\n");
        return EXIT_FAILURE;
    }

    int src_fd;
    if((src_fd = open(argv[1], O_RDONLY)) == -1){
        fprintf(stderr, "Error: Cannot open source file '%s'. %s.\n", 
                argv[1], strerror(errno));
        return EXIT_FAILURE;
    };


    int dst_fd;
    if((dst_fd = open(argv[2], O_WRONLY | O_TRUNC | O_CREAT, src_sb.st_mode)) == -1){
        fprintf(stderr, "Error: Cannot open/create destination file '%s'. %s.\n",
                argv[2], strerror(errno));
        close(src_fd);
        return EXIT_FAILURE;
    }



    char *buf;
    if ((buf = (char *)malloc(sizeof(char) * BUFSIZE)) == NULL){
        close(src_fd);
        close(dst_fd);
        fprintf(stderr, "Error: malloc failed.\n");
        return EXIT_FAILURE;
    }

    int bytes_read;
    while((bytes_read = read(src_fd, buf, BUFSIZE)) > 0){
        if(write(dst_fd, buf, bytes_read) != bytes_read){
            fprintf(stderr, "Error: Failed to write to file '%s'. %s.\n",
                    argv[2], strerror(errno));
            close(src_fd);
            close(dst_fd);
            free(buf);
            return EXIT_FAILURE;
        };
    };

    if (bytes_read == -1){
        fprintf(stderr, "Error: Failed to read from file '%s'. %s.\n",
                argv[1], strerror(errno));
        close(src_fd);
        close(dst_fd);
        free(buf);
        return EXIT_FAILURE;
    }
    close(src_fd);
    close(dst_fd);
    free(buf);
    return EXIT_SUCCESS;
}