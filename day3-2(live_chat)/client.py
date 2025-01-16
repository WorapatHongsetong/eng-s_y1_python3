import socket
import threading

HOST = 'localhost'  
PORT = 21002

def send_message(client_socket):
    while True:
        try:
            message = input("Enter message: ")
            if message.lower() == "exit()":
                print("Disconnecting...")
                client_socket.send(message.encode())
                break
            client_socket.send((message + "\n").encode())
        except Exception as e:
            print(f"[ERROR] Sending message failed: {e}")
            break

def receive_message(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                print("[SERVER CLOSED CONNECTION]")
                break
            print(message.strip())
        except Exception as e:
            print(f"[ERROR] Receiving message failed: {e}")
            break

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print("[CONNECTED] Connected to server")

        send_thread = threading.Thread(target=send_message, args=(client_socket,))
        receive_thread = threading.Thread(target=receive_message, args=(client_socket,))

        send_thread.start()
        receive_thread.start()

        send_thread.join()
        receive_thread.join()

        print("[DISCONNECTED] Client disconnected")
