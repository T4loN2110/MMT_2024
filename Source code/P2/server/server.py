import socket
import os
import time

HOST = "127.0.0.1"
PORT = 54321

# Đọc file_list
def readFileList():
    file_list = []
    try:
        with open('file_list.txt', 'r') as file:
            for line in file:
                temp = line.strip().split(' ')
                if len(temp) == 2:
                    name, size = temp
                    file_list.append((name, size))
        return file_list
    except FileNotFoundError:
        print('File not found')
        return file_list
# Xử lý kết nối và yêu cầu từ client
def handleClient(socket):
    try:
        file_list = readFileList()
        # Gửi thông tin các file hiện có cho client
        file_data = '\n'.join([f'{name} {size}' for name, size in file_list])
        socket.sendall(file_data.encode() + b'\n')
        # Chờ client kết nối
        while True:
            try:
            # Nhận tên file yêu cầu tải của client
                download_file = socket.recv(1024).decode()
                if not download_file:
                    break
                file_path = os.path.join('files', download_file)
                if os.path.exists(file_path):
                    # Lấy size của file
                    file_size = os.path.getsize(file_path)
                    socket.sendall(str(file_size).encode() + b'\n')
                    with open(file_path, 'rb') as f:
                        while True:
                            file_content = f.read(1024)
                            if not file_content:
                                break
                            # Gửi toàn bộ nội dung file cho client
                            socket.sendall(file_content)
                            time.sleep(0.1)
                else: 
                    socket.send('File not found'.encode())
            except KeyboardInterrupt:
                socket.close()  
    except KeyboardInterrupt:
        socket.close()
    finally:
        socket.close()
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    print("Waiting for Client")
    try:
        while True:
            conn, addr = s.accept()
            print('Connected successfully!')
            handleClient(conn)
    except KeyboardInterrupt:
        print('Server closed.')
    finally:
        s.close()

if __name__ == '__main__':
    main()