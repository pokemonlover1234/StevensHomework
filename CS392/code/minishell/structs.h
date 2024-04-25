/*******************************************************************************
 * Name        : precurse.h
 * Author      : Aidan Fischer
 * Date        : 4/11/2021
 * Description : structs header for minishell 
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System. 
 ******************************************************************************/

#ifndef _STRUCTS__H_
#define _STRUCTS__H_
#define BUFSIZE 4096

struct argsdata {
    char **argv;
    int argc;
};

struct statedata {
    unsigned int INQUOTE:1;
    unsigned int WHITESPACE:1;
    unsigned int WAITING:1;
};

#endif