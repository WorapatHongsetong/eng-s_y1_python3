# Client side
import socket
import threading

HOST = 'localhost'
PORT = 21001

def send_message_function(client_socket):
    while True:
        message = input("Enter a message: ")
        client_socket.send((message + "\n").encode())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected to server")

    send_thread = threading.Thread(target=send_message_function, args=(s,))
    send_thread.start()

    while True:
        # message = input("Enter a message: ")
        # s.send((message+"\n").encode())
        
        message_received = ""

        while True:
            data = s.recv(32)
            if data:
                print('Received data chunk from server: ', repr(data))
                message_received += data.decode()
                if message_received.endswith("\n"):
                    print(message_received)
                    print("End of message received")
                    break
            else:
                print("Connection lost!")
                break
        if not message_received:
            break

print("Client finished")