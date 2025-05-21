# Makefile para chat cliente-servidor

CC = gcc
CFLAGS = -Wall -pthread

all: serv7 cli7

serv7: serv7.c
	$(CC) $(CFLAGS) serv7.c -o serv7

cli7: cli7.c
	$(CC) $(CFLAGS) cli7.c -o cli7

clean:
	rm -f serv7 cli7


all:
	@echo "Compilación y ejecución de la práctica"

clean:
	@echo "Limpiando..."
