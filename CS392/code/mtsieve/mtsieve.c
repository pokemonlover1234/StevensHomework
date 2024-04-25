/*******************************************************************************
 * Name        : mtsieve.c
 * Author      : Aidan fischer
 * Date        : 4/21/2021
 * Description : Segmented sieve with threads
 * Pledge : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdbool.h>
#include <limits.h>
#include <sys/sysinfo.h>
#include <string.h>
#include <unistd.h>
#include <math.h>
#include <time.h>
#include <pthread.h>

typedef struct arg_struct {
    int start;
    int end;
} thread_args;

int total_count = 0;
pthread_mutex_t lock;

void display_usage(char *prog){
    printf("Usage: %s -s <starting value> -e <ending value> -t <num threads>\n",prog);
    return;
}

//Taken from readints.c example program
bool is_integer(char *input) {
    int start = 0, len = strlen(input);

    if (len >= 1 && input[0] == '-') {
        if (len < 2) {
            return false;
        }
        start = 1;
    }
    for (int i = start; i < len; i++) {
        if (!isdigit(input[i])) {
            return false;
        }
    }
    return true;
}

//Assumes input has passed is_integer.
int is_overflow(char *input){
    //Safe to assume max int is less than 64 characters on any system. 
    char max[64];
    int res = sprintf(max, "%ld", input[0] == '-' ? (long)INT_MAX : -(long)INT_MIN);

    if(res < 0){
        //Failed to read system max unsigned int into max. Assume "2147483647"
        strcpy(max, input[0] == '-' ? "2147483647" : "2147483648");
    }
    if(strlen(input)>strlen(max)){
        return true;
    }else if(strlen(input)==strlen(max)){
        int i = 0;
        while(i < strlen(max)){
            if(input[i] > max[i]){
                return true;
            }
            i++;
        }
        return false;
    }else{
        return false;
    }
}

void* segmentsieve(void *ptr){
    thread_args args = *(thread_args *)ptr;
    //Prepare sieve of Eratosthenes for sieving up to sqrt(b)
    int std_sieve_to = (int)floor(sqrt(args.end));
    int *low_primes = (int *)malloc(sizeof(int)*(std_sieve_to));
    for(int i = 0; i < std_sieve_to - 1; i++){
        low_primes[i] = i + 2;
    }
    //Safety terminator for prime searcher in siever.
    low_primes[std_sieve_to - 1] = -1;

    //Efficiently sieve up to sqrt(b)
    int p = 2;
    while(p <= (int)floor(sqrt(std_sieve_to))){
        for(int i = p * p - 2; i < std_sieve_to - 1; i += p){
            low_primes[i] = -1;
        }
        while(low_primes[++p] == -1){}
    }


    bool *high_primes = (bool *)malloc(sizeof(bool)*(args.end - args.start + 1));
    memset(high_primes, true, args.end - args.start + 1);

    for(int i = 0; i < std_sieve_to - 1; i++){
        if(!(low_primes[i] + 1)){
            continue;
        }
        int p = low_primes[i];
        int j = (int)ceil(((double)args.start)/p) * p - args.start;
        if(args.start <= p){
            j += p;
        }
        for(int k = j; k < args.end - args.start + 1; k += p){
            high_primes[k] = false;
        }
    }

    int add = 0;
    for(int i = 0; i < args.end - args.start + 1; i++){
        if(high_primes[i]){
            int tp = i + args.start;
            int num_threes = 0;
            while(tp > 0){
                num_threes += (tp % 10 == 3);
                tp /= 10;
            }
            add += num_threes >= 2;
        }
    }
    int res = pthread_mutex_lock(&lock);
    if(res != 0){
        fprintf(stderr, "Warning: Failed to lock mutex 'lock'. %s.\n",strerror(res));
    }

    total_count += add;

    res = pthread_mutex_unlock(&lock);
    if(res != 0){
        fprintf(stderr, "Warning: Failed to unlock mutex 'lock'. %s.\n",strerror(res));
    }
    free(low_primes);
    free(high_primes);

    pthread_exit(NULL);
}

int main(int argc, char *argv[]){
    if (argc < 3) {
        display_usage(argv[0]);
        return EXIT_FAILURE;
    }

    int opt = 0;
    //Since these are confined by integer limits, LONG_MAX can be used to check if unset.
    long start = LONG_MAX, end = LONG_MAX, num_threads = LONG_MAX;

    int overflow_s;

    while ((opt = getopt(argc, argv, ":s:e:t:")) != -1) {
        switch (opt) {
            case 's':
                optopt = 's';
                if(is_integer(optarg)){
                    overflow_s = is_overflow(optarg);
                    if(overflow_s == 1){
                        fprintf(stderr, "Error: Integer overflow for parameter '-%c'.\n",optopt);
                        return EXIT_FAILURE;
                    }else if(overflow_s == 2){
                        start = -1;
                        break;
                    }
                    start = atoi(optarg);
                }else{
                    fprintf(stderr, "Error: Invalid input '%s' received for parameter '%c'.\n",optarg,optopt);
                    return EXIT_FAILURE;
                } 
                break;
            case 'e':
                optopt = 'e';
                if(is_integer(optarg)){
                    overflow_s = is_overflow(optarg);
                    if(overflow_s == 1){
                        fprintf(stderr, "Error: Integer overflow for parameter '-%c'.\n",optopt);
                        return EXIT_FAILURE;
                    }else if(overflow_s == 2){
                        end = -1;
                        break;
                    }
                    end = atoi(optarg);
                }else{
                    fprintf(stderr, "Error: Invalid input '%s' received for parameter '%c'.\n",optarg,optopt);
                    return EXIT_FAILURE;
                } 
                break;
            case 't':
                optopt = 't';
                if(is_integer(optarg)){
                    overflow_s = is_overflow(optarg);
                    if(overflow_s == 1){
                        fprintf(stderr, "Error: Integer overflow for parameter '-%c'.\n",optopt);
                        return EXIT_FAILURE;
                    }else if(overflow_s == 2){
                        num_threads = -1;
                        break;
                    }
                    num_threads = atoi(optarg);
                }else{
                    fprintf(stderr, "Error: Invalid input '%s' received for parameter '%c'.\n",optarg,optopt);
                    return EXIT_FAILURE;
                } 
                break;
            case '?':
            case ':':
                if (optopt == 'e' || optopt == 's' || optopt == 't'){
                    fprintf(stderr, "Error: Option -%c requires an argument.\n",optopt);
                }else if(isprint(optopt)){
                    fprintf(stderr, "Error: Unknown option '-%c'.\n",optopt);
                }else{
                    fprintf(stderr, "Error: Unknown option character '\\x%x'.\n",optopt);
                }
                return EXIT_FAILURE;
            default:
                return EXIT_FAILURE;
        }
    }

    if(optind < argc){
        fprintf(stderr, "Error: Non-option argument '%s' supplied.\n",argv[optind]);
        return EXIT_FAILURE;
    }

    if(start == LONG_MAX){
        fprintf(stderr, "Error: Required argument <starting value> is missing.\n");
        return EXIT_FAILURE;
    }
    if(start < 2){
        fprintf(stderr, "Error: Starting value must be >= 2.\n");
        return EXIT_FAILURE;
    }

    if(end == LONG_MAX){
        fprintf(stderr, "Error: Required argument <ending value> is missing.\n");
        return EXIT_FAILURE;
    }
    if(end < 2){
        fprintf(stderr, "Error: Ending value must be >= 2.\n");
        return EXIT_FAILURE;
    }
    if(end < start){
        fprintf(stderr, "Error: Ending value must be >= starting value.\n");
        return EXIT_FAILURE;
    }

    if(num_threads == LONG_MAX){
        fprintf(stderr, "Error: Required argument <num threads> is missing.\n");
        return EXIT_FAILURE;
    }
    if(num_threads < 1){
        fprintf(stderr, "Error: Number of threads cannot be less than 1.\n");
        return EXIT_FAILURE;
    }
    if(num_threads > 2 * get_nprocs()){
        fprintf(stderr, "Error: Number of threads cannot exceed twice the number of processors(%d).\n",get_nprocs());
        return EXIT_FAILURE;
    }
    //Calculate how many per thread each thread takes
    int testing = end - start + 1;
    if(testing < num_threads){
        num_threads = testing;
    }
    int each = testing/num_threads;
    int rem = testing - each * num_threads;
    int remr = rem;
    //Note that rem is < num_threads (by definition of remainder). 
    //Therefore the beginning threads each get 1 until the remainder is exhausted.

    int current = start;

    printf("%d segments:\n",(int)num_threads);
    for(int i = 0; i < num_threads; i++){
        printf("   [%d, %d]\n", current, current + each - 1 + (remr > 0));
        current = current + each + (remr > 0);
        --remr;
    }

    current = start;
    remr = rem;

    pthread_mutex_init(&lock, NULL);

    pthread_t *threads = malloc(sizeof(pthread_t) * num_threads);

    //Create segmented sieves. 
    int retval;
    thread_args *args = (thread_args *)malloc(sizeof(thread_args) * num_threads);
    for(int i = 0; i < num_threads; i++){
        args[i].start = current;
        args[i].end = current + each - 1 + (remr > 0);
        current = current + each + (remr > 0);
        remr--;
        if ((retval = pthread_create(&threads[i], NULL, segmentsieve, (void *)&args[i])) != 0) {
            fprintf(stderr, "Error: Cannot create segmenter thread. %s.\n",
                    strerror(retval));
            free(threads);
            free(args);
            return EXIT_FAILURE;
        }
    }
    // Wait for all threads to finish.
    for (int i = 0; i < num_threads; i++) {
        int res = pthread_join(threads[i], NULL);
        if(res != 0){
            fprintf(stderr, "Warning: Failed to join thread %d. %s.\n",i,strerror(res));
        }
    }

    printf("Total primes between %d and %d with two or more '3' digits: %d\n",(int)start,(int)end,total_count);

    int res = pthread_mutex_destroy(&lock);
    if(res != 0){
        fprintf(stderr, "Warning: Failed to destroy mutex 'lock'. %s.\n",strerror(res));
    }

    free(threads);
    free(args);

    return EXIT_SUCCESS;
}