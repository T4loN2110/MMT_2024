import socket
import threading

HOST = '127.0.0.1'
PORT = 65431
BUFSIZE = 4096

def load_file_list(filename="files/file_list.txt"):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
try:
    print("Connected by ", addr)

    file_list = load_file_list()
    conn.sendall("\n".join(file_list).encode())

    while True:
        file_name = conn.recv(BUFSIZE).decode()
        if not file_name:
            break



except KeyboardInterrupt:
    conn.close()
finally:
    conn.close()
