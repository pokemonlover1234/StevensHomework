#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define SCALE_FACTOR 1000000

int num_running = 0;
pthread_mutex_t lock;

int random_int_in_range(int low, int high) {
    return low + rand() % (high - low + 1);
}

void *sleep_print(void *ptr) {
    int thread_num = *(int *)ptr;
    long tid = (long)pthread_self();
    srand((time(NULL) & 0xFFFF) | (tid << 16));

    useconds_t sleep_time = 
        (useconds_t)random_int_in_range(1 * SCALE_FACTOR, 5 * SCALE_FACTOR);
    printf("I, thread %d, am going to sleep for %.2f seconds.\n", thread_num,
           (double)sleep_time / SCALE_FACTOR);
    usleep(sleep_time);
    printf("I, thread %d, have finished.\n", thread_num);

    int retval;
    if ((retval = pthread_mutex_lock(&lock)) != 0) {
        fprintf(stderr, "Warning: Cannot lock mutex. %s.\n",
                strerror(retval));
    }
    num_running--;
    if ((retval = pthread_mutex_unlock(&lock)) != 0) {
        fprintf(stderr, "Warning: Cannot unlock mutex. %s.\n",
                strerror(retval));
    }
    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage %s <num_threads>\n", argv[0]);
        return EXIT_FAILURE;
    }
    int num_threads = atoi(argv[1]);
    if (num_threads <= 0) {
        fprintf(stderr, "Error: Invalid number of threads '%s'.\n", argv[1]);
        return EXIT_FAILURE;
    }

    pthread_t *threads;
    if ((threads = (pthread_t *)
                       malloc(num_threads * sizeof(pthread_t))) == NULL) {
        fprintf(stderr, "Error: Cannot allocate memory for threads.\n");
        return EXIT_FAILURE;
    }

    int *thread_nums;
    if ((thread_nums = (int *)malloc(num_threads * sizeof(int))) == NULL) {
        free(threads);
        fprintf(stderr, "Error: Cannot allocate memory for thread args.\n");
        return EXIT_FAILURE;
    }

    int retval;
    if ((retval = pthread_mutex_init(&lock, NULL)) != 0) {
        fprintf(stderr, "Error: Cannot create mutex. %s.\n", strerror(retval));
        free(threads);
        free(thread_nums);
        return EXIT_FAILURE;
    }

    // Create independent threads.
    int num_started = 0;
    for (int i = 0; i < num_threads; i++) {
        thread_nums[i] = i + 1;
        if ((retval = pthread_create(&threads[i], NULL, sleep_print,
                                     (void *)(&thread_nums[i]))) != 0) {
            fprintf(stderr, "Error: Cannot create thread %d. "
                            "No more threads will be created. %s.\n",
                            i + 1, strerror(retval));
            break;
        }
        num_started++;
        if ((retval = pthread_mutex_lock(&lock)) != 0) {
            fprintf(stderr, "Warning: Cannot lock mutex. %s.\n",
                    strerror(retval));
        }
        num_running++;
        if ((retval = pthread_mutex_unlock(&lock)) != 0) {
            fprintf(stderr, "Warning: Cannot unlock mutex. %s.\n",
                    strerror(retval));
        }
    }
    
    // Wait until threads are complete before main continues. If we don't wait,
    // we run the risk of executing an exit, which will terminate the process
    // and all threads before the threads have completed.
    for (int i = 0; i < num_started; i++) {
        if (pthread_join(threads[i], NULL) != 0) {
            fprintf(stderr, "Warning: Thread %d did not join properly.\n",
                    thread_nums[i]);
        }
    }

    printf("Num threads started: %d\nThreads still running: %d\n",
           num_started, num_running);

    free(threads);
    free(thread_nums);

    if ((retval = pthread_mutex_destroy(&lock)) != 0) {
        fprintf(stderr, "Warning: Cannot destroy mutex. %s.\n",
                strerror(retval));
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
