#\
/*******************************************************************************\
 * Name        : makefile\
 * Author      : Aidan Fischer\
 * Date        : 3/13/2021\
 * Description : pfind makefile for project\
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System. \
 ******************************************************************************/


CC=gcc
CFLAGS = -Wall -Werror -pedantic-errors -O3
DEPS = precurse.h permstring.h

%.o : %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

build: pfind.o precurse.o permstring.o
	$(CC) -o pfind pfind.o precurse.o permstring.o $(CFLAGS)

clean:
	rm pfind pfind.o precurse.o permstring.o
