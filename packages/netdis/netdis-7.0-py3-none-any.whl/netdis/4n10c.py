import socket
import threading


def receive_message(client):
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except:
            print("Error receiving message.")
            client.close()
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 55555)) 
    
    name = input("Enter your name: ")
    client.send(name.encode())
    
    thread = threading.Thread(target=receive_message, args=(client,))
    thread.start()

    while True:
        message = input("Message:")
        if message.lower() == 'exit':
            client.send(f"{name} has left the chat.".encode())
            client.close()
            break
        client.send(message.encode())

if __name__ == "__main__":
    start_client()
