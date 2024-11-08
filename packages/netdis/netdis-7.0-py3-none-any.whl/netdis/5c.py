import socket

server_host = '127.0.0.1'
server_port = 65432
file_path = 'file_to_send.txt' 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))

file_name = file_path.split('/')[-1]
client_socket.send(file_name.encode())

with open(file_path, 'rb') as file:
    while chunk := file.read(1024):
        client_socket.send(chunk)

print(f"File '{file_name}' has been sent.")
client_socket.close()
