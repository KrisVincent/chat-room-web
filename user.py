import socket
import time



#I created the class for flexibility
class Chatter:

    def __init__(self,port,server,format = "utf-8") -> None:
        
        self.PORT = port
        self.SERVER = server
        self.ADDR = (server, port)
        self.FORMAT = format
        self.DISCONNECT_MESSAGE = "!DISCONNECT"


    def connect(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(self.ADDR)
        return client


    def send(self, client, msg):
        message = msg.encode(self.FORMAT)
        client.send(message)



    def start(self):
    
        name = input("Connected! Now Enter your name!: ")

        connection = self.connect()
        msg = f"{name} has joined!"
        self.send(connection, msg)

        try:
        
            while True:

                msg = input("Message (q for quit): ")

                if msg == self.DISCONNECT_MESSAGE:
                    break
                
                #store messages in msg variable then send it
                msg = f"{name}: {msg}"
                self.send(connection, msg)

        #this error is for when user manually disconnects
        except Exception as e:
            
                print(f"{name} has been disconnected..")     

        
    
        time.sleep(1)

    #this is for the chat box for every client to see
    def chat_box(self):

        connection = self.connect()
        while True:
            msg = connection.recv(1024).decode(self.FORMAT)
            print(msg)
    