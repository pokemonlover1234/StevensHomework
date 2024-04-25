#include <pthread.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#define MAX_EXPRS        100
#define QUEUE_LEN        5
#define MAX_STRLEN       16
#define SCALE_FACTOR     1000000
#define NUM_THREAD_PAIRS 20

// Function prototypes
void* consume(void *ptr);
void* produce(void *ptr);
int random_int_in_range(int low, int high, unsigned int *seed);

// Globals
char *queue[QUEUE_LEN];
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t producer_cond = PTHREAD_COND_INITIALIZER;
pthread_cond_t consumer_cond = PTHREAD_COND_INITIALIZER;
int num_occupied = 0, read_index = 0, write_index = 0,
    num_consumed = 0, num_produced = 0;

int random_int_in_range(int low, int high, unsigned int *seed) {
    return low + rand_r(seed) % (high - low + 1);
}

void* consume(void *ptr) {
    //unsigned int seed = (unsigned int)(time(NULL) ^ pthread_self());
    int thread_id = *(int *)ptr,
        count = 0;
    while (count++ < MAX_EXPRS) {
        // Lock the mutex.
        pthread_mutex_lock(&mutex);

        // pthread_cond_wait must be placed in a while loop.
        // pthread_cond_wait atomically unlocks the mutex and waits for the
        // condition variable to be signaled.
        // Unlocking the mutex and suspending on the condition variable is done
        // atomically.
        while (num_occupied <= 0) {
            pthread_cond_wait(&consumer_cond, &mutex);
        }

        int a, b;
        sscanf(queue[read_index], "%d + %d", &a, &b);
        printf("Consumer[%d, %d]: %d + %d = %d\n", thread_id, ++num_consumed,
               a, b, a + b);
        read_index = (read_index + 1) % QUEUE_LEN;
        num_occupied--;

        // Notify the producer that the data has been consumed.
        pthread_cond_signal(&producer_cond);

        // Unlock the mutex.
        pthread_mutex_unlock(&mutex);

        /*
        usleep(
            (useconds_t)random_int_in_range(
                0 * SCALE_FACTOR, 0.5 * SCALE_FACTOR, &seed));
        */
    }
    pthread_exit(NULL);
}

void* produce(void *ptr) {
    unsigned int seed = (unsigned int)(time(NULL) ^ pthread_self());
    int thread_id = *(int *)ptr,
        count = 0;
    while (count++ < MAX_EXPRS) {
        int a = random_int_in_range(0, 9, &seed),
            b = random_int_in_range(0, 9, &seed);

        // Lock the mutex.
        pthread_mutex_lock(&mutex);

        while (num_occupied >= QUEUE_LEN) {
            pthread_cond_wait(&producer_cond, &mutex);
        }

        sprintf(queue[write_index], "%d + %d", a, b);
        printf("Producer[%d, %d]: %s\n", thread_id, ++num_produced,
               queue[write_index]);
        write_index = (write_index + 1) % QUEUE_LEN;
        num_occupied++;

        // Notify the consumer that data is available.
        pthread_cond_signal(&consumer_cond);

        // Unlock the mutex.
        pthread_mutex_unlock(&mutex);

        /*
        usleep(
            (useconds_t)random_int_in_range(
                0 * SCALE_FACTOR, 0.5 * SCALE_FACTOR, &seed));
        */
    }
    pthread_exit(NULL);
}

int main() {
    pthread_t threads[NUM_THREAD_PAIRS * 2];
    int thread_ids[NUM_THREAD_PAIRS * 2], ret_code = EXIT_SUCCESS;

    for (int i = 0; i < QUEUE_LEN; i++) {
        queue[i] = (char *)malloc(sizeof(char) * MAX_STRLEN);
    }

    for (int i = 0; i < NUM_THREAD_PAIRS; i++) {
        thread_ids[i] = i + 1;
        thread_ids[i + NUM_THREAD_PAIRS] = i + 1;

        int retval;
        if ((retval = pthread_create(
                &threads[i], NULL, produce, &thread_ids[i])) != 0) {
            fprintf(stderr, "Error: Cannot create producer thread %d. %s.\n",
                    thread_ids[i], strerror(retval));
            ret_code = EXIT_FAILURE;
            goto EXIT;
        }
        if ((retval = pthread_create(
                &threads[i + NUM_THREAD_PAIRS], NULL, consume,
                &thread_ids[i + NUM_THREAD_PAIRS])) != 0) {
            fprintf(stderr, "Error: Cannot create consumer thread %d. %s.\n",
                    thread_ids[i + NUM_THREAD_PAIRS], strerror(retval));
            ret_code = EXIT_FAILURE;
            goto EXIT;
        }
    }

    // Wait for all threads to finish.
    for (int i = 0; i < NUM_THREAD_PAIRS * 2; i++) {
        pthread_join(threads[i], NULL);
    }

    if (num_occupied != 0) {
        fprintf(stderr, "Error: Something is wrong with your code.\n");
    }

EXIT:
    for (int i = 0; i < QUEUE_LEN; i++) {
        free(queue[i]);
    }
    return ret_code;
}
