/*******************************************************************************
 * Name        : pfind.c
 * Author      : Aidan Fischer
 * Date        : 3/13/2021
 * Description : permstring implementation for project
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System. 
 ******************************************************************************/

#include "permstring.h"
#include <string.h>
#include <sys/stat.h>
#define FALSE 0
#define TRUE 1

//Returns FALSE if permstr is a valid perm string or TRUE if it is invalid
int perm_invalid(char *permstr){
    //Is an invalid perm string if not correct length
    if(strlen(permstr) != 9){
        return TRUE;
    }
    //Loop through the perm string and return true if there is an invalid character.
    for(int i = 0; i < 9; i++){
        switch(permstr[i]){
            case '-':
                break;
            case 'r':
                if(i % 3 != 0){
                    return TRUE;
                }
                break;
            case 'w':
                if(i % 3 != 1){
                    return TRUE;
                }
                break;
            case 'x':
                if(i % 3 != 2){
                    return TRUE;
                }
                break;
            default:
                return TRUE;
        }
    }
    return FALSE;
}

//Returns an integer representing the permstr, assuming permstr is valid
//Ex. rw-r--r-- -> 110100100 = 420
int permstr_to_int(char *permstr){
    int res = 0;
    for(int i = 0; i < 9; i++){
        //Since we receive this when it is already valid, no need to check
        //each perm, just check if they aren't '-'.
        res <<= 1;
        res += (permstr[i] != '-');
    }
    return res;
}

//Takes a mode_t and a permint constucted b permstr_to_int and 
//returns a boolean representing if they match.
int perms[] = {S_IRUSR, S_IWUSR, S_IXUSR,
               S_IRGRP, S_IWGRP, S_IXGRP,
               S_IROTH, S_IWOTH, S_IXOTH};

int permint_matches_stat(mode_t mode, int permint){
    int res = TRUE;
    for(int i = 0; i < 9; i++){
        //Logic is thus: Since booleans are ints (0 is false, 1 is true), track
        //the final result through this. a &= b is equivalent to a = a&b. 
        //Therefore, if the perms differ between permint and mode, the 
        //equivalence check will return false (0) and res will become 0.
        res &= ((mode & perms[i]) == (permint & perms[i]));
    }
    return res;
}