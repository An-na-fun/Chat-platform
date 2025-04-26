import json
import socket
import threading
import sys
import argparse
import time



WEB_HOST = "localhost"

            
WEB_PORT = 8030              # Arbitrary non-privileged port

HOST = "localhost"
PORT = 8031

# Content length
# 
# 
current_user = []

page = '''<html>
<head>

    <style>
        #chatpage_container{
            display: none;
        }
        
        #homepage{
            display: block;
        }

        #endchat_container{
            display: none;
        }
        
        
    </style>
    
    <script>
        let lastMessageTimestamp = 0;
        let pollingInterval = null;
        
        
        function post_message(){
            
            const user_message = document.getElementById("message").value;
            const username = document.getElementById("username").value;
            console.log(user_message);
            if(!user_message) {
                return;
            }
            
            const req =  new XMLHttpRequest();
            req.open('POST', '/api/message', true);
            
            req.setRequestHeader('Content-Type', 'application/json');
            req.withCredentials = true;
            
            req.onload = function(){
                console.log('I am here');
                if(req.status === 200){
                    const data = JSON.parse(req.responseText);
                    console.log(data);
                    if (!pollingInterval) {
                        pollingInterval = setInterval(get_messages, 5000); // Poll every 5 seconds
                    }
                    display_messages(username, user_message, data.timestamp);
                    console.log('I am here');
                    
                    
                    
                } else {
                    console.error("Error with status:", req.status);
                }
            }
            req.send(JSON.stringify({ username: username, message: user_message }));

        }
    
        function get_messages(){
            const req = new XMLHttpRequest();
            req.open('GET', `/api/messages?timestamp=${lastMessageTimestamp}`, true);
            
            req.setRequestHeader('Content-Type', 'application/json');
            req.withCredentials = true;
            
            req.onload = function() {
                if (req.status === 200) {
                    const messages = JSON.parse(req.responseText);
                    
                    console.log(messages);
                    if(messages.status === "data") {
                        const read_chat = messages.chat;
                        
                        read_chat.forEach((read_message) => {
                            console.log(read_message.username, read_message.message, read_message.timestamp);
                            display_messages(read_message.username, read_message.message, read_message.timestamp);
                        });
                    }
                    
                } else {
                    console.error("Error fetching new messages:", req.status);
                }
            };
            
            req.send();
        }
        
        function display_messages(username, user_message, timestamp){
            const messagesBody = document.getElementById("messages_body");
    
            // Create a new row for the message
            const row = document.createElement("tr");
            
            // Create a cell for the message content
            const messageCell = document.createElement("td");
            messageCell.classList.add("username");
            messageCell.textContent = username;
            
            // Create a cell for the username
            const usernameCell = document.createElement("td");
            usernameCell.classList.add("user_message");
            usernameCell.textContent = user_message;
            
            
            const timestampCell = document.createElement("td");
            timestampCell.classList.add("timestamp");
            timestampCell.textContent = timestamp;
            
            lastMessageTimestamp = timestamp;
            console.log(lastMessageTimestamp);
            // Append the cells to the row
            row.appendChild(messageCell);
            row.appendChild(usernameCell);
            row.appendChild(timestampCell);
            // Append the row to the table body
            messagesBody.appendChild(row);
        }
        
        
        
        function login_user(){
            
            const user_name = document.getElementById("username").value;
            name = user_name;
            console.log(user_name);
            if(!user_name) {
                return;
            }
            
            const req =  new XMLHttpRequest();
            req.open('POST', '/api/login', true);
            
            req.setRequestHeader('Content-Type', 'application/json');
            req.withCredentials = true;
            
            req.onload = function(){
                console.log('I am here');
                if(req.status === 200){
                    const data = JSON.parse(req.responseText);
                    console.log('I am here');
                    if(data.success){
                        const div1 = document.getElementById("homepage");
                        const div2 = document.getElementById("chatpage_container");
                        div1.style.display = "none";
                        div2.style.display = "block";
                    }else{
                        alert("Login failed!");
                    }
                } else {
                    console.error("Error with status:", req.status);
                }
            }
            req.send(JSON.stringify({ username: user_name }));

        }
        
        function logout_user() {
            const req = new XMLHttpRequest();
            req.open('DELETE', '/api/login', true);
            
            req.onload = function() {
                if (req.status === 200) {
                    const data = JSON.parse(req.responseText);
                    console.log(data);
                    // Hide the chat page and show the homepage
                    const div1 = document.getElementById("homepage");
                    const div2 = document.getElementById("chatpage_container");
                    div1.style.display = "block";
                    div2.style.display = "none";
                    
                    // Clear the username and message inputs
                    
                    document.getElementById("username").value = "";
                    document.getElementById("message").value = "";
                    
                    
                } else {
                    console.error("Error logging out:", req.status);
                }
            };
            
            req.send();
        }        
        
        
        
        document.addEventListener("DOMContentLoaded", function() {
            document.getElementById("login").addEventListener('click', login_user);
            document.getElementById("send_message").addEventListener('click', post_message);
            document.getElementById("logout").addEventListener('click', logout_user);
        });
        
        
    </script>
</head>


<body>

<div id="homepage">
    <h3>Welcome to Discordn't</h3>
    <p>Enter your name and login to join the chat </p>

    <div id = "login-container">
        <input type="username" id="username" name="username">
        <button type="button" id="login"> login </button>
    </div>
</div>

<div id="chatpage_container" >
    <p>What's on you mind? <input type="message" id="message" name="message">  </p> 
    <br>
    <button type="button" id= "send_message"> Send message! </button>
    <button type="button"  id= "logout"> Log out! </button>
    <div id="messagescontainer> 
    </div>
    
</div>

<div id="messagescontainer">
    <table id="messages_table" border="1" style="width: 75%;">
        <thead>
            <tr>
                <th style="width: 15%;">Message</th>
                <th style="width: 35%;">Username</th>
                <th id="timestamp" style ="width: 35%;"> Timestamp</th>
            </tr>
        </thead>
        <tbody id="messages_body">
            <!-- Messages will be dynamically inserted here -->
        </tbody>
    </table>
</div>
</body>
</html>
  

</body>
</html>
'''

