#\
/*******************************************************************************\
 * Name        : makefile\
 * Author      : Aidan Fischer\
 * Date        : 3/31/2021\
 * Description : spfind makefile\
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System. \
 ******************************************************************************/



CC     = gcc
C_FILE = $(wildcard *.c)
TARGET = $(patsubst %.c,%,$(C_FILE))
CFLAGS = -g -Wall -Werror -pedantic-errors

all:
	$(CC) $(CFLAGS) $(C_FILE) -o $(TARGET)
clean:
	rm -f $(TARGET) $(TARGET).exe
