/*******************************************************************************
 * Name        : mpsumarrray.c
 * Author      : Aidan fischer
 * Date        : 5/4/2021
 * Description : chatclient project
 * Pledge : I pledge my honor that I have abided by the Stevens Honor System.
 ******************************************************************************/

#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <unistd.h>
#include "util.h"
#include <stdbool.h>

#define EXIT_BYE 2

int client_socket = -1;
char username[MAX_NAME_LEN + 1];
char inbuf[BUFLEN + 1];
char outbuf[MAX_MSG_LEN + 1];

int handle_stdin(){
    int res = get_string(outbuf, MAX_MSG_LEN);
    if(res == TOO_LONG){
        printf("Sorry, limit your message to %d characters.\n", MAX_MSG_LEN);
        return EXIT_SUCCESS;
    }
    if (send(client_socket, outbuf, strlen(outbuf), 0) < 0) {
        fprintf(stderr, "Error: Failed to send message to server. %s.\n",
                strerror(errno));
        return EXIT_FAILURE;
    }
    if(strcmp("bye", outbuf) == 0){
        printf("Goodbye.\n");
        return EXIT_BYE;
    }
    return EXIT_SUCCESS;
}

int handle_client_socket(){
    int bytes_recvd;
    if ((bytes_recvd = recv(client_socket, inbuf, BUFLEN, 0)) < 0) {
        fprintf(stderr, "Warning: Failed to receive incoming message. %s.\n",
                strerror(errno));
        return EXIT_SUCCESS;
    }

    if(bytes_recvd == 0){
        fprintf(stderr, "\nConnection to server has been lost.\n");
        return EXIT_FAILURE;
    }

    inbuf[bytes_recvd] = '\0';

    if(strcmp("bye", inbuf) == 0){
        printf("\nServer initiated shutdown.\n");
        return EXIT_BYE;
    }

    printf("\n%s\n",inbuf);
    return EXIT_SUCCESS;
}

void display_usage(char *name){
    fprintf(stderr, "Usage: %s <server IP> <port>\n", name);
}

int main(int argc, char *argv[]){
    if(argc != 3){
        display_usage(argv[0]);
        return EXIT_FAILURE;
    }

    int bytes_recvd, ip_conversion, retval = EXIT_SUCCESS;
    struct sockaddr_in server_addr;
    socklen_t addrlen = sizeof(struct sockaddr_in);

    memset(&server_addr, 0, addrlen); // Zero out structure

    // Convert character string into a network address.
    ip_conversion = inet_pton(AF_INET, argv[1], &server_addr.sin_addr);
    if (ip_conversion == 0) {
        fprintf(stderr, "Error: Invalid IP address '%s'.\n", argv[1]);
        retval = EXIT_FAILURE;
        goto EXIT;
    } else if (ip_conversion < 0) {
        fprintf(stderr, "Error: Failed to convert IP address. %s.\n",
                strerror(errno));
        retval = EXIT_FAILURE;
        goto EXIT;
    }

    int port;

    bool res = parse_int(argv[2], &port, argv[0]);

    if(!res){
        retval = EXIT_FAILURE;
        goto EXIT;
    }

    if(port < 1024 || port > 65535){
        fprintf(stderr, "Error: Port must be in range [1024, 65535].\n");
        retval = EXIT_FAILURE;
        goto EXIT;
    }  
    
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);

    //Zero out username
    memset(username, '\0', MAX_NAME_LEN + 1);


    int result;
    printf("Enter your username: ");
    fflush(stdout);
    while((result = get_string(username, MAX_NAME_LEN)) == NO_INPUT || result == TOO_LONG){
        memset(username, '\0', MAX_NAME_LEN + 1);
        if(result == TOO_LONG){
            printf("Sorry, limit your username to %d characters.\n", MAX_NAME_LEN);
        }
        printf("Enter your username: ");
        fflush(stdout);
    }
    
    printf("Hello, %s. Let's try to connect to the server.\n",username);

    if ((client_socket = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        fprintf(stderr, "Error: Failed to create socket. %s.\n",
                strerror(errno));
        retval = EXIT_FAILURE;
        goto EXIT;
    }

    if (connect(client_socket, (struct sockaddr *)&server_addr, addrlen) < 0) {
        fprintf(stderr, "Error: Failed to connect to server. %s.\n",
                strerror(errno));
        retval = EXIT_FAILURE;
        goto EXIT;
    }

    if ((bytes_recvd = recv(client_socket, inbuf, BUFLEN, 0)) < 0) {
        fprintf(stderr, "Error: Failed to receive message from server. %s.\n",
                strerror(errno));
        retval = EXIT_FAILURE;
        goto EXIT;
    }

    if(bytes_recvd == 0){
        fprintf(stderr, "All connections are buys. Try again later.\n");
        retval = EXIT_FAILURE;
        goto EXIT;
    }

    printf("\n%s\n\n",inbuf);

    if (send(client_socket, username, strlen(username), 0) < 0) {
        fprintf(stderr, "Error: Failed to send message to server. %s.\n",
                strerror(errno));
        retval = EXIT_FAILURE;
        goto EXIT;
    }

    fd_set sockset;
    int max_socket;

    while(true){
        FD_ZERO(&sockset);
        FD_SET(client_socket, &sockset);
        max_socket = client_socket;

        FD_SET(STDIN_FILENO, &sockset);

        if(STDIN_FILENO > client_socket){
            max_socket = STDIN_FILENO;
        }

        printf("[%s]: ", username);
        fflush(stdout);

        if(select(max_socket + 1, &sockset, NULL, NULL, NULL) < 0 && errno != EINTR){
            fprintf(stderr, "Error: select() failed. %s.\n",strerror(errno));
            retval = EXIT_FAILURE;
            goto EXIT;
        }

        if(FD_ISSET(client_socket, &sockset)){
            int result = handle_client_socket();
            if(result == EXIT_FAILURE){
                retval = EXIT_FAILURE;
                goto EXIT;
            }else if(result == EXIT_BYE){
                retval = EXIT_SUCCESS;
                goto EXIT;
            }
        }

        if(FD_ISSET(STDIN_FILENO, &sockset)){
            int result = handle_stdin();
            if(result == EXIT_FAILURE){
                retval = EXIT_FAILURE;
                goto EXIT;
            }else if(result == EXIT_BYE){
                retval = EXIT_SUCCESS;
                goto EXIT;
            }
        }
    }

    EXIT:
    if (fcntl(client_socket, F_GETFD) >= 0) {
        close(client_socket);
    }
    return retval;
}