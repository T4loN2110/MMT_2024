import socket
import threading

HOST = '127.0.0.1'
PORT = 65431

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
try:
    print("Connected by ", addr)
except KeyboardInterrupt:
    conn.close()
finally:
    conn.close()
