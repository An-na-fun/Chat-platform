#!/usr/bin/python3

import socket
import select
import sys
import termios
import argparse
import time

parser = argparse.ArgumentParser(description="A script to accept hostname and port.")
    
    # Add arguments for hostname and port
parser.add_argument('hostname', type=str, help='The hostname')
parser.add_argument('port', type=int, help='port number')
parser.add_argument('username', type=str, help='The username')

# Parse the command-line arguments
args = parser.parse_args()
# HOST = "'" + args.arg1 + "'" 

HOST = args.hostname
PORT = args.port
USERNAME = args.username

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's port
try:
    print(HOST, PORT)
    client_socket.connect((HOST, PORT))
      
    print(f"Connected to server hostname:{HOST} port:{PORT}")
except ConnectionRefusedError:
    print(f"Could not connect to server hostname:{HOST} port:{PORT}")
    sys.exit()


client_socket.setblocking(False)
# Canonical mode is "get input when enter is pressed
# I want to read characters immediately!

fd = sys.stdin.fileno()
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON
newattr[3] = newattr[3] & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)



inputs = [sys.stdin, client_socket]
outputs = []

build_str = ""
# term_height = 23
prev_chat = ["\n"]

# Welcome message
print("Welcome back loading messages from server...")

def process_massage(message):
    lines = message.split()
    header = lines[0]
    print(header)
    if(header == "GET"):
        return "I like you Get"
    elif (header == "POST"):
        return "I like you post"
    else :
        return "I like you message"
        
while True:
    # The client will monitor both standard input (stdin) and the socket
    try:
        
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        
        for s in readable:
            if s == client_socket:
  
                server_message = client_socket.recv(1024).decode('utf-8').strip()
                if not server_message:
                    print("Connection closed by server.")
                    # client_socket.close()
                    sys.exit(0)
                else:
                    
                    print(server_message)
                    print(">> "+ build_str, end ="", flush=True)
                    
            else:
                # If the stdin (user input) is ready, read the input
                read_char = sys.stdin.read(1)                                           
                print(read_char, end ="", flush=True)
                build_str = build_str + read_char
                
                if read_char == "\n":
                    build_str =  USERNAME + ":"+ build_str
                    
                    to_send = build_str + str(time.time())
                    # print(build_str)
                    client_socket.send(to_send.encode('utf-8'))
                    build_str = ""
            
    except KeyboardInterrupt:
        print()
        client_socket.close()
        sys.exit(0)
    except Exception as e:
        print("SOMETHING IS BAD")
    # Use select to wait until one of these is ready (stdin or server socket)
    
    

        