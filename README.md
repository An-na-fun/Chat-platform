# Chat-platform

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
