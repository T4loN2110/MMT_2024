import socket
import os
import time

HOST = "127.0.0.1"
PORT = 54321

# Đọc file input
def readInputFile():
    input_file = []
    try:
        with open('input.txt', 'r') as file:
            input_file = file.read().splitlines()
            print(input_file)
        return input_file
    except FileNotFoundError:
        return input_file
# Nhận thông tin các file hiện có bên server
def receiveFileList(socket):
    temp = b''
    while True:
        data = socket.recv(1024)
        if not data:
            break
        temp += data
        # Khi hết file
        if b'\n' in temp:
            break

    file_data = temp.decode().strip()
    file_list = file_data.splitlines()
    return file_list
# Tải file từ server
def downloadFile(socket, file_name):
    # Gửi tên file cần tải cho server
    socket.send(file_name.encode())
    file_size = socket.recv(1024).decode()
    if file_size == 'File not found':
        print(f'File {file_name} not found')
        return
    file_size = int(file_size)

    print(f'Downloading {file_name}')
    with open(os.path.join('output', file_name), 'wb') as f:
        total_bytes = 0
        last_update_time = time.time()
        while total_bytes < file_size:
            try:
                file_content = socket.recv(1024)
                if not file_content:
                    break
                f.write(file_content)
                total_bytes += len(file_content)

                # Cập nhật phần trăm tải được mỗi 0.05s
                current_time = time.time()
                if current_time - last_update_time >= 0.05:
                    percent_complete = (total_bytes / file_size) * 100
                    print(f"Downloading {file_name} ... {percent_complete:.2f}%")
                    last_update_time = current_time
            except KeyboardInterrupt: 
                print('Stop downloading')
                return
        print(f"Downloading {file_name} ... 100%")
        print(f"File {file_name} downloaded successfully.")
def main():
    server_address = (HOST, PORT)

    downloaded_files = set()
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f'Connecting to {server_address}')
            client.connect(server_address)
            file_list = receiveFileList(client)
            if not file_list:
                print('No files received from server')
                break
            print('Available file on server:')
            for file in file_list:
                print(file)

            download_files = readInputFile()
            download_files = [f for f in download_files if f not in downloaded_files]
            for file in download_files:
                downloadFile(client, file)
                downloaded_files.add(file)

            print("All files downloaded. Waiting for new files...")
            client.close()
            time.sleep(20)
        except KeyboardInterrupt:
            print('Closed client')
            client.close()
            break

if __name__ == '__main__':
    main()