error_page = '''<html>
<body>
<h3> On the wrong side of discordn't retrace your steps</h3>
<p> Go to login page and login to see or post messages </p>
</body>
</html>
'''
header = """HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: {}

"""
error_header = """HTTP/1.1 400 Bad Request
Content-Type: text/html
Content-Length: {}

"""

counter = -1

def reply(conn):
    try:
        print('Connected by', addr)
        # formattedPage = page.format(counter)
        replyHeader = header.format(len(page))
        conn.sendall(replyHeader.encode())
        conn.sendall(page.encode())
        
    except KeyboardInterrupt:
        print("I guess I'll just die")
        conn.close()
        



def handle_clients(conn, addr):
    try:
        request = conn.recv(1024).decode()
        

        if request:
            method, path, body, cookies = parse_request(request)
            cookie_username = ""
            if "username=" in cookies:
                cookie_username = cookies.split("username=")[1].split(";")[0]
            # Check for valid session cookie for restricted endpoints
           
            
            
            if path == "/":
                # current_user = "index"
                reply(conn)
                
            
            elif path == "/api/login" and method == "POST":
                # Login logic
                data = json.loads(body)
                username = data.get("username")
                
                
                
                if username:
                    response = {
                        "success": True,
                        "message": "Login successful"
                    }
                    json_response = json.dumps(response)
                    
                    reply_header = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: application/json\r\n"
                        f"Set-Cookie: username={username}; Path=/; HttpOnly\r\n"
                        f"Content-Length: {len(json_response)}\r\n\r\n"
                    )
                    current_user.append(username)
                    
                    conn.sendall(reply_header.encode())
                    conn.sendall(json_response.encode())
                else:
                    send_error(conn, 400, "Username required")
            
            elif path == "/api/login" and method == "DELETE":
                
                
                response = {
                    "success": True,
                    "message": "Logout successful"
                }
                json_response = json.dumps(response)
                reply_header = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: application/json\r\n"
                    "Set-Cookie: username=""; Max-Age=0; Path=/; HttpOnly\r\n"
                    f"Content-Length: {len(json_response)}\r\n\r\n"
                )
                conn.sendall(reply_header.encode())
                conn.sendall(json_response.encode())
            
            elif path == "/api/message" and method == "POST":
                # Restrict access to logged-in users only
                if (current_user != [] and cookie_username ==current_user[-1]):
          
                    # print(current_user)
                    current_time = str(time.time())
                    add_timestamp = {"timestamp": current_time}
                    data = json.loads(body)
                    new_message = {**data, **add_timestamp}
                    send_message(conn, json.dumps(new_message))
                    
                    response = {
                        "success": True,
                        "message": "Message sent",
                        "timestamp": current_time
                    }
                    json_response = json.dumps(response)
                    reply_header = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: application/json\r\n"
                        f"Content-Length: {len(json_response)}\r\n\r\n{json_response}"
                    )
                    conn.sendall(reply_header.encode())
            
                else:
                    send_error(conn, 401, "Unauthorized: Login required")
                    return
            elif path.startswith("/api/messages") and method == "GET":
               
                if (current_user != [] and cookie_username == current_user[-1]):
                    _, query = path.split("?")
                    # print(query)
                    if('&' in query):
                       first, second = query.split("&")
                       _, user_name = first.split("=")
                       _, timestamp = second.split("=")
                      
                       confirm_message(conn, user_name,  timestamp)
                    else:
                        _, time_data = query.split("=")
                        get_message(conn, time_data)
            
                   
                else: 
                    send_error(conn, 401, "Unauthorized: Login required")
            elif path == "/images.html" and method == "GET":
                
                file_path = "files/images.html"
                try:
                    with open(file_path, "r") as file:
                        content = file.read()
                        reply_header = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/html\r\n"
                        f"Content-Length: {len(content)}\r\n\r\n"
                        )
                        conn.sendall(reply_header.encode())
                        conn.sendall(content.encode())
                except FileNotFoundError:
                    
                    print("Error: images.html file not found")
                    
            elif path == "/images/f.jpeg" and method == "GET":
                
                file_path = "files/images/f.jpeg"
                try:
                    with open(file_path, "rb") as file:
                        content = file.read()
                        reply_header = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/html\r\n"
                        f"Content-Length: {len(content)}\r\n\r\n"
                        )
                        conn.sendall(reply_header.encode())
                        conn.sendall(content)
                except FileNotFoundError:
                    
                    print("Error: images.html file not found")
            elif path == "/images/code.jpeg" and method == "GET":
                
                file_path = "files/images/code.jpeg"
                try:
                    with open(file_path, "rb") as file:
                        content = file.read()
                        reply_header = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/html\r\n"
                        f"Content-Length: {len(content)}\r\n\r\n"
                        )
                        conn.sendall(reply_header.encode())
                        conn.sendall(content)
                except FileNotFoundError:
                    
                    print("Error: images.html file not found")
                    
            elif path == "/images/binary.jpeg" and method == "GET":
                
                file_path = "files/images/binary.jpeg"
                try:
                    with open(file_path, "rb") as file:
                        content = file.read()
                        reply_header = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/html\r\n"
                        f"Content-Length: {len(content)}\r\n\r\n"
                        )
                        conn.sendall(reply_header.encode())
                        conn.sendall(content)
                except FileNotFoundError:
                    
                    print("Error: images.html file not found")
            elif path == "/test.html" and method == "GET":
                
                file_path = "files/test.html"
                try:
                    with open(file_path, "r") as file:
                        content = file.read()
                        reply_header = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/html\r\n"
                        f"Content-Length: {len(content)}\r\n\r\n"
                        )
                        conn.sendall(reply_header.encode())
                        conn.sendall(content.encode())
                except FileNotFoundError:
                    
                    print("Error: images.html file not found")
            elif path == "/link.html" and method == "GET":
                
                file_path = "files/link.html"
                try:
                    with open(file_path, "r") as file:
                        content = file.read()
                        reply_header = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/html\r\n"
                        f"Content-Length: {len(content)}\r\n\r\n"
                        )
                        conn.sendall(reply_header.encode())
                        conn.sendall(content.encode())
                except FileNotFoundError:
                    
                    print("Error: images.html file not found")
            elif path == "/folder/turtle.html" and method == "GET":
                
                file_path = "files/folder/turtle.html"
                try:
                    with open(file_path, "r") as file:
                        content = file.read()
                        reply_header = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/html\r\n"
                        f"Content-Length: {len(content)}\r\n\r\n"
                        )
                        conn.sendall(reply_header.encode())
                        conn.sendall(content.encode())
                except FileNotFoundError:
                    
                    print("Error: images.html file not found")
            
            else:
                print(path)
                reply_header = error_header.format(len(error_page))
                conn.sendall(reply_header.encode())
                conn.sendall(error_page.encode())
                
    except Exception as e:
        print("Exception in handle_clients:", e)
    finally:
        conn.close()



