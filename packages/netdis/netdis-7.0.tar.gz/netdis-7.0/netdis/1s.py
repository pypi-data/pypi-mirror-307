import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 65432))  
server_socket.listen(1)
print("Server is waiting for a connection...")

conn, addr = server_socket.accept()
print(f"Connected by {addr}")

data = conn.recv(1024)  
if data:
    print(f"Received from client: {data.decode()}")
    conn.sendall(data) 

conn.close()
server_socket.close()
