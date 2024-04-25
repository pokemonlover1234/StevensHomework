#\
/*******************************************************************************\
 * Name        : makefile\
 * Author      : Aidan Fischer\
 * Date        : 5/4/2021\
 * Description : chatclient makefile\
 * Pledge      : I pledge my honor that I have abided by the Stevens Honor System. \
 ******************************************************************************/

CC      = gcc
TARGET  = chatserver
C_FILES = $(filter-out $(TARGET).c, $(wildcard *.c))
OBJS    = $(patsubst %.c,%.o,$(C_FILES))
CFLAGS  = -g -Wall -Werror -pedantic-errors

all: $(TARGET)
$(TARGET): $(OBJS) $(TARGET).c
	$(CC) $(OBJS) -o $(TARGET) $(TARGET).c
%.o: %.c %.h
	$(CC) $(CFLAGS) -c -o $@ $<
clean:
	rm -f $(OBJS) $(TARGET) $(TARGET).exe