def confirm_message(conn, user_name, timestamp):
    # Establish connection to the backend server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as backend_conn:
        try:
            backend_conn.connect((HOST, PORT))
            
            # Send request with `last` parameter to the backend server
            request_data = json.dumps({"method": "GET", "name": user_name, "time": timestamp})
            backend_conn.sendall(request_data.encode())

            # Receive response from the backend server
            response_data = backend_conn.recv(4096).decode()
            
            # print(response_data)
            messages = json.loads(response_data)
            # Format and send response back to the client
            json_response = json.dumps(messages)
            reply_header = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(json_response)}\r\n\r\n{json_response}"
            conn.sendall(reply_header.encode())
        except Exception as e:
            print(e)


def get_message(conn, last_timestamp):
    # Establish connection to the backend server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as backend_conn:
        try:
            backend_conn.connect((HOST, PORT))
            
            # Send request with `last` parameter to the backend server
            request_data = json.dumps({"method": "GET", "last": last_timestamp})
            backend_conn.sendall(request_data.encode())

            # Receive response from the backend server
            response_data = backend_conn.recv(4096).decode()
            
            # print(response_data)
            messages = json.loads(response_data)
            # Format and send response back to the client
            json_response = json.dumps(messages)
            reply_header = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(json_response)}\r\n\r\n{json_response}"
            conn.sendall(reply_header.encode())
        except Exception as e:
            print(e)
        

        
