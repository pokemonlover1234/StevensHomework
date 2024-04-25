/*
 * main.c -- the bare scull char module
 *
 * Copyright (C) 2001 Alessandro Rubini and Jonathan Corbet
 * Copyright (C) 2001 O'Reilly & Associates
 *
 * The source code in this file can be freely used, adapted,
 * and redistributed in source or binary form, so long as an
 * acknowledgment appears in derived source files.  The citation
 * should list that the code comes from the book "Linux Device
 * Drivers" by Alessandro Rubini and Jonathan Corbet, published
 * by O'Reilly & Associates.   No warranty is attached;
 * we cannot take responsibility for errors or fitness for use.
 *
 */

#include <linux/module.h>
#include <linux/moduleparam.h>
#include <linux/init.h>

#include <linux/kernel.h>	/* printk() */
#include <linux/slab.h>		/* kmalloc() */
#include <linux/fs.h>		/* everything... */
#include <linux/errno.h>	/* error codes */
#include <linux/types.h>	/* size_t */
#include <linux/cdev.h>

#include <linux/uaccess.h>	/* copy_*_user */

#include <linux/mutex.h> /* for mutexes */

#include "scull.h"		/* local definitions */
#include "access_ok_version.h"

/*
 * Our parameters which can be set at load time.
 */

static int scull_major =   SCULL_MAJOR;
static int scull_minor =   0;
static int scull_quantum = SCULL_QUANTUM;

module_param(scull_major, int, S_IRUGO);
module_param(scull_minor, int, S_IRUGO);
module_param(scull_quantum, int, S_IRUGO);

MODULE_AUTHOR("Aidan Fischer");
MODULE_LICENSE("Dual BSD/GPL");

static struct cdev scull_cdev;		/* Char device structure		*/

/*
 * Globals related to linked list for IOCIQUANTUM, 
 * that is, the list itself and a mutex
 */

ti_linked_list * ti_ll;
static DEFINE_MUTEX(list_lock);

/*
 * Functions for management of task info linked list
 */

// Returns true if added, false if not added (i.e. duplicate.)

static bool add_if_not_duplicate(ti_linked_list * list, ti_node * new){
	ti_node * curnode;
	if(list->head == NULL){
		list->head = new;
		list->tail = new;
		return true;
	}
	curnode = list->head;
	while(curnode != NULL){
		if(new->pid == curnode->pid && new->tgid == curnode->tgid){
			return false;
		}
		curnode = curnode->next;
	}
	// New node not added as head, and isn't a duplicate. Add to end
	new->prev = list->tail;
	list->tail->next = new;
	list->tail = new;
	return true;
}

// Removes node from list, and frees it from memory
// Supports removing any node, even though we'll only
// ever remove the head here.

static void free_node(ti_linked_list * list, ti_node * node){
	if(node == list->head){
		list->head = node->next;
	}
	if(node == list->tail){
		list->tail = node->prev;
	}
	if(node->prev != NULL){
		node->prev->next = node->next;
	}
	if(node->next != NULL){
		node->next->prev = node->prev;
	}
	kfree(node);
}

/*
 * Open and close
 */

static int scull_open(struct inode *inode, struct file *filp)
{
	printk(KERN_INFO "scull open\n");
	return 0;          /* success */
}

static int scull_release(struct inode *inode, struct file *filp)
{
	printk(KERN_INFO "scull close\n");
	return 0;
}

/*
 * The ioctl() implementation
 */

