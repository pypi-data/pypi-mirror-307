import socket

server_host = '127.0.0.1'
server_port = 65432

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_host, server_port))
server_socket.listen(1)
print("Server is listening for incoming connections...")


conn, addr = server_socket.accept()
print(f"Connected to {addr}")

file_name = conn.recv(1024).decode() 
print(f"Receiving file: {file_name}")

received_file_name = 'received_file'

with open(received_file_name, 'wb') as file:
    while True:
        data = conn.recv(1024)
        if not data:
            break
        file.write(data)

print(f"File has been saved as '{received_file_name}'.")
conn.close()
server_socket.close()