def send_message(conn, body):
    try:
        if(body):
            data = json.loads(body)
            message = data.get("message")
            print()
            if not message:
                send_error(conn, 400, "Bad Request: 'message' is required")

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as chat_conn:
                try:
                    message_type = {"method": "POST"}
                    to_send = {**message_type, **data}
                    chat_conn.connect((HOST, PORT))
                    chat_conn.sendall(json.dumps(to_send).encode())
                except Exception as e:
                    print(e)

  
    except json.JSONDecodeError:
        send_error(conn, 400, "Bad Request: Invalid JSON format")
    except Exception as e:
        send_error(conn, 500, f"Internal Server Error: {str(e)}")
        

    
def parse_request(request):
    header, _, body = request.partition("\r\n\r\n")
    lines = header.split("\r\n")
    request_line = lines[0]
    method, path, version = request_line.split(" ")
    
    # Extract cookies from headers
    headers = {line.split(": ")[0]: line.split(": ")[1] for line in lines[1:] if ": " in line}
    cookies = headers.get("Cookie", "")
    return method, path, body, cookies


def send_error(conn, status_code, message):
    response = "HTTP/1.1 {} {}\r\nContent-Type: text/plain\r\n\r\n{}".format(status_code, message, message)
    conn.sendall(response.encode())
    
    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((WEB_HOST, WEB_PORT))

    s.listen()
    
    while True:
        try:
            conn, addr = s.accept()
            # print('Connected by', addr)
            myThread = threading.Thread(target=handle_clients, args=(conn, addr))
            myThread.run()
        except KeyboardInterrupt:
            print("I guess I'll just die")
            sys.exit()
            conn.close()