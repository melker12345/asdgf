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

def handle_client(client_socket):
    working_dir = os.getcwd()  # Always initialize working_dir

    while True:
        try:
            command = client_socket.recv(1024).decode()

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

            client_socket.send(response.encode())

        except socket.error as e:
            print(f"Socket error: {e}")
            break
        except Exception as e:
            response = f"Server error: {e}"
            client_socket.send(response.encode())  # Send error back to client without terminating the server
            break

    client_socket.close()


while True:
    client_socket, _ = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()




'''
My current overview of what to do next

    - Making sure the command gets sent and received correctly 
        - What happens if a packet is lost? 
            - I don't fully understand how the program handles this currently.
            - Client should be informed and the server should not run the command

            
    - Ability to exit the server script just like the client script
        - Simply mirror how the client script does it 

    - Print the received command on server
        - It would be useful to keep track of what commands the client has sent to the server 
            either by printing it to terminal or by creating a file for every session created
            (I dont know which is best)  


    - Adding the ability to connect from another network 
        - This step is important for the main idea of the project but introduces the highest security risk 
            which is why I will integrate this the last thing I do 
            (ignore this for now unless you have some good input on how I should integrate this)

    - validating connecting device (should only my laptop and phone)
        - What I'm thinking for the device validation is to only accept 
            connection from my laptop and phones IP, but if there is a better way of doing this do that

    
            
    I have no clue when it comes to Authentication and Encryption, but these are probably the most important   
    - Authentication
    - Encryption

'''