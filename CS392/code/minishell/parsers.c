/*******************************************************************************
 * Name        : precurse.h
 * Author      : Aidan Fischer
 * Date        : 4/11/2021
 * Description : parsers implementation for minishell 
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System. 
 ******************************************************************************/

#include "structs.h"
#include "parsers.h"
#include <ctype.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <errno.h>

struct statedata;
typedef struct statedata state_t;

// Stores the trimmed input string into the given output buffer, which must be
// large enough to store the result.  If it is too small, the output is
// truncated.

//Source: https://stackoverflow.com/a/122721

size_t trimwhitespace(char *out, size_t len, const char *str)
{
  if(len == 0)
    return 0;

  const char *end;
  size_t out_size;

  // Trim leading space
  while(isspace((unsigned char)*str)) str++;

  if(*str == 0)  // All spaces?
  {
    *out = 0;
    return 1;
  }

  // Trim trailing space
  end = str + strlen(str) - 1;
  while(end > str && isspace((unsigned char)*end)) end--;
  end++;

  // Set output size to minimum of trimmed string length and buffer size minus 1
  out_size = (end - str) < len-1 ? (end - str) : len-1;

  // Copy trimmed string and add null terminator
  memcpy(out, str, out_size);
  out[out_size] = 0;

  return out_size;
}

arg_t parse_args(char *args){
    arg_t arg;

    //Strip whitespace from beginning and end, and store result in argstr
    char *argstr = (char *)malloc(BUFSIZE * sizeof(char));
    if(argstr == NULL){
        fprintf(stderr, "Error: malloc() failed. %s.\n",strerror(errno));
        fflush(NULL);
        arg.argc = 0;
        return arg;
    }
    trimwhitespace(argstr, BUFSIZE, args);

    //Handle quotes

    char *delim = "\"";
    int count = 0;
    char *tmp = argstr;

    //Count quotes
    while(*tmp){
        if(delim[0] == *tmp){
            count++;
        }
        tmp++;
    }

    //Return empty args if an uneven number of quotes is detected. 
    if(count % 2 == 1){
        fprintf(stderr, "Error: Malformed Command.\n");
        fflush(NULL);
        arg.argv = NULL;
        arg.argc = 0;
        free(argstr);
        return arg;
    }

    //Process through argstr.
    tmp = argstr;
    int position = 0;
    state_t s;
    s.INQUOTE = 0;
    s.WHITESPACE = 0;
    s.WAITING = 0;
    char* argument;
    arg.argv = (char **)malloc(BUFSIZE * sizeof(char **));
    memset(arg.argv, '\0', BUFSIZE);
    arg.argc = 0;
    if(arg.argv == NULL){
        fprintf(stderr, "Error: malloc() failed. %s.\n",strerror(errno));
        fflush(NULL);
        free(argstr);
        arg.argc = 0;
        return arg;
    }
    if(strlen(argstr) > 0){
        argument = (char *)malloc(BUFSIZE * sizeof(char));
        if(argument == NULL){
            fprintf(stderr, "Error: malloc() failed. %s.\n",strerror(errno));
            fflush(NULL);
            arg.argc = 0;
            free(argstr);
            return arg;
        }
        while(*tmp){
            if(*tmp == '\"' && !(s.INQUOTE)){
                s.INQUOTE = 1;
            }else if(*tmp == '\"'){
                s.INQUOTE = 0;
            }
            if(isspace(*tmp)){
                s.WHITESPACE = 1;
            //Trying to avoid empty args from x "" y
            }else if(*tmp != '\"'){
                s.WHITESPACE = 0;
            }
            if(!(*tmp == '\"')){
                //Normal character. Not in quotes and not waiting from previous whitespace.
                if(!s.INQUOTE && !s.WHITESPACE && !s.WAITING){
                    argument[position++] = *tmp;
                //Normal character. Not in quotes and waiting from previous whitespace.
                }else if(!s.INQUOTE && !s.WHITESPACE && s.WAITING){
                    argument = (char *)malloc(BUFSIZE * sizeof(char));
                    if(argument == NULL){
                        fprintf(stderr, "Error: malloc() failed. %s.\n",strerror(errno));
                        fflush(NULL);
                        for(int i = 0; i < arg.argc; i++){
                            free(arg.argv[i]);
                        }
                        free(arg.argv);
                        arg.argv = NULL;
                        arg.argc = 0;
                        free(argstr);
                        return arg;
                    }
                    argument[position++] = *tmp;
                    s.WAITING = 0;
                //Whitespace. Not in quotes and not waiting from previous whitespace.
                }else if(!s.INQUOTE && s.WHITESPACE && !s.WAITING){
                    argument[position] = '\0';
                    position = 0;
                    arg.argv[arg.argc++] = argument;
                    s.WAITING = 1;
                //Whitespace. Not in quotes and waiting from previous whitespace.
                }else if(!s.INQUOTE && s.WHITESPACE && s.WAITING){
                    //Do nothing.
                //Since whitespace gets added in quotes, disregard whether this is whitespace.
                //However, we do need to know if we are waiting.
                }else if(s.INQUOTE && !s.WAITING){
                    argument[position++] = *tmp;
                }else if(s.INQUOTE && s.WAITING){
                    argument = (char *)malloc(BUFSIZE * sizeof(char));
                    if(argument == NULL){
                        fprintf(stderr, "Error: malloc() failed. %s.\n",strerror(errno));
                        fflush(NULL);
                        for(int i = 0; i < arg.argc; i++){
                            free(arg.argv[i]);
                        }
                        free(arg.argv);
                        free(argstr);
                        arg.argv = NULL;
                        arg.argc = 0;
                        return arg;
                    }
                    argument[position++] = *tmp;
                    s.WAITING = 0;
                //Presumably an impossible situation (all possibilites accounted for). Report it, free already allocated args, and abort. 
                }else{
                    fprintf(stderr, "Error: Impossible situation when parsing argument."
                                    "\n  State:\n   INQUOTE:%d\n   WHITESPACE:%d\n   "
                                    "WAITING:%d",s.INQUOTE,s.WHITESPACE,s.WAITING);
                    fflush(NULL);
                    for(int i = 0; i < arg.argc; i++){
                        free(arg.argv[i]);
                    }
                    free(arg.argv);
                    free(argstr);
                    arg.argv = NULL;
                    arg.argc = 0;
                    return arg;
                }
                //Example states
                //nnn -> each n is 0 or 1, representing the state. First is INQUOTE second is WHITESPACE 3rd is WAITING
                //x represents parts that are irrelevant
                //(.) where . is a char that represents where the reader is
                //($) where $ is an unspecifed non-whitespace non-quote char that represents where the reader is
                //x "x($)x" x - 100
                //x "x( )x" x - 110
                //x ( ) x - 011
                //x( )x - 010 (This would set WAITING, but at the point of reading waiting is not yet set)
                //x ($)x - 001 (This would unset WAITING)
                //x "(") x - 111 (since quotes don't unset WHITESPACE, empty quotes wont trigger a new empty argument. )
            }
            tmp++;
        }
        //Process the last arg
        if(!s.WAITING){
            argument[position] = '\0';
            arg.argv[arg.argc++] = argument;
        }
    }
    free(argstr);
    return arg;
}

