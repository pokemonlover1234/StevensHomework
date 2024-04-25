CC     = gcc
CFLAGS = -g -Wall -Werror -pedantic-errors

all: main
main: main.c libadd.a
	$(CC) $(CFLAGS) main.c -o main libadd.a
libadd.a: add.o sub.o
	ar rs libadd.a $^
%.o: %.c %.h
	$(CC) $(CFLAGS) -c $<
clean:
	rm -f *.o *.a main main.exe
