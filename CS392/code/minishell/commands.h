/*******************************************************************************
 * Name        : precurse.h
 * Author      : Aidan Fischer
 * Date        : 4/11/2021
 * Description : commands header for minishell 
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System. 
 ******************************************************************************/

#include "structs.h"

#ifndef _COMMANDS__H_
#define _COMMANDS__H_

struct argsdata;
typedef struct argsdata arg_t;

int cd(char *path, char *cwd);

#endif