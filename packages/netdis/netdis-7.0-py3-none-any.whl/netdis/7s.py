import socket

SERVER_HOST = "localhost"
SERVER_PORT = 8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

print(f"Server is listening on {SERVER_HOST}:{SERVER_PORT}")

def add(a, b):
    return a + b

def handle_client(conn):
    try:
        # Receive the function call request
        data = conn.recv(1024)
        function_name, *args = data.decode().split()
        print(f"Server received function call: {function_name}({', '.join(args)})")

        # Execute the function and get the result
        result = globals()[function_name](*(int(arg) for arg in args))
        print(f"Server executed function and got result: {result}")

        # Send the result back to the client
        conn.sendall(str(result).encode())
        print("Server sent result to client")

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        conn.close()

def receive():
    while True:
        client, address = server_socket.accept()
        print(f'Server connected with {str(address)}')
        handle_client(client)

print("Server is running and listening...")
receive()