//Parses path into a path usable by cd. 
//It is the responsibility of cd to free nxt.
char *parse_path(char *path, struct passwd *pwd, char *cwd){
    //Allocate nxt.
    char *nxt = (char *)malloc(PATH_MAX * sizeof(char));
    if(nxt == NULL){
        fprintf(stderr, "Error: malloc() failed. %s.\n",strerror(errno));
        fflush(NULL);
        return "";
    }

    //If path is all whitespace, process as ~, as its the same as cd without arguments.
    if(strlen(path) == 0){
        strcpy(nxt, pwd->pw_dir);
        int len = strlen(nxt);
        nxt[len] = '/';
        nxt[len + 1] = '\0';
        return nxt;
    }

    //Process the path
    if(strncmp("/",path,1) == 0){
        strcpy(nxt, path);
    }else if(strncmp("~",path,1) == 0 && (strlen(path) == 1 || (strlen(path) > 1 && strncmp("/",path + 1,1) == 0))){
        strcpy(nxt, pwd->pw_dir);
        int len = strlen(nxt);
        nxt[len] = '/';
        nxt[len + 1] = '\0';
        if(strlen(path) > 2){
            strcpy(nxt + len + 1, path + 2);
        }
    }else if(strncmp("/",cwd+strlen(cwd)-1,1) == 0){
        strcpy(nxt, cwd);
        int len = strlen(nxt);
        strcpy(nxt+len, path);
    }
    else{
        strcpy(nxt, cwd);
        int len = strlen(nxt);
        nxt[len] = '/';
        strcpy(nxt + len + 1, path);
    }

    return nxt;
}
