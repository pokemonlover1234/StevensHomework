#include <linux/module.h>
#include <linux/init.h>
#include <linux/sched.h>
#include <asm/current.h>
static int hello_name_init(void){
	printk(KERN_INFO "Hello World from Aidan Fischer (10447681)\n");
	return 0;
}

static void hello_name_exit(void){
	printk(KERN_INFO "PID = %i; NAME = %s\n", current->pid, current->comm);
}
module_init(hello_name_init);
module_exit(hello_name_exit);
MODULE_LICENSE("Dual BSD/GPL");
