import socket

HOST = '192.168.1.201'  # Change to your server's IP address
PORT = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((HOST, PORT))
except socket.error as e:
    print(f"Error connecting to the server: {e}")
    exit(1)

print("Connected to the server. Enter your commands below:")
print("Enter 'exit' to close the connection.")

while True:
    command = input("PS> ")
    
    if command.lower() == "exit":
        break

    client_socket.send(command.encode())
    output = client_socket.recv(4096).decode()
    print(output)

client_socket.close()
