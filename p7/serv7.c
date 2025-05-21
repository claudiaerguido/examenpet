/*
 * serv7.c - Servidor de chat PF_INET TCP
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <pthread.h>

#define MAX_CLIENTES 100
#define MAX_NICK 32
#define MAX_MSG 512
#define PUERTO 12345

typedef struct {
    int socket;
    char nick[MAX_NICK];
} cliente_t;

cliente_t *clientes[MAX_CLIENTES];
pthread_mutex_t clientes_mutex = PTHREAD_MUTEX_INITIALIZER;

void broadcast(char *mensaje, int emisor) {
    pthread_mutex_lock(&clientes_mutex);
    for (int i = 0; i < MAX_CLIENTES; ++i) {
        if (clientes[i] && clientes[i]->socket != emisor) {
            send(clientes[i]->socket, mensaje, strlen(mensaje), 0);
        }
    }
    pthread_mutex_unlock(&clientes_mutex);
}

void *manejador_cliente(void *arg) {
    int sock = *((int *)arg);
    free(arg);
    char nick[MAX_NICK];
    char buffer[MAX_MSG + MAX_NICK + 4];
    int recibido;

    if ((recibido = recv(sock, nick, MAX_NICK, 0)) <= 0) {
        close(sock);
        return NULL;
    }
    nick[recibido] = '\0';

    pthread_mutex_lock(&clientes_mutex);
    for (int i = 0; i < MAX_CLIENTES; ++i) {
        if (clientes[i] && strcmp(clientes[i]->nick, nick) == 0) {
            send(sock, "Nick duplicado\n", 16, 0);
            close(sock);
            pthread_mutex_unlock(&clientes_mutex);
            return NULL;
        }
    }

    cliente_t *cli = malloc(sizeof(cliente_t));
    cli->socket = sock;
    strncpy(cli->nick, nick, MAX_NICK);
    for (int i = 0; i < MAX_CLIENTES; ++i) {
        if (!clientes[i]) {
            clientes[i] = cli;
            break;
        }
    }
    pthread_mutex_unlock(&clientes_mutex);

    snprintf(buffer, sizeof(buffer), "%s se ha unido al chat\n", nick);
    broadcast(buffer, sock);

    while ((recibido = recv(sock, buffer, MAX_MSG, 0)) > 0) {
        buffer[recibido] = '\0';
        char mensaje[MAX_MSG + MAX_NICK + 4];
        snprintf(mensaje, sizeof(mensaje), "%s: %s", nick, buffer);
        broadcast(mensaje, sock);
    }

    close(sock);
    pthread_mutex_lock(&clientes_mutex);
    for (int i = 0; i < MAX_CLIENTES; ++i) {
        if (clientes[i] && clientes[i]->socket == sock) {
            free(clientes[i]);
            clientes[i] = NULL;
            break;
        }
    }
    pthread_mutex_unlock(&clientes_mutex);
    snprintf(buffer, sizeof(buffer), "%s ha salido del chat\n", nick);
    broadcast(buffer, -1);
    return NULL;
}

int main() {
    int servidor, *nuevo_sock;
    struct sockaddr_in direccion;

    servidor = socket(AF_INET, SOCK_STREAM, 0);
    direccion.sin_family = AF_INET;
    direccion.sin_addr.s_addr = INADDR_ANY;
    direccion.sin_port = htons(PUERTO);

    bind(servidor, (struct sockaddr *)&direccion, sizeof(direccion));
    listen(servidor, 10);
    printf("[SERV7] Servidor de chat en puerto %d...\n", PUERTO);

    while (1) {
        socklen_t tam = sizeof(direccion);
        int nuevo = accept(servidor, (struct sockaddr *)&direccion, &tam);
        nuevo_sock = malloc(sizeof(int));
        *nuevo_sock = nuevo;
        pthread_t tid;
        pthread_create(&tid, NULL, manejador_cliente, (void *)nuevo_sock);
        pthread_detach(tid);
    }
    return 0;
}
