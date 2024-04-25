#include <linux/kernel.h>
#include <linux/syscalls.h>
#include <linux/uaccess.h>

SYSCALL_DEFINE1(aidan_syscall, __user char*, inp){
	//Checks if the pointer is null, if it's not safe to read/write to the memory at that pointer if it isn't null, and if the length of the string at that address is longer than 32, including null terminator. If any of these are true, then return -1.
	int repl = 0;
	size_t size;
	char str[32];
	int i;
	int failed_bytes;
	if (inp == NULL || !access_ok(VERIFY_WRITE, inp, strnlen_user(inp, 32)) || strnlen_user(inp, 32) > 32){
		printk(KERN_WARNING "aidan_syscall::invalid string pointer passed to function. Either null, unsafe to write to, or too long.\n");
		return -1;
	}
	size = strnlen_user(inp, 32);
	//Should return size - 1 if successful, since it returns size of string NOT including trailing NUL if it succeeds.
	if(strncpy_from_user(str, inp, size) != size - 1){
		printk(KERN_WARNING "aidan_syscall::failed to copy full string from userspace.\n");
		return -1;
	}
	printk(KERN_WARNING "before:%s\n", str);
	for(i = 0; i < size; i++){
		char c = str[i];
		if(c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u' || c == 'y'){
			str[i] = 'X';
			repl++;
		}
	}
	printk(KERN_WARNING "after:%s\n", str);
	failed_bytes = copy_to_user((void __user *)inp, (const void *)str, size);
	if(failed_bytes != 0){
		printk(KERN_WARNING "aidan_syscall::failed to copy full string to userspace. Failed to copy %d bytes.\n", failed_bytes);
		return -1;
	}
	return repl;
}
