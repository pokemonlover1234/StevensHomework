#\
/*******************************************************************************\
 * Name        : makefile\
 * Author      : Aidan Fischer\
 * Date        : 4/11/2021\
 * Description : minishell makefile\
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System. \
 ******************************************************************************/


CC=gcc
CFLAGS = -Wall -Werror -pedantic-errors -g
DEPS = commands.h parsers.h structs.h

%.o : %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

build: commands.o minishell.o parsers.o
	$(CC) -o minishell commands.o parsers.o minishell.o $(CFLAGS)

all: commands.o minishell.o parsers.o
	$(CC) -o minishell commands.o parsers.o minishell.o $(CFLAGS)

clean:
	rm minishell minishell.o commands.o parsers.o

cleano:
	rm minishell minishell.o commands.o parsers.o