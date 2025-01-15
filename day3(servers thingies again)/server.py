# server side
import socket

HOST = '0.0.0.0'
PORT = 21002

kill_server = False

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    print("Server is running and listening on port", PORT)
except OSError as msg:
    print("Failed to set up server:", msg)
    exit(1)

while not kill_server:
    print("Waiting for a new client to connect...")
    conn, addr = s.accept()
    print("Connection accepted from", addr)

    with conn:
        while True:
            try:
                message_received = ""
                while True:
                    data = conn.recv(32)
                    if data:
                        print("Received data chunk from client:", repr(data))
                        message_received += data.decode()
                        if message_received.endswith("\n"):
                            break
                    else:
                        print("Connection lost!")
                        break

                if message_received:
                    if message_received.strip() == "exit()":
                        print(addr, "disconnected")
                        break

                    print("Received message:", message_received.strip())
                    
                    reply = input("Reply to client: ")
                    if reply.strip() == "kill()":
                        kill_server = True
                        print("Shutting down server...")
                        break
                    elif reply:
                        conn.send(("Server: " + reply + "\n").encode())
                else:
                    break

            except ConnectionResetError:
                print("Client forcibly closed the connection.")
                break

    conn.close()
    print("Connection with", addr, "closed.")

s.close()
print("Server finished")
