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

def send_msg(sock, msg):
    msg_encoded = msg.encode()
    msg_length = len(msg_encoded)
    msg_length_encoded = msg_length.to_bytes(4, 'big')
    sock.sendall(msg_length_encoded)
    sock.sendall(msg_encoded)

def recv_msg(sock):
    msg_length_encoded = sock.recv(4)
    if not msg_length_encoded:
        return None
    msg_length = int.from_bytes(msg_length_encoded, 'big')
    msg_encoded = sock.recv(msg_length)
    return msg_encoded.decode()

while True:
    command = input("PS> ")
    if command.lower() == "exit":
        break
    send_msg(client_socket, command)
    output = recv_msg(client_socket)
    print(output)

client_socket.close()
