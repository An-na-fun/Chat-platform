# Assignment 1

## PART A

To run part A:
1. # Run  [server.py] //the host in this file would bind to "" there are two port [webclients:8031] [terminal_clients:8032] the host name and port number is display after running the file
    python3 server.py

2. # To Run webserver [webserver.py] //the host in this file is localhost and the port is [8030] the browser client will connect by entering [localhost:8030]
    python3 webserver.py

3. # To run terminal client [python_client.py] [hostname] [portnumber] [username]

    python3 python_client.py localhost 8032 mill


## PART B 

4. # To run 'c' client [client.c] compile client.c
    clang client.c -o client
   # Then excecute the file by [host] [port] [username] [chat]
   ./client localhost 8030 fun finished te mon