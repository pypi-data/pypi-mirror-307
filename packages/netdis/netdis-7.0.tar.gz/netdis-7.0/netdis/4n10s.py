import socket
import threading

clients = []

def broadcast(message, client):
    for c in clients:
        if c != client:
            try:
                c.send(message)
            except:
                clients.remove(c)

def handle_client(client):
    client.send("Enter your name: ".encode())
    name = client.recv(1024).decode()
    print(f"{name} connected.")
    broadcast(f"{name} has joined the chat!".encode(), client)
    
    while True:
        try:
            message = client.recv(1024)
            if message:
                print(f"{name}: {message.decode()}")
                broadcast(f"{name}: {message.decode()}".encode(), client)
        except:
            clients.remove(client)
            broadcast(f"{name} has left the chat.".encode(), client)
            client.close()
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 55555))
    server.listen(5)
    print("Server started, waiting for clients...")
    
    while True:
        client, address = server.accept()
        print(f"Connection established with {address}")
        

        clients.append(client)
        
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    start_server()
