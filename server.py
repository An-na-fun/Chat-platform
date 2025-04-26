import socket
import sys
import select
import traceback
import json
from ChatDatabase import ChatDatabase

websocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# non-blocking, so that select can deal with the multiplexing
websocket.setblocking(False)
hostname = socket.gethostname()
# This accepts a tuple...

websocket.bind(("", 8031))

port = websocket.getsockname()[1]
print("listening on interface " + hostname + " port number is ", port)

websocket.listen()


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setblocking(False)
hostname = socket.gethostname()

serversocket.bind(("", 8032))
port = serversocket.getsockname()[1]
print("listening on interface " + hostname + " port number is ", port)

serversocket.listen()

inputs = [websocket, serversocket]
webclients = []
terminalclients = []



outputs = [] # None

# Chat Database class to store the dat
db = ChatDatabase()

print("waiting for input")
while True: #FOREVAR 
  try:

    
    readable, writable, exceptional = select.select(inputs + webclients + terminalclients, outputs, inputs + webclients + terminalclients)

    # Read what we can, from where we can
    for clientsocket in readable:

      if clientsocket is serversocket:

        conn, addr = serversocket.accept()
        # print('connected by', addr)
        terminalclients.append(conn)
        chats = db.get_chats().encode()   
           
        try:
          conn.sendall(chats)
        except BlockingIOError:
          pass      
      elif clientsocket in terminalclients:

        try:
          
          data = clientsocket.recv(1024)
          
          if not data:  # Empty data indicates client disconnect
            # print('Client disconnected')
            terminalclients.remove(clientsocket)
            clientsocket.close()
            break
          else: 
              data_str = data.decode().strip()
              new_line = data_str.split("\n")
              username, message = new_line[0].split(":")     
              time = new_line[1]                   
              if(message == "quit"):
                # print('Client disconnected')
                webclients.remove(clientsocket)
                clientsocket.close()
              else:
                db.insert_chat(username, message, time)
                
              data_client = f"{username}: {message} "
              # print(data_client)


          for each_client in terminalclients:
            each_client.sendall(data_client.encode())

        except BlockingIOError:
          pass
        
      elif clientsocket is websocket:

        conn, addr = websocket.accept()
        # print('connected by', addr)
        webclients.append(conn)
      
      elif clientsocket in webclients:

        try:
          
          data = clientsocket.recv(1024)
          if not data:  # Empty data indicates client disconnect
            # print('Client disconnected')
            webclients.remove(clientsocket)
            clientsocket.close()
            break
          else: 
                
            data_str = data.decode()
            json_data = json.loads(data_str)
            data_list = list(json_data.items())
            first_key, first_value = data_list[0]
            
            
            if(first_value == "POST"):
              second_key, username = data_list[1]
              third_key, message = data_list[2]  
              fourth_key, timestamp = data_list[3]  
                         
              db.insert_chat(username, message, timestamp)
              
              data_client = f"{username}: {message} "
              
              for each_client in terminalclients:
                each_client.sendall(data_client.encode())
                
            elif(first_value == "GET"):
              # print("Yet to be implemented")
              if(len(data_list) == 2):
                second_key, timestamp = data_list[1]
                
                chat = db.get_chat_time(timestamp)
                chat = json.loads(chat)
                status = ''
                if (chat):
                  status = "data"
                else:
                  status = "none"
                  
                response = {
                  "status": status,  # Change this based on your logic
                  "chat" : chat
                }
                
                clientsocket.sendall(json.dumps(response).encode())
              
              if(len(data_list) == 3):
                second_key, username = data_list[1]
      
                fourth_key, timestamp = data_list[2]
                chat = db.get_chat(username,  timestamp)
                chat = json.loads(chat)
                status = ''
                if (chat):
                  status = "data"
                else:
                  status = "none"

                response = {
                  "status": status,  
                  "chat" : chat
                }
                
                clientsocket.sendall(json.dumps(response).encode())
            
        except BlockingIOError:
          pass


    for clientsocket in exceptional:
        inputs.remove(clientsocket)
        if clientsocket in webclients:
            webclients.remove(clientsocket)
        if clientsocket in terminalclients:
            terminalclients.remove(clientsocket)
        clientsocket.close()

  except KeyboardInterrupt:
    print("I guess I'll just die")
    websocket.close()
    sys.exit(0)
  except Exception as e:
    print("SOMETHING IS BAD")
    print(e)
    traceback.print_exc()

