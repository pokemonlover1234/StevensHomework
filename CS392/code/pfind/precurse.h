/*******************************************************************************
 * Name        : precurse.h
 * Author      : Aidan Fischer
 * Date        : 3/13/2021
 * Description : precurse header file for project
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System. 
 ******************************************************************************/

#ifndef _PRECURSE__H_
#define _PRECURSE__H_
#include <dirent.h>

void pdir(DIR *dir, int perm, char *rootpath);

#endif