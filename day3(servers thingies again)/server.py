# server side

import socket
import sys
from pyexpat.errors import messages

HOST = '0.0.0.0'
PORT = 21002
s = None

kill_server = False

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created")
except OSError as msg:
    s = None
    print(f"Error creating socket: {msg}")
    exit(1)

try:
    s.bind((HOST, PORT))
    s.listen()
    print("Socket bound and listening")
except OSError as msg:
    print("Error binding/listening!")
    s.close()
    exit(1)

conn, addr = s.accept()
with conn:
    print('Connection accepted from ', addr)

    while True:
        message_received = ""
        while True:
            data = conn.recv(32)
            if data:
                print('Received data chunk from client: ', repr(data))
                message_received += data.decode()
                if message_received.endswith("\n"):
                    break
            else:
                print("Connection lost!")
                break

        if message_received:
            if message_received.endswith("exit()\n"):
                print(addr, "disconnected")
                break

            print("Received message: ", message_received)
            # conn.send(("Server summarized: " + message_received[:10] + "\n").encode())

            reply = input("Reply to client: ")
            if reply == "kill()":
                kill_server = True
            elif reply:
                conn.send(("Server: " + reply + "\n").encode())

        else:
            break

s.close()
print("Server finished")