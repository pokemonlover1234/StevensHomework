/*******************************************************************************
 * Name        : precurse.h
 * Author      : Aidan Fischer
 * Date        : 4/11/2021
 * Description : parsers header for minishell 
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System. 
 ******************************************************************************/

#include "structs.h"
#include <pwd.h>

#ifndef _PARSERS__H_
#define _PARSERS__H_

struct argsdata;
typedef struct argsdata arg_t;

arg_t parse_args(char *args);
char *parse_path(char *path, struct passwd *pwd, char *cwd);

#endif