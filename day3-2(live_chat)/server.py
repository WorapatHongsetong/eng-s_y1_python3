import socket
import threading

HOST = ''
PORT = 21002

clients = []

def broadcast(message, sender_address, sender_socket=None):
    formatted_message = f"[{sender_address}]: {message.decode()}"
    for client in clients:
        if client != sender_socket:  
            try:
                client.send(formatted_message.encode())
            except Exception as e:
                print(f"[ERROR] Could not send message to a client: {e}")
                clients.remove(client)
                client.close()

def handle_client(client_socket, client_address):
    print(f"[NEW CONNECTION] {client_address} connected.")
    clients.append(client_socket)
    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"[{client_address}] {message.decode().strip()}")
            broadcast(message, sender_address=client_address, sender_socket=client_socket)
    except Exception as e:
        print(f"[ERROR] Connection with {client_address} ended: {e}")
    finally:
        print(f"[DISCONNECTED] {client_address}")
        clients.remove(client_socket)
        client_socket.close()

def start_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen()
        print(f"[LISTENING] Server is running and listening on port {PORT}")
    except Exception as e:
        print(f"[ERROR] Failed to set up server: {e}")
        return

    while True:
        client_socket, client_address = server.accept()
        print(f"[CONNECTION] Accepted connection from {client_address}")
        
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
