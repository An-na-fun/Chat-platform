import sqlite3
import traceback
import json
class ChatDatabase: 
    def __init__(self):
        # path to database
        self.database_path = 'chat.db'
        self._create_chat_table()
        
     
    def _create_chat_table(self):
        # create the chat table if it doesn't exist 
        conn = sqlite3.connect(self.database_path)
        
        try:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chats(
                     username TEXT NOT NULL,
                     message TEXT NOT NULL, 
                     timestamp REAL NOT NULL 
                )    
            """)
            
            conn.commit()
            
        except sqlite3.Error as e:
            print(f"Something happenned with create an new chat table: {e}")
            
        finally:
            conn.close()
    
    
    def insert_chat(self, username, message, timestamp):
        # 
        conn = sqlite3.connect(self.database_path)
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO chats (username, message, timestamp) VALUES(?, ?, ?)", (username, message, timestamp))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Something happenned with inserting an new chat: {e}")
            print("SQLite error details:", e.args)
            traceback.print_exc()
        finally:
            conn.close()
    
    def get_chats(self):
        # 
        conn = sqlite3.connect(self.database_path)
        try:
            retrieve = conn.cursor()
            retrieve.execute("SELECT username, message FROM chats ORDER BY timestamp DESC LIMIT 20")
            chats = retrieve.fetchall()
            result_string = ""
            for row in reversed(chats):
                result_string += ": ".join(map(str, row)) + "\n"
                # print(result_string)
            return result_string
        except sqlite3.Error as e:
            print(f"Something happenned with retrieving chat: {e}")
            return []
        finally:
            conn.close()
            
    def get_chat_time(self, time):
        conn = sqlite3.connect(self.database_path)
        try:
            retrieve = conn.cursor()
            # Adjust the SQL query to filter by timestamp
            retrieve.execute(
                "SELECT username, message, timestamp FROM chats WHERE timestamp > ? ORDER BY timestamp DESC LIMIT 10", 
                (time,)
            )
            chats = retrieve.fetchall()
            
            # Format the results as a list of dictionaries
            chat_list = [
                {"username": row[0], "message": row[1], "timestamp": row[2]}
                for row in reversed(chats)
            ]
            
            # Convert the list to a JSON-formatted string
            return json.dumps(chat_list)
        except sqlite3.Error as e:
            print(f"Something happened with retrieving chat: {e}")
            return json.dumps([])
        finally:
            conn.close()
            
    def get_chat(self, username=None, timestamp=None):
        conn = sqlite3.connect(self.database_path)
        try:
            retrieve = conn.cursor()
            
            # Construct the SQL query dynamically based on the provided filters
            query = "SELECT username, timestamp FROM chats WHERE 1=1"
            params = []
            
            if username:
                query += " AND username = ?"
                params.append(username)
            
            if timestamp:
                query += " AND timestamp = ?"  # Exact match for timestamp
                params.append(timestamp)
            
            query += " ORDER BY timestamp DESC LIMIT 10"  # Limit results to 10
            
            # Execute the query
            retrieve.execute(query, tuple(params))
            chats = retrieve.fetchall()
            
            # Format the results as a list of dictionaries
            chat_list = [
                {"username": row[0], "timestamp": row[1]}
                for row in reversed(chats)
            ]
            
            # Convert the list to a JSON-formatted string
            return json.dumps(chat_list)
        
        except sqlite3.Error as e:
            print(f"Error retrieving chat: {e}")
            return json.dumps([])
        
        finally:
            conn.close()
            


