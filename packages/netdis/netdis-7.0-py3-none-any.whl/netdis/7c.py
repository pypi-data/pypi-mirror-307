import socket

CLIENT_HOST = "localhost"
CLIENT_PORT = 8000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((CLIENT_HOST, CLIENT_PORT))

def call_remote_function(func_name, *args):
    request = f"{func_name} {' '.join(str(arg) for arg in args)}"
    print(f"Client sent function call: {request}")
    client_socket.sendall(request.encode())
    result = client_socket.recv(1024).decode()
    print(f"Client received result: {result}")
    return float(result)

# Example usage
result = call_remote_function('add', 2, 3)
print(f"Final result: {result}")