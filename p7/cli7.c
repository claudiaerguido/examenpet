/*
 * cli7.c - Cliente de chat PF_INET TCP
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>

#define MAX_NICK 32
#define MAX_MSG 512
#define PUERTO 12345
#define SERVIDOR "127.0.0.1"

int sockfd;

void *recibir(void *arg) {
    char buffer[MAX_MSG + MAX_NICK + 4];
    int len;
    while ((len = recv(sockfd, buffer, sizeof(buffer)-1, 0)) > 0) {
        buffer[len] = '\0';
        printf("%s", buffer);
        fflush(stdout);
    }
    printf("\n[CLI7] Desconectado del servidor.\n");
    exit(0);
}

int main() {
    struct sockaddr_in server_addr;
    char nick[MAX_NICK];
    char mensaje[MAX_MSG];

    printf("Ingrese su nick: ");
    fgets(nick, MAX_NICK, stdin);
    nick[strcspn(nick, "\n")] = '\0';

    if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("socket");
        return 1;
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PUERTO);
    inet_pton(AF_INET, SERVIDOR, &server_addr.sin_addr);

    if (connect(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("connect");
        return 1;
    }

    send(sockfd, nick, strlen(nick), 0);

    pthread_t recv_thread;
    pthread_create(&recv_thread, NULL, recibir, NULL);

    while (fgets(mensaje, MAX_MSG, stdin)) {
        send(sockfd, mensaje, strlen(mensaje), 0);
    }

    close(sockfd);
    return 0;
}

