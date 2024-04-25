/*******************************************************************************
 * Name        : minishell.c
 * Author      : Aidan fischer
 * Date        : 4/11/2021
 * Description : minisheel assignment
 * Pledge : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/

#include "parsers.h"
#include "structs.h"
#include "commands.h"
#include <signal.h>
#include <errno.h>
#include <pwd.h>
#include <string.h>
#include <stdio.h>
#include <limits.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>
#include <sys/wait.h>

#define BRIGHTBLUE "\x1b[34;1m"
#define DEFAULT "\x1b[0m"

struct argsdata;
typedef struct argsdata arg_t;

volatile sig_atomic_t interrupt = false;
volatile sig_atomic_t term = false;

void catch_sigint(int sig){
    interrupt = true;
    return;
}

void catch_sigterm(int sig){
    term = true;
}

int run_prg(arg_t args, char *buf, char *cwd){
    pid_t pid = fork();
    if (pid < 0) {
        fprintf(stderr, "Error: fork() failed. %s.\n", strerror(errno));
        fflush(NULL);
        return EXIT_FAILURE;
    } 
    if (pid > 0) {
        int status = 0;
        do {
            // Wait for the child to complete and get the status of how it
            // terminated.
            pid_t w = waitpid(pid, &status, 0);
            if (w == -1 && !interrupt && !term && errno != ECHILD) {
                // waitpid failed
                fprintf(stderr, "Error: wait() failed. %s.\n", strerror(errno));
                fflush(NULL);
                exit(EXIT_FAILURE);
            }
            if(errno == ECHILD){
                errno = 0;
            }
        //Make sure interrupts both do not cause wait to stop executing prematurely, and also do not lock up the program.
        //If this is not done, while the !interrupt in the wait status would not cause an error, some processes
        //that take a bit to close out after an interrupt may cause some weird behavior. For example, weird
        //textual orders when interrupting dd, or the exit command not working, etc.
        } while (((!WIFEXITED(status) && !WIFSIGNALED(status)) || (interrupt && ((interrupt) = false) == false)) && !term);
    } else {
        // We're in the child.
        if (execvp(args.argv[0], args.argv) == -1) {
            fprintf(stderr, "Error: exec() failed. %s.\n", strerror(errno));
            fflush(NULL);
            //Child process has seperate memory space. Must free memory allocated by parent.
            free(buf);
            free(cwd);
            for(int i = 0; i < args.argc; i++){
                free(args.argv[i]);
            }
            free(args.argv);
            exit(EXIT_FAILURE);
        }
    }
    return EXIT_SUCCESS;
}

int main(int argc, char **argv){
    char *buf = (char *)malloc(BUFSIZE * sizeof(char));
    if(buf == NULL){
        fprintf(stderr, "Error: malloc() failed. %s.\n",strerror(errno));
        fflush(NULL);
        return EXIT_FAILURE;
    }
    char *cwd = (char *)malloc(PATH_MAX * sizeof(char));
    if(cwd == NULL){
        free(buf);
        fprintf(stderr, "Error: malloc() failed. %s.\n",strerror(errno));
        fflush(NULL);
        return EXIT_FAILURE;
    }

    struct sigaction action;

    memset(&action, 0, sizeof(struct sigaction));
    action.sa_handler = catch_sigint;

    if (sigaction(SIGINT, &action, NULL) == -1) {
        free(buf);
        free(cwd);
        fprintf(stderr, "Error: Cannot register signal handler. %s.\n", strerror(errno));
        fflush(NULL);
        return EXIT_FAILURE;
    }
    
    struct sigaction action2;

    memset(&action2, 0, sizeof(struct sigaction));
    action2.sa_handler = catch_sigterm;

    if (sigaction(SIGTERM, &action2, NULL) == -1) {
        free(buf);
        free(cwd);
        fprintf(stderr, "Error: Cannot register signal handler. %s.\n", strerror(errno));
        fflush(NULL);
        return EXIT_FAILURE;
    }

    if((cwd = getcwd(cwd, PATH_MAX * sizeof(char))) == NULL){
        free(buf);
        free(cwd);
        fprintf(stderr, "Error: Cannot get current working directory. %s.\n",strerror(errno));
        fflush(NULL);
        return EXIT_FAILURE;
    }

    uid_t uid = getuid();
    struct passwd *pwd; 
    if((pwd = getpwuid(uid)) == NULL){
        free(buf);
        free(cwd);
        fprintf(stderr, "Error: Cannot get passwd entry. %s.\n",strerror(errno));
        fflush(NULL);
        return EXIT_FAILURE;
    }

    while(true){
        printf("%s[%s%s%s]$ ",DEFAULT,BRIGHTBLUE,cwd,DEFAULT);\
        fflush(NULL);
        if(fgets(buf, BUFSIZE, stdin) == NULL && !interrupt && !term){
            free(buf);
            free(cwd);
            fprintf(stderr, "Failed to read from stdin. %s.\n", strerror(errno));
            fflush(NULL);
            return EXIT_FAILURE;
        }
        if(interrupt){
            interrupt = false;
            printf("\n");
            fflush(NULL);
            continue;
        }
        if(term){
            free(buf);
            free(cwd);
            fflush(NULL);
            return EXIT_SUCCESS;
        }
        if(strncmp("exit", buf, 4) == 0 && (strncmp("\n", buf + 4, 1) == 0 || strncmp(" ", buf + 4, 1) == 0)){
            free(buf);
            free(cwd);
            return EXIT_SUCCESS;
        }else if(strncmp("cd", buf, 2) == 0 && (strncmp("\n", buf + 2, 1) == 0 || strncmp(" ", buf + 2, 1) == 0)){
            arg_t arg = parse_args(buf);
            if(arg.argc == 0){

            }else if(arg.argc > 2){
                fprintf(stderr, "Error: Too many arguments to cd.\n");
                fflush(NULL);
            }else if(arg.argc == 1){
                cd(parse_path("~", pwd, cwd), cwd);
            }else{
                cd(parse_path(arg.argv[1], pwd, cwd), cwd);
            }
            for(int i = 0; i < arg.argc; i++){
                free(arg.argv[i]);
            }
            free(arg.argv);
        }else if(strlen(buf) > 1){
            arg_t arg = parse_args(buf);
            if(!(arg.argc == 0)){
                run_prg(arg, buf, cwd);
            }
            for(int i = 0; i < arg.argc; i++){
                free(arg.argv[i]);
            }
            free(arg.argv);
        }
    }
}