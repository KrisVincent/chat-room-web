import threading
import socket
import io

class Server:

    def __init__(self,port,server,format = "utf-8"):

        #setting up server
        self.PORT = port
        self.SERVER = server
        self.ADDR = (server,port)
        print(type(self.ADDR))
        
        self.FORMAT = format
        self.DISCONNECT_MSG = "!DISCONNECT"

        #create socket
        self.SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.SERVER.bind(self.ADDR) # must be in tuple when passing server and port

        #this will be used for identifying each individual client
        self.names = []
        
        self.clients = set()
        self.clients_lock = threading.Lock()


    #this is for handling each client (thread)
    def handle_client(self,conn, addr):
        print(f"[NEW CONNECTION] {addr} Connected")
        msg = conn.recv(1024).decode(self.FORMAT)
       

        get_name = msg.split(" ") # string to list to get name
        get_name = get_name[0] #first index is the name

        self.names.append(get_name) # use list to add and remove name 

        self.sendAll(msg)
      
        try:
            connected = True
            

            while connected:
                msg = conn.recv(1024).decode(self.FORMAT)

                if not msg:
                    break

                #this will detect if the disconnect keyword is sent
                if  self.DISCONNECT_MSG in msg.split(" "):
                    self.sendAll(f"{get_name}:{self.DISCONNECT_MSG}")
                    connected = False

                print(f"{msg}")
                self.sendAll(msg)

        #if user disconnects suddenly
        except ConnectionResetError:
           
              print(f"{get_name} has been disconnected..")

        #will remove the current client and sends message to lst_messages
        finally:
            
            with self.clients_lock:
                self.clients.remove(conn)
                self.names.remove(get_name)
            conn.close()
        self.sendAll(f"{get_name} has been disconnected..")

    #this is for sending message
    def sendAll(self, msg):

         with self.clients_lock:
                for c in self.clients:
                    c.sendall(f"{msg}".encode(self.FORMAT))



    def start(self):
        #server will start to listen for incoming clients/connections
        print('[SERVER STARTED]!')
        self.SERVER.listen()
        while True:
            conn, addr = self.SERVER.accept()
           
            with self.clients_lock:
                self.clients.add(conn)
            
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()




      