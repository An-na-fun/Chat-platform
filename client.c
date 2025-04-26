#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netdb.h>

void send_request(int client_socket, const char *request) {
    ssize_t n = write(client_socket, request, strlen(request));
    assert(n >= 0 && "Failed to send request");
}

void receive_response(int client_socket, char *response, size_t size) {
    ssize_t n = read(client_socket, response, size - 1);
    assert(n >= 0 && "Failed to receive response");
    response[n] = '\0';
}

int connect_to_server(const char *host, int port) {
    struct hostent *server = gethostbyname(host);
    assert(server != NULL && "Failed to resolve host");

    int client_socket = socket(AF_INET, SOCK_STREAM, 0);
    assert(client_socket >= 0 && "Failed to create socket");

    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    memcpy(&server_addr.sin_addr.s_addr, server->h_addr, server->h_length);

    int conn_status = connect(client_socket, (struct sockaddr *)&server_addr, sizeof(server_addr));
    assert(conn_status >= 0 && "Failed to connect to server");

    return client_socket;
}

char* post_message(const char *host, int port, const char *username, const char *message) {
    int client_socket = connect_to_server(host, port);

    int content_length = strlen(username) + strlen(message) + 30;

    char request[1024];
    snprintf(request, sizeof(request), 
             "POST /api/message HTTP/1.1\r\n"
             "Host: localhost\r\n"
             "Content-Type: application/json\r\n"
             "Cookie: username=%s\r\n"
             "Content-Length: %d\r\n\r\n"
             "{\"username\":\"%s\", \"message\":\"%s\"}",
             username, content_length, username, message);

    send_request(client_socket, request);

    char response[1024];
    receive_response(client_socket, response, sizeof(response));
    printf("Posting message on the server, assert fails if user is not logged in\n");
    assert(strstr(response, "200 OK") != NULL && "POST failed");
    printf("Message successfully posted\n");

    char *timestamp_start = strstr(response, "\"timestamp\": \"");
    if (timestamp_start != NULL) {
        timestamp_start += strlen("\"timestamp\": \"");
        static char timestamp[50];
        int i = 0;
        while (timestamp_start[i] != '\"' && timestamp_start[i] != '\0') {
            timestamp[i] = timestamp_start[i];
            i++;
        }
        timestamp[i] = '\0';
        close(client_socket);
        return timestamp;
    } else {
        printf("Timestamp not found in the response.\n");
        close(client_socket);
        return NULL;
    }
}

void get_message(const char *host, int port, const char *username, const char *timestamp) {
    int client_socket = connect_to_server(host, port);

    char request[1024];
    snprintf(request, sizeof(request),
             "GET /api/messages?username=%s&timestamp=%s HTTP/1.1\r\n"
             "Host: %s\r\n"
             "Cookie: username=%s\r\n\r\n",
             username, timestamp, host, username);

    send_request(client_socket, request);

    char response[1024];
    receive_response(client_socket, response, sizeof(response));
    assert(strstr(response, "200 OK") != NULL && "GET failed");
    printf("Message confirmed to be posted\n");

    close(client_socket);
}

int main(int argc, char *argv[]) {
    if (argc < 5) {
        fprintf(stderr, "Usage: %s [host] [port] [username] [message...]\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    const char *host = argv[1];
    int port = atoi(argv[2]);
    const char *username = argv[3];

    size_t message_len = 0;
    for (int i = 4; i < argc; i++) {
        message_len += strlen(argv[i]) + 1;
    }

    char *message = malloc(message_len);
    if (message == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
    }

    message[0] = '\0';
    for (int i = 4; i < argc; i++) {
        strcat(message, argv[i]);
        if (i < argc - 1) strcat(message, " ");
    }

    char *timestamp = post_message(host, port, username, message);
    if (timestamp == NULL) {
        printf("Failed to get timestamp. Exiting.\n");
        free(message);
        return 1;
    }

    get_message(host, port, username, timestamp);

    printf("All assertions passed.\n");
    free(message);
    return 0;
}
