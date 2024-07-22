import socket
import os

HOST = '127.0.0.1'
PORT = 65431
BUFSIZE = 4096

def load_file_list(filename="C:/Users/ACER/Desktop/MMT_2024/Source code/files/file_list.txt"):
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

        with open(os.path.join("files", file_name), 'rb') as file:
            while True:
                bytes_read = file.read(BUFSIZE)
                if not bytes_read:
                    break
                conn.sendall(bytes_read)

except KeyboardInterrupt:
    conn.close()
finally:
    conn.close()
