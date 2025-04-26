## Project Overview

This project is a simple messaging platform that allows users to send and receive messages both through a web interface and a terminal (command-line) application. It leverages **socket programming** for real-time communication and **multithreading** to handle multiple clients simultaneously.

## Features

- Real-time message sending and receiving
- Web-based and terminal-based interfaces
- Concurrent client handling using multithreading
- Efficient and lightweight communication through sockets

## Technologies Used

- **Python** (for socket programming and threading)
- **HTML/CSS/JavaScript** (for the web front-end)
- **Socket Programming**
- **Multithreading**

## How It Works

- The server listens for incoming connections from both web and terminal clients.
- Each client is managed on a separate thread, allowing multiple users to communicate at the same time.
- Messages are transmitted through sockets in real time.


### Run [server.py]
- The host in this file would bind to `""`.
- There are two ports:
  - **Web clients**: `8031`
  - **Terminal clients**: `8032`
- The hostname and port number are displayed after running the file.

```bash
python3 server.py
```

### To Run webserver [webserver.py]
- The host in this file is `localhost`.
- The port is `8030`.
- The browser client will connect by entering `localhost:8030`.
- Running this file is allows the web client connect to server

```bash
python3 webserver.py
```

### To run terminal client [python_client.py] [hostname] [portnumber] [username]
- Running this file is allows the terminal client connect to server
Example:

```bash
python3 python_client.py localhost 8032 mill
```

---

## To run 'c' client [client.c]:

1. Compile `client.c`:

```bash
clang client.c -o client
```

2. Then execute the file by [host] [port] [username] [chat]:

```bash
./client [host] [port] [username] [chat]
```
