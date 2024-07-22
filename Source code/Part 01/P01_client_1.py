import socket
import os

HOST = '127.0.0.1'
PORT = 65431
BUFSIZE = 4096
INPUT = "input.txt"
OUTPUT = "output"

def download_file(file_name, client):
    file_size = int(client.recv(BUFSIZE).decode())
    received_size = 0
    with open(os.path.join(OUTPUT, file_name), 'wb') as file:
        while received_size < file_size:
            bytes_read = client.recv(BUFSIZE)
            if not bytes_read:
                break
            file.write(bytes_read)
            received_size += len(bytes_read)
            percent_complete = (received_size / file_size) * 100
            print(f"Downloading {file_name}: {percent_complete:.2f}% complete", end='\r')
            
def open_input_file():
    if os.name == 'nt':
        os.system(f'notepad.exe {INPUT}')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
print("Client connect to server with port: " + str(PORT))
client.connect(server_address)


file_list = client.recv(BUFSIZE).decode()
print("File list from server:")
print(file_list)

try:
    open_input_file()
    while True:
        if os.path.exists(INPUT):
            with open(INPUT, 'r') as file:
                files_to_download = [line.strip() for line in file]
            
            for file_name in files_to_download:
                    client.sendall(file_name.encode())
                    download_file(file_name, client)
except KeyboardInterrupt:
    client.close()
finally:
    client.close()