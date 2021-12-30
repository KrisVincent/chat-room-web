import socket
import time

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client


def send(client, msg):
    message = msg.encode(FORMAT)
    client.send(message)


def start():
   
    name = input("Connected! Now Enter your name!: ")


    connection = connect()
    msg = f"{name} has joined!"
    send(connection, msg)
    while True:
        msg = input("Message (q for quit): ")

        if msg == 'q':
            break
        
        msg = f"{name}: {msg}"
        send(connection, msg)

    send(connection, DISCONNECT_MESSAGE)
    time.sleep(1)
    print('Disconnected')


start()