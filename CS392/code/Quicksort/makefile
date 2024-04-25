#\
/*******************************************************************************\
 * Name        : makefile\
 * Author      : Aidan Fischer\
 * Date        : 2/27/2021\
 * Description : Quicksort makefile for project\
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System. \
 ******************************************************************************/


CC=gcc
CFLAGS = -Wall
DEPS = quicksort.h

%.o : %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

build: quicksort.o sort.o
	$(CC) -o sort sort.o quicksort.o

clean:
	rm sort sort.o quicksort.o