static long scull_ioctl(struct file *filp, unsigned int cmd,
		unsigned long arg)
{

	int err = 0, tmp;
	int retval = 0;
    task_info taskinf;
	ti_node * newnode;

	/*
	 * extract the type and number bitfields, and don't decode
	 * wrong cmds: return ENOTTY (inappropriate ioctl) before access_ok()
	 */
	if (_IOC_TYPE(cmd) != SCULL_IOC_MAGIC) return -ENOTTY;
	if (_IOC_NR(cmd) > SCULL_IOC_MAXNR) return -ENOTTY;

	/*
	 * the direction is a bitmask, and VERIFY_WRITE catches R/W
	 * transfers. `Type' is user-oriented, while
	 * access_ok is kernel-oriented, so the concept of "read" and
	 * "write" is reversed
	 */
	if (_IOC_DIR(cmd) & _IOC_READ)
		err = !access_ok_wrapper(VERIFY_WRITE, (void __user *)arg,
				_IOC_SIZE(cmd));
	else if (_IOC_DIR(cmd) & _IOC_WRITE)
		err =  !access_ok_wrapper(VERIFY_READ, (void __user *)arg,
				_IOC_SIZE(cmd));
	if (err) return -EFAULT;

	switch(cmd) {

	case SCULL_IOCRESET:
		scull_quantum = SCULL_QUANTUM;
		break;
        
	case SCULL_IOCSQUANTUM: /* Set: arg points to the value */
		retval = __get_user(scull_quantum, (int __user *)arg);
		break;

	case SCULL_IOCTQUANTUM: /* Tell: arg is the value */
		scull_quantum = arg;
		break;

	case SCULL_IOCGQUANTUM: /* Get: arg is pointer to result */
		retval = __put_user(scull_quantum, (int __user *)arg);
		break;

	case SCULL_IOCQQUANTUM: /* Query: return it (it's positive) */
		return scull_quantum;

	case SCULL_IOCXQUANTUM: /* eXchange: use arg as pointer */
		tmp = scull_quantum;
		retval = __get_user(scull_quantum, (int __user *)arg);
		if (retval == 0)
			retval = __put_user(tmp, (int __user *)arg);
		break;

	case SCULL_IOCHQUANTUM: /* sHift: like Tell + Query */
		tmp = scull_quantum;
		scull_quantum = arg;
		return tmp;
	
	case SCULL_IOCIQUANTUM:
		//Update taskinf struct with information from current, then copy to userspace
		taskinf.state = current->state;
		taskinf.stack = current->stack;
		taskinf.cpu = current->cpu;
		taskinf.prio = current->prio;
		taskinf.static_prio = current->static_prio;
		taskinf.normal_prio = current->normal_prio;
		taskinf.rt_priority = current->rt_priority;
		taskinf.pid = current->pid;
		taskinf.tgid = current->tgid;
		taskinf.nvcsw = current->nvcsw;
		taskinf.nivcsw = current->nivcsw;
		retval = __copy_to_user((void __user *)arg, (const void *)&taskinf, sizeof(task_info));
		// Update the linked list storing the processes that have called the "i" command.
		newnode = (ti_node *)kmalloc(sizeof(ti_node), GFP_KERNEL);
		if(newnode == NULL){
			printk(KERN_ERR "scull::IOCIQUANTUM - Failed to allocate memory for new node. Not storing.\n");
			break;
		}
		newnode->next = NULL;
		newnode->prev = NULL;
		newnode->pid = taskinf.pid;
		newnode->tgid = taskinf.tgid;
		// List is not used before this point, so 
		// now lock the mutex and try adding the node.
		mutex_lock(&list_lock);
		if(!add_if_not_duplicate(ti_ll, newnode)){
			free_node(ti_ll, newnode);
		}
		mutex_unlock(&list_lock);
		break;

	default:  /* redundant, as cmd was checked against MAXNR */
		return -ENOTTY;
	}
	return retval;

}


struct file_operations scull_fops = {
	.owner =    THIS_MODULE,
	.unlocked_ioctl = scull_ioctl,
	.open =     scull_open,
	.release =  scull_release,
};

/*
 * Finally, the module stuff
 */

/*
 * The cleanup function is used to handle initialization failures as well.
 * Thefore, it must be careful to work correctly even if some of the items
 * have not been initialized
 */
void scull_cleanup_module(void)
{
	int count = 1;
	dev_t devno = MKDEV(scull_major, scull_minor);
	//Print gathered info from IQUANTUM to kernel log and clean up the linked list
	mutex_lock(&list_lock);
	if(ti_ll != NULL && ti_ll->head != NULL){
		while(ti_ll->head != NULL){
			printk(KERN_INFO "Task %d: PID %u, TGID %u\n", count, ti_ll->head->pid, ti_ll->head->tgid);
			free_node(ti_ll, ti_ll->head);
			count++;
		}
	}
	//kfree on NULL is safe, no need to check.
	kfree(ti_ll);
	mutex_unlock(&list_lock);
	
	/* Get rid of the char dev entry */
	cdev_del(&scull_cdev);

	/* cleanup_module is never called if registering failed */
	unregister_chrdev_region(devno, 1);
}


int scull_init_module(void)
{
	int result;
	dev_t dev = 0;

	/*
	 * Get a range of minor numbers to work with, asking for a dynamic
	 * major unless directed otherwise at load time.
	 */
	if (scull_major) {
		dev = MKDEV(scull_major, scull_minor);
		result = register_chrdev_region(dev, 1, "scull");
	} else {
		result = alloc_chrdev_region(&dev, scull_minor, 1, "scull");
		scull_major = MAJOR(dev);
	}
	if (result < 0) {
		printk(KERN_WARNING "scull: can't get major %d\n", scull_major);
		return result;
	}

	cdev_init(&scull_cdev, &scull_fops);
	scull_cdev.owner = THIS_MODULE;
	result = cdev_add (&scull_cdev, dev, 1);
	/* Fail gracefully if need be */
	if (result) {
		printk(KERN_NOTICE "Error %d adding scull character device", result);
		goto fail;
	}

	// Initialize task_info linked list

	mutex_lock(&list_lock);

	ti_ll = (ti_linked_list *)kmalloc(sizeof(ti_linked_list), GFP_KERNEL);
	ti_ll->head = NULL;
	ti_ll->tail = NULL;

	mutex_unlock(&list_lock);

	return 0; /* succeed */

  fail:
	scull_cleanup_module();
	return result;
}

module_init(scull_init_module);
module_exit(scull_cleanup_module);
