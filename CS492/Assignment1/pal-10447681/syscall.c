#define _GNU_SOURCE

#include <unistd.h>
#include <stdio.h>
#include <sys/syscall.h>


#define Aidan_SYSCALL 548

int main(int argc, char *argv[]){
	char str1[] = "adkasdfkakdfaadajeoprawiruoiawfanvoaphiapoefwaoefjwaffa";
	char str2[] = "abcdefghijklmnopqrstuvwxyz";
	printf("OLD str1:%s\n", str1);
	long res1 = syscall(Aidan_SYSCALL, str1);
	printf("str1 syscall res: %ld\n", res1);
	printf("NEW str1:%s\n", str1);
	printf("OLD str2:%s\n", str2);
	long res2 = syscall(Aidan_SYSCALL, str2);
	printf("str2 syscall res: %ld\n", res2);
	printf("NEW str2:%s\n", str2);
}
