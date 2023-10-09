import select
import socket
import sys
import threading
import subprocess
import os

# Configuration
HOST = '0.0.0.0'
PORT = 8080
shutdown_flag = False  # Flag for graceful shutdown

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server is listening on {HOST}:{PORT}")

#line 19
def send_msg(sock, msg):
    msg_encoded = msg.encode()
    msg_length = len(msg_encoded)
    msg_length_encoded = msg_length.to_bytes(4, 'big')
    sock.sendall(msg_length_encoded)
    sock.sendall(msg_encoded)

#line 27
def recv_msg(sock):
    msg_length_encoded = sock.recv(4)
    if not msg_length_encoded:
        return None
    msg_length = int.from_bytes(msg_length_encoded, 'big')
    msg_encoded = sock.recv(msg_length)
    return msg_encoded.decode()

#line 36
def handle_client(client_socket):
    working_dir = os.getcwd()
    while True:
        try:
            command = recv_msg(client_socket)
            if not command:
                break

            if command.startswith("cd "):
                try:
                    new_dir = os.path.join(
                        working_dir, command.split(' ', 1)[1])
                    os.chdir(new_dir)
                    working_dir = os.getcwd()
                    response = f"Changed directory to {working_dir}"
                except Exception as e:
                    response = f"Error changing directory: {e}"
            else:
                result = subprocess.run(
                    ['powershell', '-NoProfile', '-Command', command], cwd=working_dir, capture_output=True, text=True)
                response = result.stdout + result.stderr
                if not response:
                    response = "Command executed with no output."

            send_msg(client_socket, response)

        except socket.error as e:
            print(f"Socket error: {e}")
            break

    client_socket.close()

#line 69
def listen_for_exit_command():
    global shutdown_flag
    while True:
        user_input = input(
            "Type 'exit' to shut down the server: ").strip().lower()
        if user_input == "exit":
            shutdown_flag = True
            print("\nShutting down the server...")
            break

# Start the input listener thread (add around Line 80)
input_thread = threading.Thread(target=listen_for_exit_command)
input_thread.daemon = True  # So that this thread will exit when the main program exits
input_thread.start()


# line 86
try:
    while not shutdown_flag:
        # Check if there's a client trying to connect
        readable, _, _ = select.select([server_socket], [], [], 1)  # Line 89

        if server_socket in readable:
            client_socket, _ = server_socket.accept()               # Line 91
            client_thread = threading.Thread(
                target=handle_client, args=(client_socket,))       # Line 93
            client_thread.start()
finally:
    server_socket.close() 