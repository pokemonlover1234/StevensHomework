/*******************************************************************************
 * Name        : pfind.c
 * Author      : Aidan Fischer
 * Date        : 3/13/2021
 * Description : permstring header for project
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System. 
 ******************************************************************************/

#ifndef _PERMSTRING__H_
#define _PERMSTRING__H_
#include <sys/types.h>
int perm_invalid(char *permstr);

int permstr_to_int(char *permstr);

int permint_matches_stat(mode_t mode, int permint);
#endif