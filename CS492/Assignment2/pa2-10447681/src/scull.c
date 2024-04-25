#define _GNU_SOURCE
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <sched.h>
#include <sys/wait.h>
#include <pthread.h>

#include "scull.h"

#define CDEV_NAME "/dev/scull"

#define STACK_SIZE 0x5000000

/* Quantum command line option */
static int g_quantum;

static void usage(const char *cmd)
{
	printf("Usage: %s <command>\n"
	       "Commands:\n"
	       "  R          Reset quantum\n"
	       "  S <int>    Set quantum\n"
	       "  T <int>    Tell quantum\n"
	       "  G          Get quantum\n"
	       "  Q          Query quantum\n"
	       "  X <int>    Exchange quantum\n"
	       "  H <int>    Shift quantum\n"
	       "  h          Print this message\n",
	       cmd);
}

typedef int cmd_t;

// Create a stack necessary for clone() calls. 
// I wanted to try using clone instead of fork(), 
// to have fun.

static void * create_stack(){
	void * ptr = malloc(STACK_SIZE);
	if(ptr == NULL){
		perror("Memory failed to allocate");
	}
	return ptr + STACK_SIZE;
}

// The function that calls IOCIQUANTUM in clone 
// Need to provide do_op signature here, due to
// function definition cross-dependency
static int do_op(int fd, cmd_t cmd);
static int do_IQUANTUM(void * fd){
	do_op(*(int *)fd, 'i');
	do_op(*(int *)fd, 'i');
	return 0;
}

// Because pthread is annoying, need a seperate 
// version of the same function above with a 
// different signature and return method. 
static void * do_IQUANTUM_thr(void * fd){
	do_op(*(int *)fd, 'i');
	do_op(*(int *)fd, 'i');
	pthread_exit(NULL);
	return NULL;
}


static cmd_t parse_arguments(int argc, const char **argv)
{
	cmd_t cmd;

	if (argc < 2) {
		fprintf(stderr, "%s: Invalid number of arguments\n", argv[0]);
		cmd = -1;
		goto ret;
	}

	/* Parse command and optional int argument */
	cmd = argv[1][0];
	switch (cmd) {
	case 'S':
	case 'T':
	case 'H':
	case 'X':
		if (argc < 3) {
			fprintf(stderr, "%s: Missing quantum\n", argv[0]);
			cmd = -1;
			break;
		}
		g_quantum = atoi(argv[2]);
		break;
	case 'R':
	case 'G':
	case 'Q':
	case 'h':
	case 'i':
	case 'p':
	case 't':
		break;
	default:
		fprintf(stderr, "%s: Invalid command\n", argv[0]);
		cmd = -1;
	}

ret:
	if (cmd < 0 || cmd == 'h') {
		usage(argv[0]);
		exit((cmd == 'h')? EXIT_SUCCESS : EXIT_FAILURE);
	}
	return cmd;
}

static int do_op(int fd, cmd_t cmd)
{
	int ret, q, status, i, pid, j;
	// Create the stacks for the p command.
	// Create an array for them, as well
	// an array for pthread stuff.
	void * s1 = create_stack();
	void * s2 = create_stack();
	void * s3 = create_stack();
	void * s4 = create_stack();
	void * s[4] = {s1, s2, s3, s4};
	pthread_t threads[4];
	task_info taskinf;
	switch (cmd) {
	case 'R':
		ret = ioctl(fd, SCULL_IOCRESET);
		if (ret == 0)
			printf("Quantum reset\n");
		break;
	case 'Q':
		q = ioctl(fd, SCULL_IOCQQUANTUM);
		printf("Quantum: %d\n", q);
		ret = 0;
		break;
	case 'G':
		ret = ioctl(fd, SCULL_IOCGQUANTUM, &q);
		if (ret == 0)
			printf("Quantum: %d\n", q);
		break;
	case 'T':
		ret = ioctl(fd, SCULL_IOCTQUANTUM, g_quantum);
		if (ret == 0)
			printf("Quantum set\n");
		break;
	case 'S':
		q = g_quantum;
		ret = ioctl(fd, SCULL_IOCSQUANTUM, &q);
		if (ret == 0)
			printf("Quantum set\n");
		break;
	case 'X':
		q = g_quantum;
		ret = ioctl(fd, SCULL_IOCXQUANTUM, &q);
		if (ret == 0)
			printf("Quantum exchanged, old quantum: %d\n", q);
		break;
	case 'H':
		q = ioctl(fd, SCULL_IOCHQUANTUM, g_quantum);
		printf("Quantum shifted, old quantum: %d\n", q);
		ret = 0;
		break;
	case 'i':
		ret = ioctl(fd, SCULL_IOCIQUANTUM, &taskinf);
		if (ret == 0)
			printf("state %ld, stack 0x%lx, cpu %u, prio %d, sprio %d, nprio %d, rtprio %u, pid %d, tgid %d, nv %lu, niv %lu\n", taskinf.state, (unsigned long)taskinf.stack, taskinf.cpu, taskinf.prio, taskinf.static_prio, taskinf.normal_prio, taskinf.rt_priority, taskinf.pid, taskinf.tgid, taskinf.nvcsw, taskinf.nivcsw);
		break;
	case 'p':
		ret = 0;
		for(i = 0; i < 4; i++){
			// Check validity of stacks
			if(s[i] - STACK_SIZE == NULL){
				ret = -1;
				perror("Failed to create a stack");
				break;
			}
			// Create the child. SIGCHLD necessary for wait to work.
			pid = clone(&do_IQUANTUM, s[i], SIGCHLD, (void *)&fd);
			if(pid == -1){
				ret = -1;
				perror("Clone: Failed to create child");
				break;
			}
		}
		for(i = 0; i < 4; i++){
			j = wait(&status);
			if(j == -1){
				perror("Error when waiting");
			}
		}
		// Make sure output is printed.
		fflush(stdout);
		break;
	case 't':
		// clone has this annoying, but justified, behavior
		// of setting thread's parents to the parent of the 
		// caller, so wait doesn't work. I tried to get it
		// to work for this, but I just gave up and used pthread.
		ret = 0;
		for(i = 0; i < 4; i++){
			ret = pthread_create(&threads[i], NULL, do_IQUANTUM_thr, (void *)&fd);
			if(ret != 0){
				perror("Failed to create thread");
			}
		}
		for(i = 0; i < 4; i++){
			j = pthread_join(threads[i], NULL);
			if(j != 0){
				perror("Error when waiting");
			}
		}
		fflush(stdout);
		break;

	default:
		/* Should never occur */
		abort();
		ret = -1; /* Keep the compiler happy */
	}

	if (ret != 0)
		perror("ioctl");
	return ret;
}

int main(int argc, const char **argv)
{
	int fd, ret;
	cmd_t cmd;

	cmd = parse_arguments(argc, argv);

	fd = open(CDEV_NAME, O_RDONLY);
	if (fd < 0) {
		perror("cdev open");
		return EXIT_FAILURE;
	}

	printf("Device (%s) opened\n", CDEV_NAME);

	ret = do_op(fd, cmd);

	if (close(fd) != 0) {
		perror("cdev close");
		return EXIT_FAILURE;
	}

	printf("Device (%s) closed\n", CDEV_NAME);

	return (ret != 0)? EXIT_FAILURE : EXIT_SUCCESS;
}
