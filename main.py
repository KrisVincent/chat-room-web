import threading
import socket
import time

class Server:

    def __init__(self,port,server,format = "utf-8"):
        #setting up server
        self.port = port
        self.server = server
        
        self.format = format
        self.disconnect_msg = "!DISCONNECT"

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server.bind((server,port)) # must be in tuple when passing server and port

        self.names = []

        self.clients = set()
        self.clients_lock = threading.Lock()

    def handle_client(self,conn, addr):
        print(f"[NEW CONNECTION] {addr} Connected")
        msg = conn.recv(1024).decode(self.format)

        get_name = msg.split(" ") # string to list to get name
        get_name = get_name[0] #first index is the name

        self.names.append(get_name) # use list to add and remove name 

        try:
            connected = True
            while connected:
                msg = conn.recv(1024).decode(self.format)

                if not msg:
                    break

                if msg == self.disconnect_msg:
                    connected = False

                print(f"{msg}")
                with self.clients_lock:
                    for c in self.clients:
                        c.sendall(f"[{addr}] {msg}".encode(self.format))

                


        finally:
            print(self.names)
            print(get_name)
            with self.clients_lock:
                self.clients.remove(conn)
                self.names.remove(get_name)
            conn.close()

    def start(self):
        print('[SERVER STARTED]!')
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            with self.clients_lock:
                self.clients.add(conn)
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

    #below codes are for the client side\

    