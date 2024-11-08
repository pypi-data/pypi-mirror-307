import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 65432))  

message = "Hello, Server!"
client_socket.sendall(message.encode())
print(f"Sent to server: {message}")

data = client_socket.recv(1024)
print(f"Received from server: {data.decode()}")

client_socket.close()
